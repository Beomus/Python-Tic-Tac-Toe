import pygame
import time
import sys
import random
import itertools

WIDTH = 600
HEIGHT = 600

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (10, 10, 10)

class Board:
    def __init__(self, w, h, dimension=3):
        self._board = [[None] * 3, [None] * 3, [None] * 3]
        self.dimension = dimension
        self.turn = 0
        pygame.init()
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode([w, h])
        pygame.display.set_caption("Tic Tac Toe")
        self.display.fill(WHITE)
        self.clock = pygame.time.Clock()

    def draw_board(self):
        for i in range(1, self.dimension):
            pygame.draw.line(self.display, BLACK, (int(i*self.width/self.dimension), 0), (int(i*self.width/self.dimension), self.height), 5)
            pygame.draw.line(self.display, BLACK, (0, int(i*self.height/self.dimension)), (self.width, int(i*self.height/self.dimension)), 5)

    def draw_XO(self, turn, pos):
        x, y, row, col = pos
        if x is None or y is None or row is None or col is None:
            return

        if turn == "O" and self._board[row][col] is None:
            self._board[row][col] = "O"
            pygame.draw.circle(self.display, BLACK, (int(x), int(y)), int(self.height/12), 10)
            self.turn += 1
            # self._check_state()
        
        if turn == "X" and self._board[row][col] is None:
            self._board[row][col] = "X"
            pygame.draw.line(self.display, BLACK, (x - self.width/12, y - self.height/12), (x + self.width/12, y + self.height/12), 10)
            pygame.draw.line(self.display, BLACK, (x + self.width/12, y - self.height/12) ,(x - self.width/12, y + self.height/12), 10)
            self.turn += 1
            # self._check_state()


    def click(self):
        x, y = pygame.mouse.get_pos()
        # @TODO: fix center pos
        if x < self.width/3:
            x_pos = self.width/6
            col = 0
        elif x <= self.width*2/3:
            x_pos = self.width/3 + self.width/6
            col = 1
        elif x <= self.width:
            x_pos = self.width*2/3 + self.width/6
            col =2
        else:
            x_pos = None
            col = None

        if y < self.height/3:
            y_pos = self.height/6
            row = 0
        elif y <= self.height*2/3:
            y_pos = self.height/3 + self.height/6
            row = 1
        else:
            y_pos = self.height*2/3 + self.height/6
            row = 2
        position = x_pos, y_pos, row, col
        print(position)
        return position
        # if (row and col and self._board[row][col] is None):
            # print(self._board)
            # print(self.turn)
            # self.draw_XO(self.turn, (x_pos, y_pos, row, col))
            # next(self.turn)
            # self._check_state()
        

    def _check_state(self):
        """
        state will be assign to winner which is none
        update winner once one is found and return the state "won"
        also check full board to return state "draw"
        default return "None"
        """
        winner = None
        # check row
        for row in range(3):
            if (self._board[row][0] == self._board[row][1] == self._board[row][2]) and (self._board[row][0] is not None):
                winner = self._board[row][0]
                pygame.draw.line(self.display, (255, 0, 0), (0, (int(row*self.height/3) + 100)), (self.width, int(row*self.height/3) + 100), 20)
                # time.sleep(2)
                return ("Won", winner)

        # check col
        for col in range(3):
            if (self._board[0][col] == self._board[1][col] == self._board[2][col]) and (self._board[0][col] is not None):
                winner = self._board[0][col]
                pygame.draw.line(self.display, (255, 0, 0), ((int(col*self.width/3) + 100, 0)), (int(col*self.width/3) + 100, self.height), 20)
                # time.sleep(2)
                return ("Won", winner)

        # check diagonal
        if (self._board[0][0] == self._board[1][1] == self._board[2][2]) and (self._board[0][0] is not None):
            winner = self._board[0][0]
            pygame.draw.line(self.display, (255, 0, 0), (self.width/6, self.height/6), (self.width*2/3 + self.width/6, self.height*2/3 + self.height/6), 20)
            # time.sleep(2)
            return ("Won", winner)
        if (self._board[0][2] == self._board[1][1] == self._board[2][0]) and (self._board[0][2] is not None):
            winner = self._board[0][2]
            pygame.draw.line(self.display, (255, 0, 0), (self.width/6, self.height*2/3 + self.height/6), (self.width*2/3 + self.width/6, self.height/6), 20)
            # time.sleep(2)
            return ("Won", winner)

        if all([all(row) for row in self._board]) and winner is None:
            time.sleep(2)
            return ("Draw", winner)
        
        return (None, winner)

    def _display_message(self, message):
        font = pygame.font.SysFont("comicsansms", 40)
        text_surface = font.render(message, True, BLACK, WHITE)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (WIDTH / 2, HEIGHT / 2)
        self.display.fill(WHITE)
        self.display.blit(text_surface, text_rectangle)
    
    def play(self):
        run = True
        state = None
        winner = None
        turn_cycle = ["X", "O"]
        track = 0
        self.display.fill(WHITE)
        while run and state not in ["Draw", "Won"]:

            self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self.click()
                    cur_turn = turn_cycle[self.turn%2]
                    self.draw_XO(cur_turn, pos)
                    self._check_state()
            
            if state is None:
                state, winner = self._check_state()
        
            if winner is not None:
                # time.sleep(2)
                if winner == "X" or winner == "O":
                    self._display_message(f"Winner is: {winner} with total {self.turn} turns!")
                elif winner == "Draw":
                    self._display_message(f"It's a {winner} with total {self.turn} turns!")

            pygame.display.update()
            self.clock.tick(FPS)

        time.sleep(2)
        pygame.quit()


def main():
    
    board = Board(WIDTH, HEIGHT)
    board.play()

        
    
if __name__ == "__main__":
    main()