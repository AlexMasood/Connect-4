import numpy as np
import math
class Board:
    
    def __init__(self,row = 6,col = 7,winNum = 4):
        self.board = np.zeros((row,col),dtype=int)
        
        self.col = col
        self.row = row
        self.winNum = winNum
        self.boardHash = None
        self.isEnd = False
        self.singleMoveDict = {}
        self.solutionSet = {15, 30, 60, 120, 
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
            34630287360, 69260574720, 138521149440, 277042298880, 554084597760, 1108169195520, 2216338391040}
        self.populateSingleMoveDict()
        
        

    def getBoard(self):
        return self.board

    def printBoard(self):
        print(self.board)
        
    def populateSingleMoveDict(self):
        for row in range(0,self.row):
            for col in range(0,self.col):
                self.singleMoveDict[(row,col)] = int(math.pow(2,((7*(5-row))+(6 - col)))) 
    """
    Creates a hash of the current board returns board hash
    """
    def getHash(self,boardTuple):
        self.boardHash = tuple(boardTuple)# str(self.board.ravel())
        return self.boardHash
    
    """
    resets all dates for training
    """
    def reset(self):
        self.board = np.zeros((self.row,self.col),dtype=int)
        self.boardHash = None
        self.isEnd = False
    """
    input  row number int, column number int, and current player int
    sets the move to the lowest row in the column
    """
    def move(self,colNum,player,playerBoardNum):
        return self.gravity(self.getBoard(),colNum,player,playerBoardNum)
        

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
    def gravity(self,board, colNum, player,playerBoardNum):
        floor = self.row -1
        while (board[floor][colNum]!=0):
            floor-=1        
        
        board[floor][colNum] = player
        return  (playerBoardNum|self.singleMoveDict.get((floor,colNum)))
        


    """
    input of a board
    checks the top of each column, returning the list of empty space indexes
    """
    def getRemainingMoves(self,board):
        remainingMoves = set()
        for col in range(0,len(board[0])):
            if(board[0][col] == 0):
                remainingMoves.add(col)
        return remainingMoves
    
    """
    Check and returns how many spaces are remaining
    """
    def openSpaces(self):
        return np.count_nonzero(self.board == 0)
    
    """
    converts the board to a binary number based on the current players moves,
    uses a binary and operation on the board number and a precalculated list of winning solutions
    returns true if board is solved, false otherwise.
    """
    def binarySolver(self, board, player):
        tempBoard = board.copy()
        for row in tempBoard:
            for index in range(0,len(row)):
                if (row[index] != player):
                    row[index] = 0
                if (row[index] == 2):
                    row[index] = 1
    
        singleArrayBoard = tempBoard.ravel()
        boardInt = int("0b"+''.join(map(str, singleArrayBoard)),2)

        for ans in self.solutionSet:
            if(boardInt&ans == ans):
                return True
        return False
    
    def binaryCheck(self,boardInt):
        for ans in self.solutionSet:
            if(boardInt&ans == ans):
                return True
        return False

#A = np.arange(4).reshape((2,2))
#print(A)
#print(np.flip(A,1))