import os.path as osp
import paddle
import paddle.nn.functional as F
from paddle.autograd import grad
import numpy as np
import datetime
import time
from ..interpreter.abc_interpreter import Interpreter


def sample_parse_nlp_example(sample):
    """This is an example function for parsing samples. Users may need to give this function.

    """
    inputs = sample['input_ids'], sample['token_type_ids']
    target = sample['target']
    return inputs, target


class InfluenceFunctionInterpreter(Interpreter):
    def __init__(self, paddle_model: callable, sample_parse_func: callable, device: str = 'gpu:0', use_cuda=None):
        """
        
        Args:
            paddle_model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            sample_parse_func (callable): A function that parses a wrapped sample to ``inputs`` and ``target``.
            device (str): The device used for running ``paddle_model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        Interpreter.__init__(self, paddle_model, device, use_cuda)
        self.sample_parse_func = sample_parse_func

    def train(self, train_args):

        raise NotImplementedError("To do")

    def interpret(self, sample_test, train_lader, damp=0.1, scale=1000.0, recursion_depth=100):


        return


def calc_influence_single(model, train_loader, test_loader, test_id_num,
                          training_sample_num,
                          damp, scale, recursion_depth, r, 
                          s_test_vec=None,
                          recompute_s_test=False,
                          save_dir=None):
    """Calculates the influences of all training data points on a single
    test dataset image.

    Args:
        model: pytorch model
        train_loader: DataLoader, loads the training dataset
        test_loader: DataLoader, loads the test dataset
        test_id_num: int, id of the test sample for which to calculate the
            influence function
        device (_type_): _description_
        training_sample_num (_type_): _description_
        damp (_type_): _description_
        scale (_type_): _description_
        recursion_depth (_type_): _description_
        r (_type_): _description_
        s_test_vec (_type_, optional): list of torch tensor, contains s_test vectors. If left
            empty it will also be calculated
        recompute_s_test (bool, optional): whether force to recompute s_test. Defaults to False.

    Returns:
        influence: list of float, influences of all training data samples
            for one test sample
        harmful: list of float, influences sorted by harmfulness
        helpful: list of float, influences sorted by helpfulness
        test_id_num: int, the number of the test dataset point
            the influence was calculated for
    """

    # Calculate s_test vectors if not provided
    if not s_test_vec:
        filename = f'{save_dir}/s_test_vec_{test_id_num}.pd'
        if not osp.exists(filename) or recompute_s_test:
            sample_test = test_loader.dataset[test_id_num]

            s_test_vec = _calc_s_test_single(model, sample_test, train_loader,
                                            damp=damp, scale=scale, recursion_depth=recursion_depth,
                                            r=r)

            paddle.save(s_test_vec, filename)
        else:
            print("Loading pre-computed s_test_vec from", filename)
            s_test_vec = paddle.load(filename)

    # Calculate the influence function
    train_dataset_size = len(train_loader.dataset)
    influences = []
    for i in range(train_dataset_size):
        if i % 100 == 0:
            print(datetime.datetime.now(), i)
        if i == training_sample_num:
            break
            
        sample_z = train_loader.dataset[i]
        
        grad_z_vec = _grad_z(sample_z, model)
        
        tmp_influence = -sum(
            [
                paddle.sum(k * j)
                for k, j in zip(grad_z_vec, s_test_vec)
            ]) / train_dataset_size
        influences.append(tmp_influence.numpy())

    harmful = np.argsort(influences)
    helpful = harmful[::-1]

    return influences, harmful.tolist(), helpful.tolist(), test_id_num


def _calc_s_test_single(model, sample_test, train_loader,
                        damp=0.1, scale=1000, recursion_depth=100, r=5):
    """Calculates s_test for a single test image taking into account the whole
    training dataset. s_test = invHessian * nabla(Loss(test_img, model params))
    Arguments:
        model: pytorch model, for which s_test should be calculated
        sample_test: test image
        train_loader: pytorch dataloader, which can load the train data
        device: 
        damp: float, influence function damping factor
        scale: float, influence calculation scaling factor
        recursion_depth: int, number of recursions to perform during s_test
            calculation, increases accuracy. r*recursion_depth should equal the
            training dataset size.
        r: int, number of iterations of which to take the avg.
            of the h_estimate calculation; r*recursion_depth should equal the
            training dataset size.
    Returns:
        s_test_vec: torch tensor, contains s_test for a single test image"""
    s_test_vec_list = []
    train_loader_iters = train_loader.__iter__()
    for i in range(r):
        s_test_vec_list.append(_s_test(sample_test, model, train_loader_iters,
                                        damp=damp, scale=scale,
                                        recursion_depth=recursion_depth))

    s_test_vec = s_test_vec_list[0]
    for i in range(1, r):
        for j in range(len(s_test_vec)):
            s_test_vec[j] += s_test_vec_list[i][j]

    s_test_vec = [s_test / r for s_test in s_test_vec]

    return s_test_vec


def _s_test(sample_test, model, train_loader, 
            damp=0.1, scale=1000.0, recursion_depth=100):
    """s_test can be precomputed for each test point of interest, and then
    multiplied with grad_z to get the desired value for each training point.
    Here, strochastic estimation is used to calculate s_test. s_test is the
    Inverse Hessian Vector Product.
    Arguments:
        sample_test: torch tensor, test data points, such as test images
        model: torch NN, model used to evaluate the dataset
        train_loader: torch Dataloader, can load the training dataset
        device: 
        damp: float, dampening factor
        scale: float, scaling factor
        recursion_depth: int, number of iterations aka recursion depth
            should be enough so that the value stabilises.
    Returns:
        h_estimate: list of torch tensors, s_test"""
    v = _grad_z(sample_test, model)
    h_estimate = v.copy()

    end = time.time()
    
    def func(module, input, output):
        scale = paddle.standard_normal(output.shape, output.dtype) + 1.0
        # print(output.shape, std.mean(), std.std(), output.mean(), output.std())
        
        return scale * output
    
    for i in range(recursion_depth):

        h_estimate_prev = h_estimate
        for sample in train_loader:
            x = sample['input_ids']
            t = sample['target']
            t = paddle.argmax(t, axis=-1)
            token_type_ids = sample['token_type_ids']
            
            # add some noises to make the gradients more sensisble.
            hooks = []
            for name, layer in model.named_sublayers():
                if name in [WORD_EMBEDDING_NAME]:
                    h = layer.register_forward_post_hook(func)
                    hooks.append(h)

            y = model(x, token_type_ids)
            loss = _calc_loss(y, t)
            
            for h in hooks:
                h.remove()
            
            params = [ p for p in model.parameters() if not p.stop_gradient ]
            hv = _hvp(loss, params, h_estimate)
            # Recursively caclulate h_estimate
            with paddle.no_grad():
                h_estimate = [ 
                    _v + (1 - damp) * _h_e - _hv / scale
                    for _v, _h_e, _hv in zip(v, h_estimate, hv)]

            break
        
        if i % max(100, recursion_depth // 5) == 0 or (i == recursion_depth - 1):
            print("Calc. s_test recursions: ", i, recursion_depth)
            he_vec = [_he.detach().reshape((-1,)) - _he_prev.detach().reshape((-1,))
                      for _he, _he_prev in zip(h_estimate, h_estimate_prev)]
            print(paddle.concat(he_vec).norm())
            print(f"Elapsed time (s-test): {time.time() - end: .2f} s.")
            end = time.time()
            
    return h_estimate


def _calc_loss(y, t):
    """Calculates the loss
    Arguments:
        y: torch tensor, input with size (minibatch, nr_of_classes)
        t: torch tensor, target expected by loss of size (0 to nr_of_classes-1)
    Returns:
        loss: scalar, the loss"""
    ####################
    # if dim == [0, 1, 3] then dim=0; else dim=1
    ####################
    # y = torch.nn.functional.log_softmax(y, dim=0)
    loss = F.cross_entropy(y, t)
    # y = torch.nn.functional.log_softmax(y)
    # loss = torch.nn.functional.nll_loss(
    #     y, t, weight=None, reduction='mean')
    return loss


def _grad_z(sample, model):
    """Calculates the gradient z. One grad_z should be computed for each
    training sample.
    Arguments:
        z: torch tensor, training data points
            e.g. an image sample (batch_size, 3, 256, 256)
        t: torch tensor, training data labels
        model: torch NN, model used to evaluate the dataset
    Returns:
        grad_z: list of torch tensor, containing the gradients
            from model parameters to loss"""
    model.eval()
    z = sample['input_ids']
    t = sample['target']
    token_type_ids = sample['token_type_ids']
        
    z = paddle.to_tensor([z])
    t = paddle.to_tensor([t])
    t = paddle.argmax(t, axis=-1)
    token_type_ids = paddle.to_tensor([token_type_ids])
        
    y = model(z, token_type_ids)
    loss = _calc_loss(y, t)
    # Compute sum of gradients from model parameters to loss
    params = [ p for p in model.parameters() if not p.stop_gradient ]

    # this is ok
    # model.clear_gradients()
    # loss.backward()
    # for n, p in list(model.named_parameters()):
    #     print(n, p.grad)

    return list(grad(loss, params, create_graph=False))


def _hvp(y, w, v):
    """Multiply the Hessians of y and w by v.
    Uses a backprop-like approach to compute the product between the Hessian
    and another vector efficiently, which even works for large Hessians.
    Example: if: y = 0.5 * w^T A x then hvp(y, w, v) returns and expression
    which evaluates to the same values as (A + A.t) v.
    Arguments:
        y: scalar/tensor, for example the output of the loss function
        w: list of torch tensors, tensors over which the Hessian
            should be constructed
        v: list of torch tensors, same shape as w,
            will be multiplied with the Hessian
    Returns:
        return_grads: list of torch tensors, contains product of Hessian and v.
    Raises:
        ValueError: `y` and `w` have a different length."""
    if len(w) != len(v):
        raise(ValueError("w and v must have the same length."))
        
    # print('hvp:', len(w))

    # First backprop
    # https://github.com/PaddlePaddle/Paddle/issues/36357
    # first_grads = grad(y, w, retain_graph=True, create_graph=True)
    
    # this is an alternative, but it may be not accurate nor correct
    y.backward(retain_graph=True)
    first_grads = [w_i.grad for w_i in w]

    # Elementwise products
    elemwise_products = 0
    for grad_elem, v_elem in zip(first_grads, v):
        elemwise_products += paddle.sum(grad_elem * v_elem)

    # Second backprop
    # return_grads = grad(elemwise_products, w, create_graph=True)
    # this is an alternative, but it may be not accurate nor correct
    elemwise_products.backward()
    return_grads = [w_i.grad for w_i in w]

    return return_grads
