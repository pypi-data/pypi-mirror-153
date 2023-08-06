#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Import PyTorch framework """
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleNet(nn.Module):

    def __init__(self, CFG):
        super(SimpleNet, self).__init__()
        self.CFG = CFG

    def forward(self, x):
        p = 1 / self.FG.action_size
        p = torch.FloatTensor([[p] * self.CFG.action_size])
        v = torch.FloatTensor([[0]])
        return  p, v
