from pygame.constants import KEYDOWN
from board import Board as b
from ai import AI
from player import Player
import numpy as np
import pygame
import time
"""
Implementation of reinforcement AI based on code created by MJeremy2017
https://github.com/MJeremy2017/reinforcement-learning-implementation/blob/master/TicTacToe/tic-tac-toe.ipynb
"""
class Game:
    def __init__(self, p1, p2,row = 6, col = 7, pygame = True):
        self.beingPlayed = True
        self.p1 = p1
        self.p2 = p2
        self.pygame = pygame
        self.row = row
        self.col = col
        self.pixelSize = 100
    
    """
    Input of the current board object
    Feed both AI based on winner or draw
    """
    def giveReward(self,boardObj):
        if(boardObj.binarySolver(boardObj.getBoard(),1)):
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif(boardObj.binarySolver(boardObj.getBoard(),2)):
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
        boardObj = b(row, col, winNum)
        for i in range(rounds):
            if(i%100000 == 0):
                print("rounds {}".format(i))
            boardTuple = [0,0]
            while (self.beingPlayed):
                positions = boardObj.getRemainingMoves(boardObj.getBoard())
                p1Action = self.p1.chooseAction(positions, boardObj, 1, boardTuple)
                boardTuple[0] = boardObj.move(p1Action,1,boardTuple[0])
                boardHash = boardObj.getHash(boardTuple)
                self.p1.addState(boardHash)
                if((boardObj.binaryCheck(boardTuple[0])) or (len(boardObj.getRemainingMoves(boardObj.getBoard())) == 0)):
                    self.giveReward(boardObj)
                    self.p1.reset()
                    self.p2.reset()
                    boardObj.reset()
                    break
                else:
                    positions = boardObj.getRemainingMoves(boardObj.getBoard())
                    p2Action = self.p2.chooseAction(positions, boardObj, 2,boardTuple)
                    boardTuple[1] = boardObj.move(p2Action,2,boardTuple[1])
                    boardHash = boardObj.getHash(boardTuple)
                    self.p2.addState(boardHash)
                    if((boardObj.binaryCheck(boardTuple[1])) or (len(boardObj.getRemainingMoves(boardObj.getBoard())) == 0)):
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
        boardTuple = [0,0]
        boardObj.printBoard()
        while (self.beingPlayed):
            positions = boardObj.getRemainingMoves(boardObj.getBoard())
            p1Action = self.p1.chooseAction(positions, boardObj, 1, boardTuple)
            boardTuple[0] = boardObj.move(p1Action,1,boardTuple[0])
            boardHash = boardObj.getHash(boardTuple)
            self.p1.addState(boardHash)
            boardObj.printBoard()

            if(boardObj.binarySolver(boardObj.getBoard(),1)):
                print(boardObj.getBoard())
                print(self.p1.getName() + " has won")
                boardObj.reset()
                break
            elif not(boardObj.getRemainingMoves(boardObj.getBoard())):
                print("draw")
                boardObj.reset()
                break
            else:
                positions = boardObj.getRemainingMoves(boardObj.getBoard())
                p2Action = self.p2.chooseAction(positions, boardObj, 2, boardTuple)
                boardTuple[1] = boardObj.move(p2Action,2,boardTuple[1])
                boardHash = boardObj.getHash(boardTuple)
                self.p2.addState(boardHash)
                boardObj.printBoard()
                if(boardObj.binarySolver(boardObj.getBoard(),2)):
                    print(boardObj.getBoard())
                    print(self.p2.getName() + " has won")
                    boardObj.reset()
                    break
    

    def pgHumanvsAI(self, row, col, winNum,humanStart):
        font = pygame.font.SysFont(None, 24)
        text = font.render('', True, (255,255,255))
        boardObj = b(row, col, winNum)
        boardTuple = [0,0]
        loop = True
        state = 0 # 0 = playing,1 = drawn, 2 = winner (either ai or player)
        #turn allocation setup
        humanTurn = humanStart
        if(humanStart):
            first = 1
            second = 2
        else:
            first = 2
            second = 1
        
        while loop:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    loop = False
                if (event.type == KEYDOWN):
                    if(pygame.key.get_pressed()[pygame.K_SPACE]):
                        if(state>0):
                            state = 0
                            boardObj.reset()
                            humanTurn = humanStart
                if(pygame.mouse.get_pressed()[0]):
                    #print("re")
                    if(humanTurn):
                        #print("ht")
                        pos = pygame.mouse.get_pos()
                        p1Action = int(pos[0]/self.pixelSize)
                        if(p1Action in boardObj.getRemainingMoves(boardObj.getBoard())):
                            #boardObj.move(first,p1Action[0],p1Action[1])
                            boardTuple[first-1] = boardObj.move(p1Action,first,boardTuple[first-1])
                            boardHash = boardObj.getHash(boardTuple)
                            self.p1.addState(boardHash)
                            humanTurn = not humanTurn
                            
                            if(boardObj.binarySolver(boardObj.getBoard(),first)):
                                state = 2
                                text = font.render(self.p1.getName() + " has won", True, (255,255,255))

                            elif not(boardObj.getRemainingMoves(boardObj.getBoard())):
                                state = 1
                                text = font.render('draw', True, (255,255,255))
                                humanTurn = not humanTurn
            if(not humanTurn):
                positions = boardObj.getRemainingMoves(boardObj.getBoard())
                p2Action = self.p2.chooseAction(positions, boardObj, second,boardTuple)
                boardTuple[second-1] = boardObj.move(p2Action,second,boardTuple[second-1])
                boardHash = boardObj.getHash(boardTuple)
                self.p2.addState(boardHash)
                humanTurn = not humanTurn

                if(boardObj.binarySolver(boardObj.getBoard(),second)):
                    state = 2
                    text = font.render(self.p2.getName() + " has won", True, (255,255,255))
                    print(boardObj.getBoard())

                elif not(boardObj.getRemainingMoves(boardObj.getBoard())):
                    state = 1
                    text = font.render('draw', True, (255,255,255))           
            
            img = pygame.surfarray.make_surface(np.flip(np.rot90(boardObj.getBoard(),3),1))
            img = pygame.transform.scale(img, (col * self.pixelSize,row * self.pixelSize))
            #draw to the screen
            #self.screen.fill((0,0,0)) 
            self.screen.blit(img,(0,0))
            if(state>0):
                self.screen.blit(text,(0,0))
            pygame.display.flip()
        pygame.quit()

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

    def setupScreen(self):
        pygame.display.set_mode((self.col*self.pixelSize,self.row*self.pixelSize))
        self.screen = pygame.display.get_surface()

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
    else:
        print("training new data")
    st = Game(p1, p2)
    print("training...")
    st.aIVsAI(row,col, winNum, repitions)
    if(savePolicy):
        p1.savePolicy(row,col,winNum)
        p2.savePolicy(row,col,winNum)
        print("saved game")
    else:
        print("didnt save")

