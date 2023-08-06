import numpy as np
from tqdm import tqdm

import config as CFG
import copy

from agent import Agent
from MCTS import Node
from Util import Util

util = Util(CFG)


class Evaluate():
    def __init__(self, env, model, CFG):
        self.env = env
        self.model = model
        self.CFG = CFG

    def play_AZ_vs_AZ(self, env, model1, model2, play_count=1):
        print('AlphaZero vs AlphaZero')

        player1 = Agent(env, model1, train=False)
        player2 = Agent(env, model2, train=False)

        win_model1 = 0
        win_model2 = 0

        for count in (range(play_count)):
            
            state = env.reset()
            node1 = Node(state)
            node2 = Node(state)

            node1.player = CFG.first_player
            node2.player = CFG.second_player

            action_count = 0

            while True:
                """ AlphaZero 1 turn """
                action_count += 1
                node1 = player1.alpha_zero(node1)
                state, reward, done = env.step(node1.action)

                if play_count==1: 
                    util.show_board(state)

                if done:
                    win_model1 += abs(reward)
                    break

                node2 = util.get_next_node(node2, node1.action)

                """ AlphaZero 2 turn """
                action_count += 1
                node2 = player2.alpha_zero(node2)
                state, reward, done = env.step(node2.action)

                if play_count==1: 
                    util.show_board(state)

                if done:
                    win_model2 += abs(reward)
                    break

                node1 = util.get_next_node(node1, node2.action)

            print ("count model1 model2", action_count, win_model1, win_model2)
        print()


    def play_human_vs_AZ(self, env, model):

        print('Human vs AlphaZero')
        win_human = 0
        win_alpha_zero = 0

        player = Agent(env, model, train=False)

        """ Initialize  """
        state = env.reset()
        node = Node(state)
        util.show_board(state)

        while True:
            
            """ Human turn """
            action = player.human(node.states[0])
            state, reward, done = env.step(action)

            util.show_board(state)

            if done:
                win_human += reward * self.CFG.first_player
                break

            # ここは、player_human に入れるか
            node = util.get_next_node(node, action)

            """ AlphaZero turn """
            node = player.alpha_zero(node)
            state, reward, done = env.step(node.action)

            util.show_board(state)

            if done:
                win_alpha_zero += reward
                break

        print ("AlphaZero, Human", win_alpha_zero, win_human)

    def play_AZ_vs_human(self, env, model):

        print('AlphaZero vs Human')

        win_human = 0
        win_alpha_zero = 0

        player = Agent(env, model, train=False)

        """ Initialize  """
        state = env.reset()
        node = Node(state)

        util.show_board(state)

        while True:

            """ AlphaZero turn """
            node = player.alpha_zero(node)
            state, reward, done = env.step(node.action)

            util.show_board(state)

            if done:
                win_alpha_zero += reward
                break

            """ Human turn """
            action = player.human(env.state)
            state, reward, done = env.step(action)

            util.show_board(state)

            if done:
                win_human -= reward
                break

            node = util.get_next_node(node, action)

        print ("AlphaZero, Human", win_alpha_zero, win_human)
        

    def play_random_vs_AZ(self, env, model, play_count=1):

        print('Random vs AlphaZero')
        win_random = 0
        win_alpha_zero = 0

        player = Agent(env, model, train=False)

        for count in (range(play_count)):
            
            state = env.reset()
            
            ### DEBUG ###
            # state = [[1, 1, 1, 1, 1, 1],
            #          [-1, -1, -1, -1, -1, -1],
            #          [-1, -1, -1, -1, -1, -1],
            #          [-1, -1, -1, -1, -1, -1],
            #          [-1, -1, -1, -1, -1, -1],
            #          [-1, -1, -1, -1, -1, -1]]

            # state[5][1] = 0
            # state[2][3] = 0

            node = Node(state)

            while True:
                """ Random turn """
                action = player.random(state)
                state, reward, done  = env.step(action)

                if play_count==1: util.show_board(state)

                if done:
                    win_random += abs(reward)
                    break

                node = util.get_next_node(node, action)
                
                """ AlphaZero turn """
                node = player.alpha_zero(node)
                state, reward, done = env.step(node.action)

                if play_count==1: util.show_board(state)

                if done:
                    win_alpha_zero += abs(reward)
                    break

            print ("Random , AlphaZero ",win_random, win_alpha_zero)
        print()


    def play_AZ_vs_random(self, env, model, play_count=1):

        print('AlphaZero vs Random')
        win_random = 0
        win_alpha_zero = 0
        
        player = Agent(env, model, train=False)

        for count in (range(play_count)):
            
            state = env.reset()
            node = Node(state)

            while True:

                """ AlphaZero turn """
                node = player.alpha_zero(node)
                state, reward, done = env.step(node.action)

                if play_count==1:util.show_board(state)

                if done:
                    win_alpha_zero += abs(reward)
                    break

                """ Random turn """
                action = player.random(state)
                state, reward, done  = env.step(action)

                if play_count==1:util.show_board(state)

                if done:
                    win_random += abs(reward)
                    break

                node = util.get_next_node(node, action)

            print ("AlphaZero , Random ", win_alpha_zero , win_random)
        print()



