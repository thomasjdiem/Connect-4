from AlphaBeta import *
import pygame

BoardDimensions = (6,7)

TopHeight = 150
HEIGHT = 100*BoardDimensions[0]
WIDTH = 100*BoardDimensions[1]

white = (245,245,245)
red = (220,0,0)
black = (0,0,0)
yellow = (255,255,153)
blue = (0,50,200)

Colors = {-1:black, 0:white, 1:red}

class Game:
    def __init__(self, dimensions):
        self.nrows, self.ncols = dimensions
        self.board = [[0 for _ in range(self.ncols)] for _ in range(self.nrows)]
        self.turn = 1
        self.num_moves = 0
        self.possible_moves = list(range(self.ncols))
        self.winner = 0
        self.way = ""

    def MakeMove(self, position):
        for row in range(self.nrows-1,0,-1):
            if self.board[row][position] == 0:
                self.board[row][position] = self.turn
                self.turn *= -1
                self.num_moves += 1
                return

        self.board[0][position] = self.turn
        self.turn *= -1
        self.num_moves += 1
        self.possible_moves.remove(position)
            
    def CheckWinner(self):
        # Check rows
        for row in range(self.nrows):
            for col in range(self.ncols-3):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][col + 3]:
                    self.winner = self.board[row][col]
                    self.way = "row"


        # Check columns
        for row in range(self.nrows-3):
            for col in range(self.ncols):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col]:
                   self.winner = self.board[row][col]
                   self.way = "col"

        # Check diagonal (top left to bottom right)
        for row in range(self.nrows-3):
            for col in range(self.ncols-3):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3]:
                    self.winner = self.board[row][col]
                    self.way = "diag"

        # Check diagonal (top right to bottom left)
        for row in range(self.nrows-3):
            for col in range(3, self.ncols):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row + 1][col - 1] == self.board[row + 2][col - 2] == self.board[row + 3][col - 3]:
                    self.winner = self.board[row][col]
                    self.way = "diag"
    
    def Display(self):
        for row in range(self.nrows):
            for col in range(self.ncols):
                pygame.draw.circle(WIN,Colors[self.board[row][col]],\
                (col*WIDTH/self.ncols + 50,row*HEIGHT/self.nrows + TopHeight + 50),45)
    
def DisplayOptions():
    Text1 = ["Player", "Player", "Computer"]
    Text2 = ["Player", "Computer", "Player"]

    for i in range(3):
        pygame.draw.rect(WIN, yellow, \
            pygame.Rect(i*WIDTH/3, 0, (i+1) * WIDTH/3, TopHeight))
        pygame.draw.rect(WIN, black, \
            pygame.Rect(i*WIDTH/3, 0, (i+1) * WIDTH/3, TopHeight),5)
        font = pygame.font.Font(None, 45)

        text_surface = font.render(Text1[i], True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((i+0.5) * WIDTH/3,TopHeight/2 - 30)
        WIN.blit(text_surface, text_rect)

        text_surface = font.render("vs", True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((i+0.5) * WIDTH/3,TopHeight/2)
        WIN.blit(text_surface, text_rect)

        text_surface = font.render(Text2[i], True, black)
        text_rect = text_surface.get_rect()
        text_rect.center = ((i+0.5) * WIDTH/3,TopHeight/2 + 30)
        WIN.blit(text_surface, text_rect)

def DisplayText(MyGame, Players):
    text = Players[MyGame.turn] + " turn"
    if MyGame.num_moves == 0:
        text = "Start Game! " + text
    if MyGame.num_moves >= MyGame.ncols * MyGame.nrows:
        text = "Game ended in a draw."
    if MyGame.winner != 0:
        text = "Game over.  " + Players[MyGame.winner] + " wins."

    pygame.draw.rect(WIN, yellow, pygame.Rect(0, 0, WIDTH, TopHeight))
    font = pygame.font.Font(None, 65)

    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH/2,TopHeight/2)
    WIN.blit(text_surface, text_rect)

if __name__ == "__main__":

    WIN = pygame.display.set_mode((WIDTH,HEIGHT+TopHeight))
    pygame.init()
    WIN.fill(blue)

    MyGame = Game(BoardDimensions)
    MyGame.Display()
    DisplayOptions()  
    pygame.display.update()
    
    PygameRunning = True
    GameStarted = False
    GameOver = False

    while PygameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PygameRunning = False
            if GameStarted:
                if not GameOver:
                    if Computer != MyGame.turn:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_presses = pygame.mouse.get_pressed()
                            if mouse_presses[0]:
                                x,y = pygame.mouse.get_pos()
                                if y > TopHeight:
                                    pos = x*MyGame.ncols // WIDTH
                                    MyGame.MakeMove(pos)
                                    MyGame.Display()
                                    pygame.display.update()
                                    MyGame.CheckWinner()
                                    if MyGame.winner != 0:
                                        GameOver = True
                                    if MyGame.num_moves == MyGame.nrows * MyGame.ncols:
                                        GameOver = True
                                    DisplayText(MyGame, Players)
                                    pygame.display.update()
                    else:
                        _, best_move = AlphaBeta(MyGame, 6, -100000, 100000, Computer)
                        MyGame.MakeMove(best_move)
                        MyGame.CheckWinner()
                        MyGame.Display()
                        pygame.display.update()
                        if MyGame.winner != 0:
                            GameOver = True
                        if MyGame.num_moves == MyGame.nrows * MyGame.ncols:
                            GameOver = True
                        DisplayText(MyGame, Players)
                        pygame.display.update()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        x,y = pygame.mouse.get_pos()
                        if y < TopHeight:
                            option = x*3 // WIDTH
                            if option == 0:
                                Players = {1: "Player 1", -1: "Player 2"}
                                Computer = 0
                            elif option == 1:
                                Players = {1: "Player", -1: "Computer"}
                                Computer = -1
                            else:
                                Players = {1: "Computer", -1: "Player"}
                                Computer = 1
                            GameStarted = True
                            DisplayText(MyGame, Players)
                            pygame.display.update()

                    
    pygame.quit()