import sys
import math

class Ball:
    def __init__(self, r=10, pos=[100,100], v=[5,5], a=[0,0]):
        self.r = r
        self.pos = pos # position
        self.v = v   # verocit
        self.a = a   # acceleration
        self.move_unit = 1

    def getPosition(self):
        return self.pos

    # pos: [x,y]
    def setPosition(self, pos):
        self.pos = pos

    def getVerocity(self):
        return self.v

    # v: [vx,vy]
    def setVerocity(self, v):
        self.v = v

    def getAcceleration(self):
        return self.a

    # a: [ax,ay]
    def setAcceleration(self, a):
        self.a = a

    # calclate next position 
    # Base: x = x + tu*vx, y = y + tu*vy, tu is timue unit.
    def calcNextPosition(self):
        x = self.pos[0] + self.move_unit*self.v[0]
        y = self.pos[1] + self.move_unit*self.v[1]
        return [x,y]

    def calcNextVerocity(self, tu=1):
        vx = self.v[0] + self.move_unit*self.a[0]
        vy = self.v[1] + self.move_unit*self.a[1]
        return [vx,vy]

    def reflect(self, dir=""):
        if dir == "x":
            self.v[0] = -self.v[0]
        elif dir == "y":
            self.v[1] = -self.v[1]
        elif dir == "xy":
            self.v[0] = -self.v[0]
            self.v[1] = -self.v[1]
        elif dir == "":
            return
        else:
            print >> sys.stderr, "WARNING(Ball.py): Unknown reflect direction is input."

    def dump(self):
        print "----------------------------------------"
        print "pos:%f\t%f" % (self.pos[0], self.pos[1])
        print "  v:%f\t%f" % (self.v[0], self.v[1])
        print "  a:%f\t%f" % (self.a[0], self.a[1])

if __name__ == "__main__":
    ball = Ball()
    ball.setPosition( [0,0] )
    ball.setVerocity( [1,1] )
    t = 0
    while( t<100 ):
        ball.setPosition( ball.calcNextPosition() )
        if (ball.getPosition()[0] > 20.):
            ball.reflect("x")
        elif (ball.getPosition()[0] < -20.):
            ball.reflect("x")
        if (ball.getPosition()[1] > 20.):
            ball.reflect("y")
        elif (ball.getPosition()[1] < -20.):
            ball.reflect("y")

        if t % 10 == 0:
            a = ball.getAcceleration()
            ball.setAcceleration( [a[0]+0.1, a[1]+0.2] )
        
        ball.setVerocity( ball.calcNextVerocity() )
        ball.dump()
        t += 1