"""
Inputs of board rows, board columns, and win number
Loads computers AI is first player
"""  
def computerFirstGame(row,col,winNum):
    p1 = AI("computer", expRate = 0)
    p2 = Player("Human")
    p1.loadPolicy(row, col, winNum, "p1")

    st = Game(p1,p2,row,col)
    if(st.pygame):
        pygame.init()
        st.setupScreen()
        st.pgHumanvsAI(row,col, winNum,False)
    else:
        st.humanVsAI(row,col, winNum) 

"""
Inputs of board rows, board columns, and win number
Loads computers AI second player
"""
def humanFirstGame(row,col,winNum):
    p1 = Player("Human")
    p2 = AI("computer", expRate = 0)
    p2.loadPolicy(row, col, winNum, "p2")

    st = Game(p1,p2,row,col)
    if(st.pygame):
        pygame.init()
        st.setupScreen()
        st.pgHumanvsAI(row,col, winNum,True)
    else:
        st.humanVsAI(row,col, winNum) 
"""
Inputs of board rows, board columns, and win number
"""
def humanVsHumanGame(row,col,winNum):
    p1 = Player("Human1")
    p2 = Player("Human2")
    st = Game(p1,p2)
    st.humanVsHuman(row,col, winNum)


start = time.time()
#trainAI(10000000,6,7,4,continueAITraining=True, savePolicy=True)
#computerFirstGame(6,7,4)
humanFirstGame(6,7,4)
end = time.time()
print(end - start)