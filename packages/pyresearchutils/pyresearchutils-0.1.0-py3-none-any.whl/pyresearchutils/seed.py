import random

import numpy as np
from pyresearchutils.logger import info


def set_seed(seed: int = 0):
    import torch
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    info(f"Setting Random Seed to {seed}")
