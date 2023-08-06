import numpy as np
import os, sys
import pickle
import paddle

from .abc_interpreter import Interpreter


class InfluenceFunctionInterpreter(Interpreter):
    """

    """

    def __init__(self, paddle_model: callable, device: str = 'gpu:0', use_cuda=None):
        """
        
        Args:
            paddle_model (callable): A model with :py:func:`forward` and possibly :py:func:`backward` functions.
            device (str): The device used for running ``paddle_model``, options: ``"cpu"``, ``"gpu:0"``, ``"gpu:1"`` 
                etc.
        """
        Interpreter.__init__(self, paddle_model, device, use_cuda)

    def train(self, ):
        return
