import random

import pygame
from pygame.locals import *
import Paddle
import Ball
import Block
import Stage
import MyPlayer

class Breakout:
    def __init__(self, board_w=400, board_h=700,\
                 paddle_w=80, paddle_h=20, ball_r=10, ball_v=5):
        self.board_w = board_w
        self.board_h = board_h
        self.paddle_w = paddle_w
        self.paddle_w_2 = paddle_w/2 # half width
        self.paddle_h = paddle_h
        self.paddle_top = self.board_h - paddle_h
        self.paddle = Paddle.Paddle(board_w/2, paddle_w)
        self.ball_r = ball_r
        self.ball_pos = [self.board_w/2, self.board_h/2]
        self.ball_v = [ball_v*random.choice([-1,1]),ball_v*random.choice([-1,1])]
        self.ball_a = [0,0]
        self.ball = Ball.Ball(self.ball_r, self.ball_pos, self.ball_v, self.ball_a)
        self.stage = Stage.Stage()
        self.new_broken_block = None
        self.score = 0
        self.result = None
        self.player = None

    def getStage(self):
        return self.stage

    def movePaddle(self, dir_and_width):
        cur_x = self.paddle.getX()
        x = cur_x + dir_and_width
        if x - self.paddle_w_2 <= 0:
            self.paddle.setX(self.paddle_w_2)
        elif x + self.paddle_w_2 >= self.board_w:
            self.paddle.setX(self.board_w - self.paddle_w_2)
        else:
            self.paddle.setX(x)

    def updateBallPosition(self):
        self.ball_pos = self.ball.calcNextPosition()
        if self.ball_pos[0] <= 0 or self.ball_pos[0] >= self.board_w:
            self.ball.reflect("x")
        if self.ball_pos[1] <= 0:
            self.ball.reflect("y")
        if self.ball_pos[1] >= self.board_h:
            self.result = "GAMEOVER"
            return [self.score, self.result]

        # hit check between ball and paddle
        self.HitCheckForBallAndPaddle()
        ret = self.HitCheckForBallAndBlocks()
        if ret == "CLEAR":
            return [self.score, self.result]
        self.ball.setPosition(self.ball_pos)
        
        return [-1, "GAMERUNNING"]

    def HitCheckForBallAndPaddle(self):
        ball_x, ball_y = self.ball_pos[0], self.ball_pos[1]
        if ball_y >= self.paddle_top:
            paddle_pos   = self.paddle.getX()
            paddle_left  = paddle_pos - self.paddle_w_2
            paddle_right = paddle_pos + self.paddle_w_2
            if ball_x > paddle_left and ball_x < paddle_right:
                self.ball.reflect("y")
            elif ball_x == paddle_left or ball_x == paddle_right:
                self.ball.reflect("xy")


    def HitCheckForBallAndBlocks(self):
        self.new_broken_block = None
        blocks = self.stage.getBlocks()
        broken_flgs = self.stage.getBrokenFlgs()
        for i, broken_flg in enumerate(broken_flgs):
            if not broken_flg:
                ball_r = self.ball_r
                ball_x, ball_y = self.ball_pos[0], self.ball_pos[1]
                ball_v = self.ball.getVerocity()
                block = blocks[i]
                block_pos = block.getPosition()
                block_size = block.getSize()
                block_left = block_pos[0] - block_size[0]/2
                block_right = block_pos[0] + block_size[0]/2
                block_top = block_pos[1] - block_size[1]/2
                block_bottom = block_pos[1] + block_size[1]/2
                hit_flg = False
                # check top hit
                if ball_x < block_right and ball_x > block_left and\
                   ball_y + ball_r > block_top and ball_y + ball_r < block_bottom:
                    self.ball.reflect("y")
                    #print "hit at TOP",
                    hit_flg = True
                # check bottom hit
                elif ball_x < block_right and ball_x > block_left and\
                   ball_y - ball_r > block_top and ball_y - ball_r < block_bottom:
                    self.ball.reflect("y")
                    #print "hit at BOTTOM",
                    hit_flg = True
                # check left hit
                elif ball_x + ball_r < block_right and ball_x + ball_r > block_left and\
                   ball_y > block_top and ball_y < block_bottom:
                    self.ball.reflect("x")
                    #print "hit at LEFT",
                    hit_flg = True
                # check right hit
                elif ball_x - ball_r < block_right and ball_x - ball_r > block_left and\
                   ball_y > block_top and ball_y < block_bottom:
                    self.ball.reflect("x")
                    #print "hit at RIGHT",
                    hit_flg = True

                if hit_flg:
                    self.stage.setBrokenFlg(True, i)
                    self.new_broken_block = i
                    self.score += 1
                    if self.stage.checkClear():
                        self.result = "CLEAR"
                        return self.result
                    #print ",Block at [%d,%d], ball [%d, %d]"\
                        #% (block_pos[0], block_pos[1], ball_x, ball_y)

    def addPlayer(self, player):
        self.player = player

    def run(self):
        return 0
        