""" ***************************************************************  """ 


def play_AZ_vs_AZ(env, model1, model2, play_count=1):
    print('AlphaZero vs AlphaZero')

    player1 = Agent(env, model1, train=False)
    player2 = Agent(env, model2, train=False)

    win_model1 = 0
    win_model2 = 0

    for count in (range(play_count)):
        
        state = env.reset()
        node1 = Node(state)
        node2 = Node(state)

        node1.player = CFG.first_player
        node2.player = CFG.second_player

        action_count = 0

        while True:
            """ AlphaZero 1 turn """
            action_count += 1
            node1 = player1.alpha_zero(node1)
            state, reward, done = env.step(node1.action)

            if play_count==1: 
                util.show_board(state)

            if done:
                win_model1 += abs(reward)
                break

            node2 = util.get_next_node(node2, node1.action)

            """ AlphaZero 2 turn """
            action_count += 1
            node2 = player2.alpha_zero(node2)
            state, reward, done = env.step(node2.action)

            if play_count==1: 
                util.show_board(state)

            if done:
                win_model2 += abs(reward)
                break

            node1 = util.get_next_node(node1, node2.action)

        print ("count model1 model2", action_count, win_model1, win_model2)
    print()


def play_human_vs_AZ(env, model):

    print('Human vs AlphaZero')
    win_human = 0
    win_alpha_zero = 0

    player = Agent(env, model, train=False)

    """ Initialize  """
    state = env.reset()
    node = Node(state)
    util.show_board(state)

    while True:
        
        """ Human turn """
        action = player.human(node.states[0])
        state, reward, done = env.step(action)

        util.show_board(state)

        if done:
            win_human += reward * CFG.first_player
            break

        # ここは、player_human に入れるか
        node = util.get_next_node(node, action)

        """ AlphaZero turn """
        node = player.alpha_zero(node)
        state, reward, done = env.step(node.action)

        util.show_board(state)

        if done:
            win_alpha_zero += reward
            break

    print ("AlphaZero, Human", win_alpha_zero, win_human)

def play_AZ_vs_human(env, model):

    print('AlphaZero vs Human')

    win_human = 0
    win_alpha_zero = 0

    player = Agent(env, model, train=False)

    """ Initialize  """
    state = env.reset()
    node = Node(state)

    util.show_board(state)

    while True:

        """ AlphaZero turn """
        node = player.alpha_zero(node)
        state, reward, done = env.step(node.action)

        util.show_board(state)

        if done:
            win_alpha_zero += reward
            break

        """ Human turn """
        action = player.human(env.state)
        state, reward, done = env.step(action)

        util.show_board(state)

        if done:
            win_human -= reward
            break

        node = util.get_next_node(node, action)

    print ("AlphaZero, Human", win_alpha_zero, win_human)
    

