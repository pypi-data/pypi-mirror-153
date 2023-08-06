#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import random
from tqdm import tqdm

""" Import PyTorch framework """
import torch
import torch.nn as nn
import torch.optim as optim

from Util import Util

import importlib
import config as CFG
importlib.reload(CFG)

device = torch.device(CFG.device)
util = Util(CFG)

class Train():
    def __init__(self, model):
        self.model = model
        self.running_loss_policy = 0.0
        self.running_loss_value = 0.0
        self.epoch_loss = 0.0
        self.learning_rate = None

        self.optimizer = optim.SGD(self.model.parameters(), 
                                   lr=CFG.learning_rate, 
                                   momentum=0.9, 
                                   weight_decay=CFG.weight_decay)

        # self.optimizer = optim.Adam(self.model.parameters(),
        #                             lr=CFG.learning_rate, 
        #                             weight_decay=CFG.weight_decay)                                   

        """ 学習係数を 0.2, 0.02, 0.002, 0.0002 に段階的に下げます """
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, 
                                              step_size=1, 
                                              gamma=0.1) 

        util.save_model_info()


    def __call__(self, dataset):

        self.model.train()

        batch_iteration_size = math.ceil(len(dataset) / CFG.batch_size)

        if batch_iteration_size == 0:
            batch_iteration_size = 1

        # print('Train loop')
        for epoch in (range(1, CFG.num_epoch + 1)):

            """ 全データセットをシャッフル """
            dataset = random.sample(dataset, len(dataset))

            iteration_size = math.ceil(len(dataset) / CFG.batch_size)

            for i in range(iteration_size):
                input_features, pi, z = util.make_batch(dataset[i:i + CFG.batch_size])
                self.train(input_features, pi, z)

            util.output_train_log(epoch, self.running_loss_policy, self.running_loss_value, batch_iteration_size)

            self.running_loss_policy = 0.0
            self.running_loss_value = 0.0


    def train(self, input_features,  pi, z):
        """ 
        define (z - v)^2 - pi^T * log(p) + c||θ||2
        """

        """ Predict policy and state value """
        p, v = self.model(input_features)

        """ Categorical Cross-entropy Error """
        p = p + 1e-10
        policy_loss = -(pi * torch.log(p)).sum(dim=1).mean()

        """ Mean Square Error """
        value_loss = (z - v).pow(2).mean()

        """ L2 regularization c||θ||2 """
        """ weight decayとして、optimizerに組み込まれています。"""
        
        
        """ Loss function """
        loss = policy_loss + value_loss

        """ Update network paramters. """
        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.model.parameters(), 0.5)
        self.optimizer.step()

        """ Running loss """
        self.running_loss_policy += policy_loss
        self.running_loss_value += value_loss

    # def save(self):
    #     try:
    #         torch.save(self.model.state_dict(), CFG.model_path)
    #     except:
    #         print("model save error.")
    #         raise()

    # def _make_batch(self, dataset):
    #     """ 毎回訓練データが変わるため、DataLoaderは使わない """
    #     input_features = [data[0] for data in dataset]
    #     pi = [data[1] for data in dataset]
    #     z = [data[2] for data in dataset]

    #     input_features = torch.FloatTensor(input_features).to(CFG.device)
    #     pi = torch.FloatTensor(pi).to(CFG.device)
    #     z = torch.FloatTensor(z).to(CFG.device)

    #     return [input_features, pi, z]

    def scheduler_step(self):
        self.scheduler.step()