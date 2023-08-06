import numpy as np
import torch


def db(x):
    if isinstance(x, np.ndarray):  # TODO:make a function
        return 10 * np.log10(x)
    elif isinstance(x, torch.Tensor):  # TODO:make a function
        return 10 * torch.log10(x)
    else:
        # TODO:change to logger
        raise Exception("AA")
