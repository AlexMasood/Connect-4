import random
import numpy as np
import pickle
"""
Implementation of reinforcement AI based on code created by MJeremy2017
https://github.com/MJeremy2017/reinforcement-learning-implementation/blob/master/TicTacToe/tic-tac-toe.ipynb
"""

class AI:
    def __init__(self, name, expRate = 0.3):
        self.name = name
        self.states = []
        self.lr = 0.2
        self.expRate = expRate
        self.decayGamma = 0.9
        self.statesValues = {}
    
    def getName(self):
        return self.name
    
    """
    takes list of positions, the numpy array of the current board, and the player as inputs.
    random move generated if random uniform number is below expRate
    each next potential legal move has its board created, hashed, and checked if in dictionary,If in dictionary value is set to value stored in the dictionary
    largest value is selected as its action 
    """
    def chooseAction(self, positions, currentBoardObj, symbol,boardTuple):
        #Element of randomness to help the AI explore new positions
        if (np.random.uniform(0,1) <= self.expRate):
            #idx = np.random.choice(len(positions))
           action = random.choice(tuple(positions))
        else:
            currentBoard = currentBoardObj.getBoard()
            valueMax = -999
            foundState = True
            for p in positions:
                nextBoard = currentBoard.copy()
                boardTupleCopy = boardTuple.copy()
                boardTupleCopy[symbol-1] = currentBoardObj.gravity(nextBoard,p,symbol,boardTupleCopy[symbol-1])
                if (self.statesValues.get(tuple(boardTupleCopy)) is None):
                    value = 0
                else:
                    value = self.statesValues.get(tuple(boardTupleCopy))
                    foundState = False
                if(value >= valueMax):
                    valueMax = value
                    action = p
            if (foundState):
                print("random move")
                action = random.choice(tuple(positions))
        return action
    
    def addState(self,state):
        self.states.append(state)

    """
    input of reward
    at the end of the game backpropagate update states value
    """
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.statesValues.get(st) is None:
                self.statesValues[st] = 0
            self.statesValues[st] += self.lr*(self.decayGamma*reward - self.statesValues[st])
            reward = self.statesValues[st]


    def reset(self):
        self.states = []

    """
    Returns a string for the filename consisting of policy followed by row, col,win number, and position of AI
    """
    def fileNaming(self, row, col,winNum,playerPos):
        return "policy_"+str(row)+"_by_"+str(col)+"_"+str(winNum)+"_"+str(playerPos)


    def savePolicy(self, row, col, winNum):
        fw = open(self.fileNaming(row, col, winNum, self.name),'wb')
        pickle.dump(self.statesValues, fw)
        fw.close()
    
    def loadPolicy(self,row, col, winNum, user):
        fr = open(self.fileNaming(row, col, winNum, user),'rb')
        self.statesValues = pickle.load(fr)
        fr.close()

    """
    Input of board object And player
    retrieves possible moves selects a random move plays move
    no validation needed since any remaining move is a legal move
    """
    def randomMove(self, board, player):
        moveList = board.getRemainingMoves(board.getBoard())
        moveCol = random.choice(moveList)
        board.move(moveCol,player)
        board.printBoard()
        