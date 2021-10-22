import numpy as np
class Board:
    
    def __init__(self,row = 6,col = 7,winNum = 4):
        self.board = np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        
        self.col = col
        self.row = row
        self.winNum = winNum
        self.boardHash = None
        self.isEnd = False
        self.solutionArray = np.array([15, 30, 60, 120, 
            1920, 3840, 7680, 15360, 
            245760, 491520, 983040, 1966080,
            31457280, 62914560, 125829120, 251658240,
            4026531840, 8053063680, 16106127360, 32212254720,
            515396075520, 1030792151040, 2061584302080, 4123168604160,
            17043520, 2181570560, 279241031680,
            8521760, 1090785280, 139620515840,
            4260880, 545392640, 69810257920,
            2130440, 272696320, 34905128960,
            16843009, 33686018, 67372036, 134744072,
            2155905152, 4311810304, 8623620608, 17247241216,
            275955859456, 551911718912, 1103823437824, 2207646875648,
            2113665, 4227330, 8454660, 16909320, 33818640, 67637280, 135274560,
            270549120, 541098240, 1082196480, 2164392960, 4328785920, 8657571840, 17315143680,
            34630287360, 69260574720, 138521149440, 277042298880, 554084597760, 1108169195520, 2216338391040])
        

    def getBoard(self):
        return self.board

    """
    Creates a hash of the current board returns board hash
    """
    def getHash(self):
        self.boardHash = str(self.board.reshape(self.row*self.col))
        return self.boardHash
    
    """
    resets all dates for training
    """
    def reset(self):
        self.board = np.zeros((self.row,self.col))
        self.boardHash = None
        self.isEnd = False
    """
    input of the board x by y numpy array, player int, row number int, column number int
    checks if move is legal and sets the new board as its output
    returns 0 if check fails
    """
    def move(self,colNum,player):
        if(self.checkMove(colNum)):
            self.gravity(self.getBoard(),colNum,player)
            return True
        return False

    """
    input of column int
    checks if placing a move in the given coordinates are legal
    returns true if legal, false if not
    """
    def checkMove(self,colNum):
        if(self.getBoard()[0][colNum] == 0):
            return True
        return False
    
    """
    Inputs of column number and player
    checks in the selected column if the floor is not an empty space
    Raises the floor when there is no empty space
    sets the players counter once a space has been found
    """
    def gravity(self,board, colNum, player):
        floor = self.row -1
        while (board[floor][colNum]!=0):
            floor-=1
        board[floor][colNum] = player

    def nextWinMove(self,board,player):
        moves = self.getRemainingMoves(board)
        for move in moves:
            possibleMove = board.copy()
            self.gravity(possibleMove,move,player)
            if(self.bitSolver(possibleMove, player)):
                return True, move
        return False, self.col #this is out of the range


    def printBoard(self):
        print(self.board)
        
    """
    Input of any length row and player counter
    Creates a copy of the row to allow editing
    for each element the element is set to 0 if it isnt the players move, this is to ignore empty coords and the other players moves
    checks if the list contains the amount required to win of the players move
    returns true if check passes, else false
    """
    def checkRow(self,row, player):
        for index in range(0,len(row)):
            if (row[index] != player):
                row[index] = 0
        for x in range((len(row)-self.winNum+1)):
            if (all(row[x:self.winNum+x])):
                return True
        else:
            return False
    
    """
    player character
    creates a copy of the board
    loops over each row to check if win condition has been met 
    rotates the board by 90 degrees and repeates check
    Creates a list of all diagonal combinations
    does a row check on all diagonal combinations
    returns true if win condition has been met
    """
    def checkBoard(self,board,player):
        boardCopy = np.copy(board)
        for x in range(0,2):
            for row in boardCopy:
                if (self.checkRow(row,player)):
                    self.isEnd = True
                    return True
            boardCopy = np.rot90(boardCopy)
        diags = [boardCopy[::-1,:].diagonal(i).copy() for i in range(-boardCopy.shape[0]+1,boardCopy.shape[1])]
        diags.extend(boardCopy.diagonal(i).copy() for i in range(boardCopy.shape[1]-1,-boardCopy.shape[0],-1))
        
        for row in diags:
            if(len(row)>=self.winNum):
                if (self.checkRow(row,player)):
                    self.isEnd = True
                    return True
        
    """
    Checks and returns remaining possible moves
    """
    def getRemainingMoves(self,board):
        remainingMoves = []
        for col in range(0,len(board[0])):
            if(board[0][col] == 0):
                remainingMoves.append(col)
        return remainingMoves
    
    """
    Check and returns how many spaces are remaining
    """
    def openSpaces(self):
        return np.count_nonzero(self.board == 0)
    
    def bitSolver(self, board, player):
        tempBoard = board.copy()
        for row in tempBoard:
            for index in range(0,len(row)):

                if (row[index] != player):
                    row[index] = 0
                if (row[index] == 2):
                    row[index] = 1
        singleArrayBoard = tempBoard.ravel()
        boardInt = int("0b"+''.join(map(str, singleArrayBoard)),2)
        for ans in self.solutionArray:
            if(boardInt&ans == ans):
                return True
        return False

# solutionArray = np.array([15, 30, 60, 120, 
#     1920, 3840, 7680, 15360, 
#     245760, 491520, 983040, 1966080,
#     31457280, 62914560, 125829120, 251658240,
#     4026531840, 8053063680, 16106127360, 32212254720,
#     515396075520, 1030792151040, 2061584302080, 4123168604160,
#     17043520, 2181570560, 279241031680,
#     8521760, 1090785280, 139620515840,
#     4260880, 545392640, 69810257920,
#     2130440, 272696320, 34905128960,
#     16843009, 33686018, 67372036, 134744072,
#     2155905152, 4311810304, 8623620608, 17247241216,
#     275955859456, 551911718912, 1103823437824, 2207646875648])

#int('0b1010', 2)
#([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,1,0,0,0],[0,0,1,0,0,0,0],[0,1,0,0,0,0,0],[1,0,0,0,0,0,0]])
# a = np.array([[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,1],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
# print(a)
# a = a.ravel()
# b = int("0b"+''.join(map(str, a)),2)
# print(b)
#  for ans in solutionArray:
#      if (b&ans == ans):
#          print("found it")
        
    