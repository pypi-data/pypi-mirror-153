#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fonction d'initialisation des seed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Created on Thu May 19 09:51:12 2022

@author: Cyrile Delestre
"""

import random

import numpy as np


def set_seed(seed: int):
    r"""
    Fonction permettant d'initialiser tous
    les générateurs pseudo-aléatoire (Python +
    numpy + PyTorch si possible + cuda si possible).
    Permettant d'assurer la reproductivité d'une expérience.

    Parameters
    ----------
    seed: int
        Racine souhaitée.
    """
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available() > 0:
            torch.cuda.manual_seed_all(seed)
    except ModuleNotFoundError:
        pass

