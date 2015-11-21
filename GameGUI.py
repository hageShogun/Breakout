import sys
import pygame
from pygame.locals import *

import Breakout
import Paddle
import Ball
import Block
import Stage
import MyPlayer

# color pallet
col_paddle= (0,51,204)
col_ball  = (204,51,51)
col_block  = (0,255,51)
col_bkscreen  = (0,0,51)
col_font= (255,255,204)
col_font_msg= (255,51,51)

class GameGUI(Breakout.Breakout):
    def __init__(self, game_params):
        Breakout.Breakout.__init__(self,game_params["SCR_W"], game_params["SCR_H"],\
                                   game_params["paddle_w"], game_params["paddle_h"],\
                                   game_params["ball_r"], game_params["ball_v"])
        self.screen     = None
        self.font       = None
        self.clock      = None
        self.score_pos  = None
        self.score_rect = None
        self.initGame()

    def initGame(self):
        print "Initializing game...",
        pygame.init()
        self.genDemoStage()
        self.screen = pygame.display.set_mode((self.board_w, self.board_h))
        pygame.display.set_caption("BREAKOUT")
        self.font = pygame.font.Font(None, 50)
        self.font_msg = pygame.font.Font(None, 150)
        self.clock = pygame.time.Clock()
        # for score position calculation
        score_text = self.font.render("SCORE:000:", True, col_font)
        score_w, score_h = score_text.get_size()
        self.score_pos = [(self.board_w - score_w), 0]
        self.score_rect = Rect(self.score_pos[0], self.score_pos[1], score_w, score_h)
        print "finished succecssfully."


    def initDraw(self):
        self.screen.fill(col_bkscreen)
        self.drawScore()
        self.drawBall()
        blocks = self.getStage().getBlocks()
        self.drawPaddle()
        self.drawBlocks()
        pygame.display.update()

    def drawMssage(self, msg=""):
        self.screen.fill(col_bkscreen)
        text = self.font_msg.render(msg, True, col_font_msg)
        text_w, text_h = text.get_size()
        self.screen.blit(text, (self.board_w/2-text_w/2, self.board_h/2-text_h/2))
        pygame.display.update()

    def drawScore(self, dirty_rects=[]):
        score_text = self.font.render("SCORE:%d" % self.score, True, col_font)
        self.screen.blit(score_text, self.score_pos)
        dirty_rects.append(self.score_rect)

    def drawPaddle(self):
        paddle_left = self.paddle.getX() - self.paddle_w_2
        rect = Rect(paddle_left, self.paddle_top, self.paddle_w, self.paddle_h)
        pygame.draw.rect(self.screen, col_paddle,rect)


    def drawBall(self):
        pygame.draw.circle(self.screen, col_ball,\
                           (self.ball_pos[0],self.ball_pos[1]),self.ball_r)
        rect = Rect(self.ball_pos[0]-self.ball_r, self.ball_pos[1]-self.ball_r,\
                    2*self.ball_r, 2*self.ball_r)

    def drawBlocks(self):
        for block in self.stage.getBlocks():
            if not block.getBrokenFlg():
                block_pos, block_size = block.getPosition(), block.getSize()
                block_left = block_pos[0] - block_size[0]/2
                block_top = block_pos[1] - block_size[1]/2
                rect = Rect(block_left, block_top, block_size[0], block_size[1])
                pygame.draw.rect(self.screen, col_block,rect)

    def deleteBlocks(self, new_broken_blocks, dirty_rects=[]):
        for i in new_broken_blocks:
            self.deleteBlock(i, dirty_rects)

    def deleteBlock(self, i, dirty_rects=[]):
        block = self.stage.getBlocks()[i]
        block_pos = block.getPosition()
        block_size = block.getSize()
        block_left = block_pos[0] - block_size[0]/2
        block_top = block_pos[1] - block_size[1]/2
        rect = Rect(block_left,block_top,block_size[0],block_size[1])
        pygame.draw.rect(self.screen, col_bkscreen, rect)
        dirty_rects.append(rect)

    def getActionFromKeyboard(self, dirty_rects):
        move_unit = 10
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            #print "LEFT is pushed...",
            #print "x=%d" % game.paddle.getX()
            self.movePaddle(-1*move_unit, dirty_rects)

        if pressed_keys[K_RIGHT]:
            #print "RIGHT is pushed...",
            #print "x=%d" % game.paddle.getX()
            self.movePaddle(1*move_unit, dirty_rects)


    # override
    def movePaddle(self, dir, dirty_rects):
        # save old position
        paddle_left = self.paddle.getX() - game.paddle_w_2
        rect = Rect(paddle_left, self.paddle_top, self.paddle_w, self.paddle_h)
        dirty_rects.append(rect)

        # actually move 
        Breakout.Breakout.movePaddle(self, dir)

        # save new position
        paddle_left = self.paddle.getX() - game.paddle_w_2
        rect = Rect(paddle_left, self.paddle_top, self.paddle_w, self.paddle_h)
        dirty_rects.append(rect)


    def updateBall(self, dirty_rects=[]):
        ball_r = self.ball_r
        ball_pos = self.ball_pos
        dirty_rects.append(Rect(ball_pos[0]-ball_r, ball_pos[1]-ball_r, 2*ball_r, 2*ball_r))
        ret = self.updateBallPosition()
        ball_pos = self.ball_pos
        dirty_rects.append(Rect(ball_pos[0]-ball_r, ball_pos[1]-ball_r, 2*ball_r, 2*ball_r))
        return ret
      
    def run(self):
        while True:
            self.clock.tick(60) # 60 fps
            dirty_rects = []
            ###################
            # update object state
            self.getActionFromKeyboard(dirty_rects)
            if self.player is not None:
                action = self.player.getNextAction(self.ball, self.paddle)
                if action != 0:
                    self.movePaddle(action, dirty_rects)

            ret = self.updateBall(dirty_rects)
            if ret[1] == "GAMEOVER" or ret[1] == "CLEAR":
                break
            
            #############
            # drawing update
            self.screen.fill(col_bkscreen)
            self.drawScore(dirty_rects)
            self.drawBall()
            self.drawPaddle()
            if len(self.new_broken_blocks) != 0:
                print len(self.new_broken_blocks)
                self.deleteBlocks(self.new_broken_blocks, dirty_rects)
            self.drawBlocks()
            pygame.display.update(dirty_rects)

            # check fps
            #print self.clock.get_fps()

            ###################
            # event processing
            for event in pygame.event.get():
                if event.type == QUIT or\
                   (event.type==KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    quit()
                elif (event.type==KEYDOWN and event.key == K_RETURN):
                    self.reset()
                    self.initDraw()

# Simple Test
if __name__ == "__main__":  
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print "Usage: python %s <auto/manual>" % argvs[0]
        quit()
    
    # GAME PARAMETER
    game_params = {"SCR_W":600, "SCR_H":480,\
                   "paddle_w":80, "paddle_h":10,\
                   "ball_r": 5, "ball_v":6}
    game = GameGUI(game_params)
    game.initDraw()

    # Player
    if argvs[1] == "auto":
        player = MyPlayer.MyPlayer((game.board_w,game.board_h),\
                                   (game.paddle_w, game.paddle_h),\
                                   game.ball_r)
        game.addPlayer(player)

    # start game
    game.run()

    # finalize
    print game.result, "SCORE:%d" % game.score
    game.drawMssage(game.result)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or\
               (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                quit()