def play_random_vs_AZ(env, model, play_count=1):

    print('Random vs AlphaZero')
    win_random = 0
    win_alpha_zero = 0

    player = Agent(env, model, train=False)

    for count in (range(play_count)):
        
        state = env.reset()
        
        ### DEBUG ###
        # state = [[1, 1, 1, 1, 1, 1],
        #          [-1, -1, -1, -1, -1, -1],
        #          [-1, -1, -1, -1, -1, -1],
        #          [-1, -1, -1, -1, -1, -1],
        #          [-1, -1, -1, -1, -1, -1],
        #          [-1, -1, -1, -1, -1, -1]]

        # state[5][1] = 0
        # state[2][3] = 0

        node = Node(state)

        while True:
            """ Random turn """
            action = player.random(state)
            state, reward, done  = env.step(action)

            if play_count==1: util.show_board(state)

            if done:
                win_random += abs(reward)
                break

            node = util.get_next_node(node, action)
            
            """ AlphaZero turn """
            node = player.alpha_zero(node)
            state, reward, done = env.step(node.action)

            if play_count==1: util.show_board(state)

            if done:
                win_alpha_zero += abs(reward)
                break

        print ("Random , AlphaZero ",win_random, win_alpha_zero)
    print()


def play_AZ_vs_random(env, model, play_count=1):

    print('AlphaZero vs Random')
    win_random = 0
    win_alpha_zero = 0
    
    player = Agent(env, model, train=False)

    for count in (range(play_count)):
        
        state = env.reset()
        node = Node(state)

        while True:

            """ AlphaZero turn """
            node = player.alpha_zero(node)
            state, reward, done = env.step(node.action)

            if play_count==1:util.show_board(state)

            if done:
                win_alpha_zero += abs(reward)
                break

            """ Random turn """
            action = player.random(state)
            state, reward, done  = env.step(action)

            if play_count==1:util.show_board(state)

            if done:
                win_random += abs(reward)
                break

            node = util.get_next_node(node, action)

        print ("AlphaZero , Random ", win_alpha_zero , win_random)
    print()



def play_random_vs_alphabeta(env, play_count=1):

    print('AlphaBeta vs Random')

    win_random = 0
    win_alphabeta = 0
    
    player = Agent(env)

    for count in (range(play_count)):
        
        state = env.reset()

        while True:

            """ Random turn """
            # print("Random turn")
            action = player.random(state)
            state, reward, done  = env.step(action)

            if play_count==1:util.show_board(state)

            if done:
                win_random += abs(reward)
                break


            """ AlphaBeta turn """
            # print("AlphaBeta turn")
            action = player.player_alphabeta(env, 1) # 1:自分の手番
            state, reward, done = env.step(action)

            if play_count==1:util.show_board(state)

            if done:
                win_alphabeta += abs(reward)
                break

        print ("Random, AlphaBeta", win_random, win_alphabeta)
    print()


def play_alphabeta_vs_random(env, play_count=1):

    print('AlphaBeta vs Random')

    win_random = 0
    win_alphabeta = 0
    
    player = Agent(env)

    for count in (range(play_count)):
        
        state = env.reset()

        while True:

            """ AlphaBeta turn """
            action = player.player_alphabeta(env, 1) # 1:自分の手番
            state, reward, done = env.step(action)

            if play_count==1:util.show_board(state)

            if done:
                win_alphabeta += abs(reward)
                break

            """ Random turn """
            action = player.random(state)
            state, reward, done  = env.step(action)

            if play_count==1:util.show_board(state)

            if done:
                win_random += abs(reward)
                break

        print ("AlphaBeta, Random ", win_alphabeta, win_random)

    print()


def play_random_vs_minimax(env, play_count=1):

    print('Random vs MiniMax')
    win_random = 0
    win_minimax = 0
    
    player = Agent(env)

    for count in (range(play_count)):
        
        state = env.reset()

        while True:

            """ Random turn """
            action = player.random(state)
            state, reward, done  = env.step(action)

            if play_count==1:util.show_board(state)

            if done:
                win_random += abs(reward)
                break

            """ AlphaBeta turn """
            action = player.player_minimax(env, 1)
            state, reward, done = env.step(action)

            if play_count==1:util.show_board(state)

            if done:
                win_minimax += abs(reward)
                break

        print ("Random , MiniMax", win_random, win_minimax)

    print()
