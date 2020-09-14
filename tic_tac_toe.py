import pygame
from time import sleep

################################################################################
#                             Init values  
################################################################################

pygame.init()
width = 800
height = 600

game_display = pygame.display.set_mode((width,height))
pygame.display.set_caption('AI  Tic-tac-toe!')
clock = pygame.time.Clock()
image = pygame.image.load('XO.png')

X_image = (0,0,150,150)
O_image = (150,0,153,150)

board = [['empty' for i in range(3)] for i in range(3)]

crashed = False
is_x_turn = False
game_over = False

################################################################################
#                             Base functions   
################################################################################

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
    if a == b and b == c and a != 'empty':
        return a
    return None


def is_game_over():
    # Crosswis
    if equal(board[0][0],board[1][1], board[2][2]) != None:
        return board[0][0]
    if equal(board[2][0],board[1][1], board[0][2]) != None:
        return board[0][0]

    # Rows
    for i in range(3):
        if equal(board[0][i], board[1][i], board[2][i]) != None:
            return board[0][i]

    # Columns
    for i in range(3):
        if equal(board[i][0], board[i][1], board[i][2]) != None:
            return board[i][0]

    # is full
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'empty':
                return 'no_winner'

    return 'tie'


################################################################################
#                             Crash screen  
################################################################################

def text_objects(text, font_size):
    font = pygame.font.SysFont('Comic Sans MS', font_size)
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()


def game_quit():
    pygame.quit()
    quit()


def restart():
    global game_over
    global board

    game_over = False
    board = [['empty' for i in range(3)] for i in range(3)]


def button(msg,x,y,w,h,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_display, (255,0,0), (x,y,w,h))

        if click[0] == 1:
            action()

    else:
        pygame.draw.rect(game_display, (0,255,0), (x,y,w,h))

    textSurf, textRect = text_objects(msg, 20)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(textSurf, textRect)


def game_over_screen():

    game_display.fill((255,255,255))

    TextSurf, TextRect = text_objects("Game Over", 115)
    TextRect.center = ((width/2),(height/2)-115)
    game_display.blit(TextSurf, TextRect)

    if is_game_over() == 'tie':
        TextSurf, TextRect = text_objects("It's a tie!", 80)    
    else:
        TextSurf, TextRect = text_objects(is_game_over() + " player won!", 80)
    
    TextRect.center = ((width/2),(height/2))
    game_display.blit(TextSurf, TextRect)

    while game_over:
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
                

        button("QUIT",(width/2)-190,(height/2)+100,100,50, game_quit) 
        button("Restart",(width/2)+90,(height/2)+100,100,50, restart)
        
        pygame.display.update()

################################################################################
#                               AI 
################################################################################

AI = 'O'
player = 'X'

def is_move_left(current_board):
    for i in range(3):
        for j in range(3):
            if current_board[i][j] == 'empty':
                return True
    return False


def evaluate(current_board):
    # Rows
    for row in range(3):
        winner = equal(current_board[row][0], current_board[row][1], current_board[row][2])

        if winner == AI: 
            return -10
        elif winner == player:
            return 10

    # Columns
    for col in range(3):
        winner = equal(current_board[0][col], current_board[1][col], current_board[2][col])
        
        if winner == AI: 
            return -10
        elif winner == player:
            return 10

    # Corsswis
    winner = equal(board[0][0],board[1][1], board[2][2]) 
    if winner != None:
        if winner == AI: 
            return -10
        elif winner == player:
            return 10

    winner = equal(board[2][0],board[1][1], board[0][2])
    if  winner != None:
        if winner == AI: 
            return -10
        elif winner == player:
            return 10
            
    return 0


def minmax(current_board, is_max):

    # checking if minmax function have reached end of the current game
    score = evaluate(current_board)
    if score == 10 or score == -10: 
        return score

    # checking if the board is not full 
    if is_move_left(current_board) == False:
        return 0

    if is_max:
        best_score = -1000
        for i in range(3):
            for j in range(3):
                if current_board[i][j] == 'empty':
                    current_board[i][j] = player
                    best_score = max(best_score, minmax(current_board, not is_max))
                    current_board[i][j] = 'empty'

        return best_score
    
    else:
        best_score = 1000
        for i in range(3):
            for j in range(3):
                if current_board[i][j] == 'empty':
                    current_board[i][j] = AI
                    best_score = min(best_score, minmax(current_board, not is_max))
                    current_board[i][j] = 'empty'

        return best_score
         

def find_best_Move(current_board):
    best_value = -1000
    best_move = (-1,-1)
    for i in range(3):
        for j in range(3):
            if current_board[i][j] == 'empty':
                current_board[i][j] = player
                move_value = minmax(current_board, False)
                current_board[i][j] = 'empty'

                if move_value > best_value:
                    best_value = move_value
                    best_move = (i,j)
    # print("best value is: " + str(best_value))
    return best_move
    
################################################################################
#                            Game loop 
################################################################################

while not crashed:
    game_display.fill((0,0,0))

    draw_board(game_display)
    draw_players(game_display)


    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            crashed = True
    
        if is_game_over() == 'no_winner':
            
            if is_x_turn:
                best_move = find_best_Move(board.copy())
                best_move = (best_move[0]*200 + 1, best_move[1]*200 + 1)
                is_x_turn = save_move(best_move, is_x_turn)
            # handle MOUSEBUTTONUP

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                is_x_turn = save_move(pos, is_x_turn)
        else:
            print("And the winner is... ", is_game_over())
            game_over = True
            game_over_screen()
                

    pygame.display.update()
    clock.tick(30)
