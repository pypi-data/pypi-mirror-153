#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

class TicTacToe():
    def __init__(self):
        self.width = 3 #CFG.board_width
        self.action_size = self.width * self.width
        self.reset()

    def reset(self):
        self.state = [[0 for x in range(0, self.width)] for y in range(0, self.width)]
        self.done = False
        self.player = -1
        self.reward = 0
        return self.state

    def step(self, a):
        x1, x2 = (a // self.width), (a % self.width)
        self.state[x1][x2] = self.player

        if self._is_done(a):
            self.done = True
            self.reward = self.player

        elif self._is_draw():
            self.done = True
            self.reward = 0

        else:
            pass

        self.player = -self.player
        return self.state, self.reward, self.done

    def get_legal_actions(self, state):
        state = np.array(state, dtype=np.float32).reshape(-1)
        return np.where(state==0)[0]

    def _is_done(self, a):
        s = self.state

        three = self.player * 3

        if s[0][0] + s[0][1] + s[0][2] == three or \
            s[1][0] + s[1][1] + s[1][2] == three or \
            s[2][0] + s[2][1] + s[2][2] == three  or \
            s[0][0] + s[1][0] + s[2][0] == three  or \
            s[0][1] + s[1][1] + s[2][1] == three  or \
            s[0][2] + s[1][2] + s[2][2] == three  or \
            s[0][0] + s[1][1] + s[2][2] == three  or \
            s[0][2] + s[1][1] + s[2][0] == three :
            return True

        return False

    def _is_draw(self):
        if not np.prod(self.state) == 0:
            """ 総積 """
            return True

        return False 

