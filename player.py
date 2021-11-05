class Player:
    def __init__(self,name):
        self.name = name
    
    def getName(self):
        return self.name
    """
    Input of remaining positions the board and the player
    ask for the input of the row and column
    whilst row and column are not in the positions list repeats question
    add to board
    """
    def chooseAction(self,positions,board,player,currentBoardNum):
        print("It is player "+str(player)+"'s turn.")

        col = int(input("Enter column: "))
        while(col not in positions):
            print("Make sure the coordinate hasn't been previously used.")
            col = int(input("Enter column between or equal to 0 and 2: "))
        return col
    
    def addState(self,state):
        pass
    def feedReward(self):
        pass
    def reset(self):
        pass
