#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Import PyTorch framework """
import torch
import torch.nn as nn
import torch.nn.functional as F

import importlib
import config as CFG
importlib.reload(CFG)

class SimpleNet(nn.Module):

    def __init__(self):
        super(SimpleNet, self).__init__()

    def forward(self, x):
        p = 1 / CFG.action_size
        p = torch.FloatTensor([[p] * CFG.action_size])
        v = torch.FloatTensor([[0]])
        return  p, v