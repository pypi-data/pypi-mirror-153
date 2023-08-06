#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import copy
import torch

class Test:
    def __init__(self):
        print("Hello world!")
        
class Util:
    def __init__(self, CFG):
        self.CFG = CFG

    def make_batch(self, dataset):
        """ 毎回訓練データが変わるため、DataLoaderは使わない """
        input_features = [data[0] for data in dataset]
        pi = [data[1] for data in dataset]
        z = [data[2] for data in dataset]

        input_features = torch.FloatTensor(input_features).to(self.CFG.device)
        pi = torch.FloatTensor(pi).to(self.CFG.device)
        z = torch.FloatTensor(z).to(self.CFG.device)

        return [input_features, pi, z]

    def output_train_log(self, epoch, running_loss_policy, running_loss_value, batch_iteration_size):

        epoch_loss_policy = running_loss_policy / batch_iteration_size
        epoch_loss_value = running_loss_value / batch_iteration_size
        epoch_loss = epoch_loss_policy + epoch_loss_value

        print('epoch: {:02}/{} lr: {:.5f}   toatl loss: {:.5f} pi_loss: {:.5f} value_loss: {:.5f}'
            .format(
                epoch, 
                self.CFG.num_epoch, 
                self.CFG.learning_rate,
                epoch_loss, 
                epoch_loss_policy, 
                epoch_loss_value
            )
        )

    def save(self, model):
        try:
            torch.save(model.state_dict(), self.CFG.model_path)
        except:
            print("model save error.")
            raise()

    def save_model_info(self):
        with open(self.CFG.model_path + '.txt', mode='w') as f:
            f.write('n_residual_block:{}\n'.format(self.CFG.n_residual_block))
            f.write('resnet_channels:{}\n'.format(self.CFG.resnet_channels))
            f.write('history_size:{}\n'.format(self.CFG.history_size))
            f.write('hidden_size:{}\n'.format(self.CFG.hidden_size))


    def save_dataset(self, filepath, dataset):
        try:
            dataset = np.array(dataset, dtype=object)
            # with open(filepath, 'wb') as f:
            #     np.save(f, dataset)        
            np.save(filepath, dataset)
        except:
            print("save_dataset error")
            raise()


    def save_iteration_counter(self, iteration_counter_path, i):
        with open(iteration_counter_path, mode='w') as f:
            f.write(str(i))

    def show_board(self, state):
        print()    
        print(" ", end="")
        for i in  range(len(state)):
            print(i, end=" ")
        print()

        for i, row in enumerate(np.array(state)):
            print(np.where(0 > row, 2, row), i)

    def indicator(self, play_count):
        progress = "";
        for i in range(play_count):
            progress += "■" # □
        print("\r"+ progress + " " + str(play_count), end="手目")

    def get_child_nodes(self, node):
        child_nodes = []
        for child_node in node.child_nodes:
            edge = copy.copy(node) # １次要素を複製
            edge.p = copy.copy(child_node.p)
            edge.w = child_node.w
            edge.Q = child_node.Q
            edge.n = child_node.n
            child_nodes.append(edge)

        return child_nodes

    def create_states(self, state):
        state = copy.deepcopy(state) 
        states = [[[0] * self.CFG.board_width] * self.CFG.board_width] * (self.CFG.history_size - 1)
        states.insert(0, state)

        return states


    def state2feature(self, node):# gomoku用
        """ 
        局面画像をバイナリーデータに変換して入力特徴とします。
        後手(1)履歴 + 先手(-1)履歴 + 手番
        """
        states = node.states
        player = node.player

        states = torch.FloatTensor(states)
        ones = torch.ones((self.CFG.history_size, self.CFG.board_width, self.CFG.board_width)) # For state
        turn = torch.ones((1, self.CFG.board_width, self.CFG.board_width))

        state_w = (states == 1) * ones # 現在の白面
        state_b = (states == -1) * ones # 現在の黒面
        turn = (player == -1) * turn # 手番（黒の番なら１、白の番なら０）
        input_features = torch.vstack((state_w, state_b, turn))
        input_features = torch.unsqueeze(input_features, 0) # バッチの次元を追加
        node.input_features = input_features
        return node.input_features.to(self.CFG.device)


    def state2feature_with_one_hot(self, node):# gomoku用
        """ 
        局面画像をバイナリーデータに変換して入力特徴とします。
        後手(1)履歴 + 先手(-1)履歴 + 手番
        """
        state = node.states[0]
        player = node.player

        state = torch.FloatTensor(state)
        ones = torch.ones((1, self.CFG.board_width, self.CFG.board_width)) # For state
        history = torch.zeros((self.CFG.history_size, self.CFG.board_width, self.CFG.board_width)) # For state
        turn = torch.ones((1, self.CFG.board_width, self.CFG.board_width))

        state_w = (state == 1) * ones # 現在の白面
        state_b = (state == -1) * ones # 現在の黒面

        """ one-hot tensor """
        for i, action in enumerate(node.actions):
            x1 = node.action // self.CFG.board_width # Row
            x2 = node.action % self.CFG.board_width  # Column
            history[i][x1][x2] = 1

        turn = (player == -1) * turn # 手番（黒の番なら１、白の番なら０）
        input_features = torch.vstack((state_w, state_b, history, turn))
        input_features = torch.unsqueeze(input_features, 0) # バッチの次元を追加
        node.input_features = input_features

        return node.input_features.to(self.CFG.device)

    def one_hot_encording(self, node):

        n = np.array([0] * self.CFG.action_size)

        for child_node in node.child_nodes:
            n[child_node.action] = child_node.n

        """ one hot vector """
        pi = [0] * self.CFG.action_size
        max_index = n.argmax()
        pi[max_index] = 1.0

        return pi

    def pobability_distribution(self, node):

        pi = np.array([0] * self.CFG.action_size)

        for child_node in node.child_nodes:
            pi[child_node.action] = child_node.n

        """ Normalize pi """
        pi_sum = pi.sum()
        if pi_sum > 0:
            pi = pi / pi_sum

        return pi.tolist()

    def get_next_states(self, states, action, player):
        """ スタックに次の状態を追加して、古い状態を切り捨てる """
        x1, x2 = (action // self.CFG.board_width), (action % self.CFG.board_width)
        next_states = copy.deepcopy(states)
        state = copy.deepcopy(next_states[0])
        state[x1][x2] = player # 石を置く
        next_states.insert(0, state) # 先頭に現在局面を追加
        next_states = next_states[:-1] # 最後の局面を廃棄
        return next_states

    def get_next_actions(self, actions):
        next_actions = copy.deepcopy(actions)
        next_actions = next_actions[:-1]
        next_actions.insert(0, next_actions) # 先頭に現在局面を追加
        return next_actions

    def get_next_node(self, node, action):
        """ 遷移先のノードを取得する処理 """
        if len(node.child_nodes) > 0 :
            """ 子ノードがある場合は行動先に遷移 """
            for child_node in node.child_nodes:
                if child_node.action == action:
                    next_node = child_node
                    break
        else:
            """ 初回訪問の場合は、今のノードを直接書き換える """
            states = self.get_next_states(node.states, action, node.player)
            next_node = copy.deepcopy(node)
            next_node.states = states
            next_node.player = -node.player

        return next_node
