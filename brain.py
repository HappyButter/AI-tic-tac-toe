import pygame

class Game:
    ################################################################################
    #                             Init values  
    ################################################################################
    def __init__(self, name='AI  Tic-tac-toe!'):
            
        pygame.init()
        self.display_width = 800
        self.display_height = 600

        self.game_display = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.XO_image = pygame.image.load('XO.png')

        self.X_image_place = (0,0,150,150)
        self.O_image_place = (150,0,153,150)

        self.board = [['empty' for i in range(3)] for i in range(3)]

        self.crashed = False
        self.is_x_turn = False
        self.game_over = False

    ################################################################################
    #                             Base functions   
    ################################################################################
    def draw_board(self):
        line_color = (172, 42, 219)
        pygame.draw.line(self.game_display, line_color, (200,10), (200,590), 20)
        pygame.draw.line(self.game_display, line_color, (400,10), (400,590), 20)

        pygame.draw.line(self.game_display, line_color, (10,200), (590,200), 20)
        pygame.draw.line(self.game_display, line_color, (10,400), (590,400), 20)


    def draw_players(self):

        for i in range(3):
            for j in range(3):
                x = i*200 + 25
                y = j*200 + 25

                if self.board[i][j] == 'X':
                    self.game_display.blit(self.XO_image, (x, y), self.X_image_place)
                if self.board[i][j] == 'O':
                    self.game_display.blit(self.XO_image, (x, y), self.O_image_place)    


    def save_move(self, pos):
        sign = 'empty'
        
        if self.is_x_turn == True:
            sign = 'X'
        if self.is_x_turn == False:
            sign = 'O'

        for i in range(3):
            for j in range(3):
                    if pos[0] > 200*i and pos[0] < 200*(i+1) and pos[1] > j*200 and pos[1] < (j+1)*200 and self.board[i][j] == 'empty':
                        self.board[i][j] = sign
                        self.is_x_turn = not self.is_x_turn


    def equal3(self, a, b, c):
        if a == b and b == c and a != 'empty':
            return a
        return None


    def is_game_over(self):
        # Crosswis
        if self.equal3(self.board[0][0],self.board[1][1], self.board[2][2]) != None:
            return self.board[0][0]
        if self.equal3(self.board[2][0],self.board[1][1], self.board[0][2]) != None:
            return self.board[0][0]

        # Rows
        for i in range(3):
            if self.equal3(self.board[0][i], self.board[1][i], self.board[2][i]) != None:
                return self.board[0][i]

        # Columns
        for i in range(3):
            if self.equal3(self.board[i][0], self.board[i][1], self.board[i][2]) != None:
                return self.board[i][0]

        # is full
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'empty':
                    return 'no_winner'

        return 'tie'


    ################################################################################
    #                             Crash screen  
    ################################################################################
    def text_objects(self, text, font_size):
        font = pygame.font.SysFont('Comic Sans MS', font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        return text_surface, text_surface.get_rect()


    def game_quit(self):
        pygame.quit()
        quit()


    def restart(self):
        self.game_over = False
        self.board = [['empty' for i in range(3)] for i in range(3)]


    def button(self,msg,x,y,w,h,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.game_display, (255,0,0), (x,y,w,h))

            if click[0] == 1:
                action()

        else:
            pygame.draw.rect(self.game_display, (0,255,0), (x,y,w,h))

        textSurf, textRect = self.text_objects(msg, 20)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.game_display.blit(textSurf, textRect)


    def game_over_screen(self):

        self.game_display.fill((255,255,255))

        TextSurf, TextRect = self.text_objects("Game Over", 115)
        TextRect.center = ((self.display_width/2),(self.display_height/2)-115)
        self.game_display.blit(TextSurf, TextRect)

        end_state = self.is_game_over()
        if end_state == 'tie':
            TextSurf, TextRect = self.text_objects("It's a tie!", 80)    
        else:
            TextSurf, TextRect = self.text_objects(end_state + " player won!", 80)
        
        TextRect.center = ((self.display_width/2),(self.display_height/2))
        self.game_display.blit(TextSurf, TextRect)

        while self.game_over:
            for e in pygame.event.get():

                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    

            self.button("QUIT",(self.display_width/2)-190,(self.display_height/2)+100,100,50, self.game_quit) 
            self.button("Restart",(self.display_width/2)+90,(self.display_height/2)+100,100,50, self.restart)
            
            pygame.display.update()

    ################################################################################
    #                               AI 
    ################################################################################
    def is_move_left(self, current_board):
        for i in range(3):
            for j in range(3):
                if current_board[i][j] == 'empty':
                    return True
        return False


    def evaluate(self, current_board):
        # Rows
        for row in range(3):
            winner = self.equal3(current_board[row][0], current_board[row][1], current_board[row][2])
            
            if  winner != None:
                if winner == 'O': 
                    return -10
                elif winner == 'X':
                    return 10

        # Columns
        for col in range(3):
            winner = self.equal3(current_board[0][col], current_board[1][col], current_board[2][col])
            
            if  winner != None:
                if winner == 'O': 
                    return -10
                elif winner == 'X':
                    return 10

        # Corsswis
        winner = self.equal3(current_board[0][0], current_board[1][1], current_board[2][2]) 
        if winner != None:
            if winner == 'O': 
                return -10
            elif winner == 'X':
                return 10

        winner = self.equal3(current_board[2][0], current_board[1][1], current_board[0][2])
        if  winner != None:
            if winner == 'O': 
                return -10
            elif winner == 'X':
                return 10
                
        return 0


    def minmax(self, current_board, is_max):

        # checking if minmax function have reached end of the current game
        score = self.evaluate(current_board)
        if score == 10 or score == -10: 
            return score

        # checking if the board is not full 
        if self.is_move_left(current_board) == False:
            return 0

        if is_max:
            best_score = -1000
            for i in range(3):
                for j in range(3):
                    if current_board[i][j] == 'empty':
                        current_board[i][j] = 'X'
                        best_score = max(best_score, self.minmax(current_board, not is_max))
                        current_board[i][j] = 'empty'

            return best_score
        
        else:
            best_score = 1000
            for i in range(3):
                for j in range(3):
                    if current_board[i][j] == 'empty':
                        current_board[i][j] = 'O'
                        best_score = min(best_score, self.minmax(current_board, not is_max))
                        current_board[i][j] = 'empty'

            return best_score
            

    def find_best_Move(self, current_board):
        best_value = -1000
        best_move = (-1,-1)
        for i in range(3):
            for j in range(3):
                if current_board[i][j] == 'empty':
                    current_board[i][j] = 'X'
                    move_value = self.minmax(current_board, False)
                    current_board[i][j] = 'empty'

                    if move_value > best_value:
                        best_value = move_value
                        best_move = (i,j)
        # print("best value is: " + str(best_value))
        return best_move
        
    ################################################################################
    #                            Game loop 
    ################################################################################
    def start(self):
        while not self.crashed:
            self.game_display.fill((0,0,0))

            self.draw_board()
            self.draw_players()


            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    self.crashed = True
            
                if self.is_game_over() == 'no_winner':
                    
                    if self.is_x_turn:
                        best_move = self.find_best_Move(self.board.copy())
                        best_move = (best_move[0]*200 + 1, best_move[1]*200 + 1)
                        self.save_move(best_move)
                    # handle MOUSEBUTTONUP
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        self.save_move(pos)
                else:
                    print("And the winner is... ", self.is_game_over())
                    self.game_over = True
                    self.game_over_screen()
                        

            pygame.display.update()
            self.clock.tick(30)
