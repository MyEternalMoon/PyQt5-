colordic = {'white':True,'black':False}

class board:
    def __init__(self,length):
        self._length = int(length)
        self.lastStep = None
        self._board = []
        self.working = True
        self.steps = 0
        self.winner = None
        for i in range(length+1):
            line = [None]*(length+1)
            self._board.append(line)

    def step(self, color, position):
        if self.working is False:
            raise EOFError('The game is over!')
        self.x, self.y = position[0], position[1]
        if any([self.x > self._length, self.y > self._length]):
            raise ValueError('Beyond the bondary.')
        if self._board[self.x][self.y] is not None:
            raise ValueError('This position was ocuppied!')
        else:
            self._board[self.x][self.y] = colordic[color]
            self.steps += 1
        self.lastStep = (self.x, self.y)

    def regret(self):
        if self.lastStep is None:
            raise ValueError
        else:
            self._board[self.lastStep[0]][self.lastStep[1]] == None
            self.steps -= 1
            self.lastStep = None

    def __repr__(self):
        return "This is a board is %d*%d with %d step(s)."%(self._length,self._length,self.steps)

    def checkX(self):
        for i in range(self._length):
            cur = None
            cnt = 0
            for j in range(self._length):
                if self._board[i][j] is not None:
                    if self._board[i][j] == cur:
                        cnt += 1
                    else:
                        cnt = 1
                else:
                    cnt = 0
                cur = self._board[i][j]
                if cnt >= 5:
                    return (True, cur)
        else:
            return (False, None)

    def checkY(self):
        for i in range(self._length):
            cur = None
            cnt = 0
            for j in range(self._length):
                if self._board[j][i] is not None:
                    if self._board[j][i] == cur:
                        cnt += 1
                    else:
                        cnt = 1
                else:
                    cnt = 0
                cur = self._board[j][i]
                if cnt >= 5:
                    return (True, cur)
        else:
            return (False, None)

    def checkXY(self):
        for i in range(self._length-4):
            cur = None
            cnt = 0
            for j in range(self._length-i):
                if self._board[j][i+j] is not None:
                    if self._board[j][i+j] == cur:
                        cnt += 1
                    else:
                        cnt = 1
                else:
                    cnt = 0
                cur = self._board[j][i+j]
                if cnt >= 5:
                    return (True, cur)

        for i in range(self._length-4):
            cur = None
            cnt = 0
            for j in range(self._length-i):
                if self._board[i+j][j] is not None:
                    if self._board[i+j][j] == cur:
                        cnt += 1
                    else:
                        cnt = 1
                else:
                    cnt = 0
                cur = self._board[i+j][j]
                if cnt >= 5:
                    return (True, cur)
        else:
            return (False, None)

    def checkN_XY(self):
        for i in range(self._length-4):
            cur = None
            cnt = 0
            for j in range(self._length-i):
                if self._board[j][self._length-i-j] is not None:
                    if self._board[j][self._length-i-j] == cur:
                        cnt += 1
                    else:
                        cnt = 1
                else:
                    cnt = 0
                cur = self._board[j][self._length-i-j]
                if cnt >= 5:
                    return (True, cur)

        for i in range(self._length-4):
            cur = None
            cnt =0
            for j in range(self._length-i):
                if self._board[i+j][self._length-j] is not None:
                    if self._board[i+j][self._length-j] == cur:
                        cnt += 1
                    else:
                        cnt = 1
                else:
                    cnt = 0
                cur = self._board[i+j][self._length-j]
                if cnt >= 5:
                    return (True, cur)
        else:
            return (False, None)

    def Transversal(self):
        '''
        每一次下棋，都触发transversal
        从四个方向检查是否五子连珠
        若无则返回None，有则返回True白子，False黑子
        :return:
        '''

        x = self.checkX()
        if x[0]:
            return x[1]
        y = self.checkY()
        if y[0]:
            return y[1]
        P = self.checkXY()
        if P[0]:
            return P[1]
        N = self.checkN_XY()
        if N[0]:
            return N[1]
        return None

    def setWinner(self):
        self.winner = self.Transversal()
        if self.winner is not None:
            self.lastStep = None
