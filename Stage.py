import Block

# TODO:
# broken_flgs shuld not be used since it is Double definition.
class Stage:
    def __init__(self):
        self.nblocks = None
        self.blocks = []
        self.broken_flgs = None
        self.broken_cnt = 0

    def init(self):
        self.nblocks = len(self.blocks)
        self.broken_flgs = [False] * self.nblocks

    def getNblocks(self):
        return self.nblocks

    def getBrokenCnt(self):
        return self.broken_cnt

    def getBlocks(self):
        return self.blocks

    def getBrokenFlgs(self):
        return self.broken_flgs

    def checkClear(self):
        if self.nblocks == self.broken_cnt:
            return True

    def addBlock(self, pos, width, height):
        self.blocks.append(Block.Block(pos, width, height))

    def setBrokenFlg(self, flg, i):
        self.broken_flgs[i] = flg
        self.blocks[i].setBrokenFlg(flg)
        self.broken_cnt += 1

    def reset(self):
        for block in self.blocks:
            block.setBrokenFlg(False)
        self.broken_flgs = [False] * self.nblocks
        self.broken_cnt = 0

    def dump(self):
        print "nblocks:", self.nblocks
        print "broken_flgs:", self.broken_flgs
        for block in self.blocks:
            block.dump()
    
    # 600x480 board is assumed.
    def genDemoStage(self):
        block_w , block_h = 38, 18
        pos0_x , pos0_y = 39, 50
        space = 2
        for i in range(0,14):
            for j in range(0,8):
                pos_x = pos0_x + i*(block_w + space)
                pos_y = pos0_y + j*(block_h + space)
                self.addBlock([pos_x,pos_y], block_w, block_h)
        self.init()

if __name__ == "__main__":
    stage = Stage()
    stage.genDemoStage()
    stage.dump()

