#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

class Gomoku():

    def __init__(self, row=5, width=6):
        self.row = row
        self.width = width
        self.action_size = self.width * self.width
        self.board_edges = self._get_board_edges()
        """ search_directions: [-w-1, -w, -w+1, -1, 1, w-1, w, w+1] """     
        self.search_directions = self._get_search_directions() # ((0,1),(1,0),(1,1),(-1,1))

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
        self.player = -self.player

        if self._is_done(a):
            self.done = True
            self.reward = -1 # 打つ手がないので負け

        elif self._is_draw():
            self.done = True
            self.reward = 0

        else:
            pass
      
        return self.state, self.reward, self.done

    def get_legal_actions(self, state):
        state = np.array(state).reshape(-1)
        return np.where(state==0)[0]

    def show(self):
        print(self.s)

    def _pass(self):
        self.player = -self.player
        pass

    def _is_done(self, a):
        """ a: action """
       
        x1, x2 = a // self.width, a % self.width 
        player = self.state[x1][x2] # どちらの手番で勝ったか？
        directions = ((0,1),(1,0),(1,1),(-1,1))

        for dir in directions:
            counter = 1

            for sign in [+1, -1]:
                ite = 0
                while True:
                    ite += 1
                    tp = (x1 + ite * dir[0] * sign, x2 + ite * dir[1] * sign)
                    r, c = tp[0], tp[1]
                    if (r >= 0 and c >= 0 and r < self.width and c < self.width) and self.state[r][c] == player:
                        counter+= 1
                    else:
                        break

            if counter >= self.row:
                """ 勝った場合の処理 """
                self.done = True
                return True

        return False

    def _search(self, pos, direction, count):
        x1, x2 = (pos // self.width), (pos % self.width)

        if self.state[x1][x2] == self.player:
            count += 1
        else:
            return False

        if count == self.row:
            return True
        
        next_pos = pos + direction

        if next_pos in self.board_edges:
            return False

        if next_pos >= self.width * self.width:
            return False

        self._search(next_pos, direction, count)

    def _is_draw(self):
        if np.prod(self.state) != 0:
            """ 総積 """
            return True

        return False

    def _get_board_edges(self):

        edges = []
        w = self.width
        opposite_v = self.action_size - w

        for i in range(w):
            edges.append(i)
            edges.append(i + opposite_v)

            if (i * w) not in edges:
                edges.append(i * w)

            opposite_h = i * w + w - 1

            if (opposite_h) not in edges:
                edges.append(opposite_h)

        return edges

    def _get_search_directions(self):
        w = self.width
        return [1, w-1, w, w+1]
