# cheat AI
class MyPlayer():
    def __init__(self,board_size, paddle_size, ball_r):
        self.board_w , self.board_h= board_size
        self.paddle_w, self.paddle_h = paddle_size
        self.ball_r = ball_r
        
    def getNextAction(self, ball, paddle):
        ball_x, ball_y = ball.getPosition()
        ball_vx, ball_vy = ball.getVerocity()
        paddle_x = paddle.getX()
        #if ball_y >= (self.board_h - self.paddle_h - self.ball_r):
        #        if ball_y >= 150 and ball_vy > 0:
        del_x = ball_x - paddle_x
        return del_x        
