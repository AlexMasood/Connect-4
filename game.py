from board import Board as b
from ai import AI
from player import Player
import numpy as np
import time
"""
Implementation of reinforcement AI based on code created by MJeremy2017
https://github.com/MJeremy2017/reinforcement-learning-implementation/blob/master/TicTacToe/tic-tac-toe.ipynb
"""
class Game:
    def __init__(self, p1, p2):
        self.beingPlayed = True
        self.p1 = p1
        self.p2 = p2
    
    """
    Input of the current board object
    Feed both AI based on winner or draw
    """
    def giveReward(self,boardObj):
        if(boardObj.binarySolver(boardObj.getBoard(),1,joint = True)):
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif(boardObj.binarySolver(boardObj.getBoard(),2, joint = True)):
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)
    
    """
    Input board row, board column, win number, and of how many rounds will be played
    Finds legal moves, decide the best course of action adds states as a board hash
    Checks board win condition, assigns reward and resets if game is over
    repeats for the second AI

    """
    def aIVsAI(self, row, col, winNum, rounds = 100):
        for i in range(rounds):
            #if(i%1000 == 0):
            #    print("rounds {}".format(i))
            boardObj = b(row, col, winNum)
            p1Board  = np.zeros((row,col),dtype=int)
            p2Board  = np.zeros((row,col),dtype=int)
            while (self.beingPlayed):
                positions = boardObj.getRemainingMoves(boardObj.getBoard())
                p1Action = self.p1.chooseAction(positions, boardObj, 1)
                boardObj.move(p1Action,1,p1Board)
                boardHash = boardObj.getHash()
                self.p1.addState(boardHash)

                if((boardObj.binarySolver(p1Board,1)) or not(boardObj.getRemainingMoves(boardObj.getBoard()))):
                    self.giveReward(boardObj)
                    self.p1.reset()
                    self.p2.reset()
                    boardObj.reset()
                    break
                else:
                    positions = boardObj.getRemainingMoves(boardObj.getBoard())
                    p2Action = self.p2.chooseAction(positions, boardObj, 2)
                    boardObj.move(p2Action,2,p2Board)
                    boardHash = boardObj.getHash()
                    self.p2.addState(boardHash)

                    if((boardObj.binarySolver(p2Board,2)) or not(boardObj.getRemainingMoves(boardObj.getBoard()))):
                        self.giveReward(boardObj)
                        self.p1.reset()
                        self.p2.reset()
                        boardObj.reset()
                        break
    """
    Inputs of board rows, board columns, and win number
    Inputs of row column and win number
    Single game of tic-tac-toe with no rewards on win or draw
    Use function computerFirstGame or humanFirstGame to choose who is first
    """
    def humanVsAI(self, row, col, winNum):
        boardObj = b(row, col, winNum)
        boardObj.printBoard()
        while (self.beingPlayed):
            positions = boardObj.getRemainingMoves(boardObj.getBoard())
            p1Action = self.p1.chooseAction(positions, boardObj, 1)
            boardObj.move(p1Action,1)
            boardHash = boardObj.getHash()
            self.p1.addState(boardHash)
            boardObj.printBoard()

            if(boardObj.binarySolver(boardObj.getBoard(),1)):
                print(self.p1.getName() + " has won")
                boardObj.reset()
                break
            elif not(boardObj.getRemainingMoves(boardObj.getBoard())):
                print("draw")
                boardObj.reset()
                break
            else:
                positions = boardObj.getRemainingMoves(boardObj.getBoard())
                p2Action = self.p2.chooseAction(positions, boardObj, 2)
                boardObj.move(p2Action,2)
                boardHash = boardObj.getHash()
                self.p2.addState(boardHash)
                boardObj.printBoard()
                if(boardObj.binarySolver(boardObj.getBoard(),2)):
                    print(self.p2.getName() + " has won")
                    boardObj.reset()
                    break

    """
    Inputs of board rows, board columns, and win number
    whilst the game is being played,
    player 1 move
    check win condition
    else check draw condition (turn>8 without a win)
    else play player 2
    check win condition
    """
    def humanVsHuman(self, rowLen, colLen, winNum):
        boardObj = b(rowLen, colLen, winNum)
        boardObj.printBoard()
        while (self.beingPlayed):
            positions = boardObj.getRemainingMoves(boardObj.getBoard())
            p1Action = self.p1.chooseAction(positions, boardObj, 1)
            boardObj.move(p1Action,1)
            boardObj.printBoard()   
            if(boardObj.checkBoard(boardObj.getBoard(),1)):
                print(self.p1.getName() + " has won")
                self.beingPlayed = False
            else:
                if(not boardObj.getRemainingMoves(boardObj.getBoard())):
                    print("Draw")
                    self.beingPlayed = False
                else:
                    positions = boardObj.getRemainingMoves(boardObj.getBoard())
                    p2Action = self.p2.chooseAction(positions, boardObj, 2)
                    boardObj.move(p2Action,2)
                    boardObj.printBoard()
                    if(boardObj.checkBoard(boardObj.getBoard(),2)):
                        print(self.p2.getName() + " has won")
                        self.beingPlayed = False


"""
Inputs of repeated training, board rows, board columns, and win number
Sets up, trains, and saves the AI
"""
def trainAI(repitions, row,col,winNum, continueAITraining = False, savePolicy = True):
    p1 = AI("p1")
    p2 = AI("p2")
    if(continueAITraining):
        print("loaded in previous AI data")
        p1.loadPolicy(row, col, winNum, "p1")
        p2.loadPolicy(row, col, winNum, "p2")
    st = Game(p1, p2)
    print("training...")
    st.aIVsAI(row,col, winNum, repitions)
    if(savePolicy):
        p1.savePolicy(row,col,winNum)
        p2.savePolicy(row,col,winNum)

"""
Inputs of board rows, board columns, and win number
Loads computers AI is first player
"""  
def computerFirstGame(row,col,winNum):
    p1 = AI("computer", expRate = 0)
    p2 = Player("Human")
    p1.loadPolicy(row, col, winNum, "p1")

    st = Game(p1,p2)
    st.humanVsAI(row,col, winNum)

"""
Inputs of board rows, board columns, and win number
Loads computers AI second player
"""
def humanFirstGame(row,col,winNum):
    p1 = Player("Human")
    p2 = AI("computer", expRate = 0)
    p2.loadPolicy(row, col, winNum, "p2")

    st = Game(p1,p2)
    st.humanVsAI(row,col, winNum) 
"""
Inputs of board rows, board columns, and win number
"""
def humanVsHumanGame(row,col,winNum):
    p1 = Player("Human1")
    p2 = Player("Human2")
    st = Game(p1,p2)
    st.humanVsHuman(row,col, winNum)

#trainAI(100000,6,7,4)
#computerFirstGame(6,7,4)
#humanVsHumanGame(10,10,5)

start = time.time()
trainAI(1000,6,7,4,continueAITraining=False, savePolicy=False)
#computerFirstGame(6,7,4)
end = time.time()
print(end - start)