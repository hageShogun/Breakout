class Block:
    def __init__(self, pos, width, height):
        self.pos = pos # [x,y]
        self.width = width
        self.height = height
        self.broken_flg = False

    def getPosition(self):
        return self.pos

    def getWidth(self):
        return self.width

    def getheight(self):
        return self.heiht

    def getSize(self):
        return [self.width, self.height]

    def setBrokenFlg(self, flg):
        self.broken_flg = flg

    def getBrokenFlg(self):
        return self.broken_flg

    def dump(self):
        print "-----------"
        print "pos", self.pos
        print "width", self.width
        print "height", self.height
        print "broken_flg", self.broken_flg
