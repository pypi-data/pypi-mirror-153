#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy 

""" 
Alpha–beta pruning
"""
def alphabeta(env, α, β, player):

    """ ゲーム終了の場合 """
    if env.done:
        # print('reward', env.reward)
        return env.reward # 報酬: -1, 0, 1
 
    """ 合法手の取得 """
    legal_actions = env.get_legal_actions(env.state)

    """
    先手にとっては最大となる価値（報酬）を選ばせ、
    後手にとっては最小となる価値（報酬）を選ばせる。
    """
    if player == 1:
        value = -2 # 状態価値に−∞を設定 float('inf')

        """ 合法手で最大値を取得 """
        for action in legal_actions: 
            child = copy.deepcopy(env) # 環境のコピー
            child.step(action) # 実行
            value = max(value, alphabeta(child, α, β, -player)) # 現在の価値とalphabetaの価値のうち大きい方を取得
            if value >= β:
                # print('β cutoff')
                break
            α = max(α, value)  # 最大値を返却
        return value 

    else:
        value = +2 # ∞
        for action in legal_actions: 
            child = copy.deepcopy(env) # 環境のコピー
            child.step(action) # 実行
            value = min(value, alphabeta(child, α, β, -player))
            if value <= α:
                # print('α cutoff')
                break
            β = min(β, value)
        return value 


"""
Alpha-betaプレーヤーで最善の手を取得 
"""
def player_alphabeta(env, player):

    """ 最善手と状態価値を初期化 """
    best_action = -1
    best_value = -2

    """ αとβを初期化 """ 
    α = -2
    β = 2

    """ 合法手でループ """
    legal_actions = env.get_legal_actions(env.state)
    print('legal_actions', legal_actions)

    for action in legal_actions:

        child = copy.deepcopy(env)
        child.step(action)

        """ 
        Alpha-betaアルゴリズムで探索して、状態価値を取得。
        後手の価値を先手にとってはマイナスの価値とする。
        """
        value = -alphabeta(child, α, β, -player) 

        """ 取得した価値が最善の場合よりも大きい場合は値を交換 """
        if value > best_value:
            best_value = value   # 取得した価値を最善の価値に設定
            best_action = action # その場合の行動を最善の行動とする 

        print('action: ', action ,value)

    print('best_action', best_action)
    return best_action # 最善の行動インデックスを返却


