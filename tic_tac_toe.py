import pygame
from time import sleep

pygame.init()
width = 800
height = 600

game_display = pygame.display.set_mode((width,height))
pygame.display.set_caption('AI  Tic-tac-toe!')
image = pygame.image.load(r'C:\Users\Carrot\Desktop\AGH\semestr 4\AI\Portfolio\Part07\XO.png')

X_image = (0,0,150,150)
O_image = (150,0,153,150)

board = [['empty' for i in range(3)] for i in range(3)]

clock = pygame.time.Clock()

crashed = False
is_x_turn = False


def draw_board(display):
    line_color = (172, 42, 219)
    pygame.draw.line(display, line_color, (200,10), (200,590), 20)
    pygame.draw.line(display, line_color, (400,10), (400,590), 20)

    pygame.draw.line(display, line_color, (10,200), (590,200), 20)
    pygame.draw.line(display, line_color, (10,400), (590,400), 20)


def draw_players(display):

    for i in range(3):
        for j in range(3):
            x = i*200 + 25
            y = j*200 + 25

            if board[i][j] == 'X':
                display.blit(image, (x, y), X_image)
            if board[i][j] == 'O':
                display.blit(image, (x, y), O_image)    



def save_move(pos, is_x_turn):
    sign = 'empty'
    
    if is_x_turn == True:
        sign = 'X'
    if is_x_turn == False:
        sign = 'O'

    for i in range(3):
        for j in range(3):
                if pos[0] > 200*i and pos[0] < 200*(i+1) and pos[1] > j*200 and pos[1] < (j+1)*200 and board[i][j] == 'empty':
                    board[i][j] = sign
                    is_x_turn = not is_x_turn
    return is_x_turn


def equal(a, b, c):
    return a == b and b == c and a != 'empty'


def is_game_over():
    # Crosswis
    if equal(board[0][0],board[1][1], board[2][2]):
        return board[0][0]
    if equal(board[2][0],board[1][1], board[0][2]):
        return board[0][0]

    # Rows
    for i in range(3):
        if equal(board[0][i], board[1][i], board[2][i]):
            return board[0][i]

    # Columns
    for i in range(3):
        if equal(board[i][0], board[i][1], board[i][2]):
            return board[i][0]

    # is full
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'empty':
                return 'no_winner'

    return 'tie'


def text_info(display):
    font = pygame.font.SysFont('Comic Sans MS', 40)
    text = font.render(is_game_over() + ' won', True, (255, 0, 0), (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (275, 275)
    display.blit(text, text_rect)

while not crashed:
    game_display.fill((0,0,0))

    draw_board(game_display)
    draw_players(game_display)


    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            crashed = True
    

        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            is_x_turn = save_move(pos, is_x_turn)

            if is_game_over() != 'no_winner':
                print("And the winner is... ", is_game_over())
        

    pygame.display.update()

    clock.tick(60)
