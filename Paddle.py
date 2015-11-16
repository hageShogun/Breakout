import sys

class Paddle:
    def __init__(self, x=100, width=10):
        self.x     = x     # paddle middle position
        self.width = width

    def setWidth(self, width):
        self.width = width
    def getWidth(self):
        return self.width

    def setX(self, x):
        self.x = x
    def getX(self):
        return self.x


    def dump(self):
        print "paddle_x:%f" % self.x

if __name__ == "__main__":
    paddle = Paddle()

