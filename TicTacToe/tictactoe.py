import time
import pygame



#Создать спрайт для квадрата
class GameBoardSquareSprite(pygame.sprite.Sprite):
    def __init__(self, color, row, column, width, height):
        super().__init__()
        self.width=width
        self.height=height
        #Создание поверхность для спрайта
        self.image=pygame.Surface([width,height])
        #Сделать фоновую игровую плитку белой
        self.image.fill(WHITE)
        self.rect=self.image.get_rect().move(row*width, column*height)
        #Нарисуйте прямоугольник на поверхности спрайта
        pygame.draw.rect(self.image, color, pygame.Rect(
            0, 0, width, height),2)

    #рисуем спрайт на экране
    def draw(self, surface):
        surface.blit(self.image, 0, 0)

# класс GameBoard, который будет проверять выигрыши,
# проигрыши и ничьи, а также даст нам возможность заполнить
# доску нашими предположениями. Также может управлять
# алгоритмической логикой размещения букв «О».
class GameBoard:
    def __init__(self, grid_size):
        self.grid_size=grid_size
        self.winner=''
        self.initialize_board()

    def initialize_board(self):
        self.board=[
            [0,0,0],
            [0,0,0],
            [0,0,0],
        ]

    # Проверьте, выиграл ли кто-то в любой строке, столбце или диагонали
    def check_if_anybody_won(self):
        # Проверить, выиграл ли кто-то по горизонтали

        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != 0:
                self.winner = self.board[row][0]
                return True

        # Проверить, выиграл ли кто-то по вертикали

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                self.winner = self.board[0][col]
                return True

        #Проверить, выиграл ли кто-то по диагонали
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.winner = self.board[0][0]
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            self.winner = self.board[0][2]
            return True

        return False

    #Проверить, заполнена ли доска
    def check_if_board_is_full(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col]==0:
                    return False
        return True


    #Поместите Х
    def place_X(self, row, col):
        self.board[row][col]="X"

    # Используется run_better_algorithm_to_place_O, чтобы
    # определить, приводит ли размещение фигуры в строке
    # или столбце на доске к выигрышному ходу. Это
    # используется для определения блокировки,а также
    # для победы противника "O"

    def is_winning_move(self, player, row, col):
        n=len(self.board)
        #Проверить строки
        if all(self.board[row][j]==player
               for j in range(n)):
            return True
        #Проверить столбцы
        if all(self.board[i][col]==player
               for i in range(n)):
            return True

        #Проверить главную диагональ
        if (row==col and all(self.board[i][i]==
            player for i in range(n))):
            return True
        #Проверить вторичную диагональ
        if (row+col==n-1 and
        all(self.board[i][n-i-1]
            ==player for i in range(n))):
            return True

        return False
    #Используется методом run_better_algorithm_to_place_O
    # для сбора всех доступных позиций на доске.
    def get_empty_positions(self):
        empty_positions = []
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell == 0:
                    empty_positions.append((i, j))
        return empty_positions

    # Использует алгоритм, чтобы решить, где разместить O.
    # Этот алгоритм никогда не проигрывает.
    def run_better_algorithm_to_place_O(self):
        grid_size = len(self.board)
        empty_positions = self.get_empty_positions()
        num_moves = sum(1 for row in self.board for
                        cell in row if cell != 0)

        # Второй ход: поместите "О" в центр или угол
        if num_moves == 1:
            center = grid_size // 2
            if (self.board[center][center] == 0):
                self.board[center][center] = "O"
                return (True, center, center)
            else:
                for row, col in [(0, 0), (0, grid_size - 1),
                                 (grid_size - 1, 0),
                                 (grid_size - 1, grid_size - 1)]:
                    if self.board[row][col] == 0:
                        self.board[row][col] = "O"
                        return (True, row, col)

        # Попробуйте выиграть или заблокировать Х для победы
        for row, col in empty_positions:
            # Check if placing "O" would win the game
            self.board[row][col] = "O"
            if self.is_winning_move("O", row, col):
                return (True, row, col)
            self.board[row][col] = 0

        # Проверьте, помешает ли размещение "О" Х выиграть
        for row, col in empty_positions:
            self.board[row][col] = "X"
            if self.is_winning_move("X", row, col):
                self.board[row][col] = "O"
                return (True, row, col)
            self.board[row][col] = 0

        # Поместите "О" в угол в начале игры
        if self.board[0][0] == "O" \
                or self.board[0][grid_size - 1] == "O" \
                or self.board[grid_size - 1][0] == "O" \
                or self.board[grid_size - 1][grid_size - 1] == "O":
            for row, col in [(0, 0), (0, grid_size - 1),
                             (grid_size - 1, 0),
                             (grid_size - 1, grid_size - 1)]:
                if self.board[row][col] == 0:
                    self.board[row][col] = "O"
                    (True, row, col)
                    return (True, row, col)

        # Поместите "О" на угловой стороне
        for row, col in empty_positions:
            if row not in [0, grid_size - 1] \
                    and col not in [0, grid_size - 1]:
                self.board[row][col] = "O"
                return (True, row, col)

        # Поместите "О" в любое доступное место
        for row, col in empty_positions:
            self.board[row][col] = "O"
            return (True, row, col)

        return (False, -1, -1)

    def get_winner_display_message(self):
        if self.winner == 'X':
            return 'X Wins!'
        elif self.winner == 'O':
            return 'O Wins!'
        else:
            return 'Draw!'

    def check_if_its_a_draw(self):
        return not (self.check_if_anybody_won()) and self.check_if_board_is_full()


#класс рисующий на экране Х или О
class LetterSprite(pygame.sprite.Sprite):
    def __init__(self, letter, row, column,
                 grid_width, grid_height):
        #инициализировать базовый класс спрайта
        super().__init__()
        font = pygame.font.Font(None, 150)

        #визуализировать шрифт на поверхности изображения
        self.image=font.render(letter, True, (0,0,0))

        #определить границы изображения на доске
        self.rect=self.image.get_rect().move(
            row*grid_width+grid_width/3,
            column*grid_height+grid_height/3
        )

    def update(self):
        pass

    def draw(self, surface):
        letter_piece=self.image
        surface.blit(letter_piece, self.rect)



# Определите цвета
WHITE=(255,255,255)
BLACK=(0,0,0)

game_window = None

# размеры игрового окна
window_width = 600
window_height = 600

#размеры сетки
grid_size = 3
grid_width = window_width / grid_size
grid_height = window_height / grid_size

# инициализируйте объект font для рендеринга текста
font = None
smallfont = None

# флаг окончания игры
game_over = False
X_placed = False
O_placed = False

# инициализируйте плату

board = None
group = None



# обработка событий
def run_event_processing():
    global X_placed
    global game_over

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            # Разместить Х на доске
            handle_mouse_down_for_x()
            X_placed=True

def handle_mouse_down_for_x():
     (row, col)=pygame.mouse.get_pos()
     row=int(row/grid_width)
     col=int(col/grid_height)
     board.place_X(row, col)
     letterX=LetterSprite('X', row, col,
                          grid_width, grid_height)
     group.add(letterX)

# Создание доски
def draw_the_board():
    group.draw(game_window)


# Создание игрового поля
def draw_game_board_square(row, col):
    rect=pygame.Rect(col*grid_width,
                     row*grid_height,
                     grid_width,
                     grid_height)
    pygame.draw.rect(game_window, BLACK, rect)

def draw_tic_tac_toe_letter(row, col, letter):
    letter_piece=font.render(letter, True, BLACK)
    game_window.blit(
        letter_piece, (row * grid_width+grid_width/4,
                       col*grid_height+grid_height/4)
    )


# Очень простой алгоритм размещения О на доске.
# Пройдись по всей доске и найдите первую доступную
# клетку. Поместите О там.

def run_algorithm_to_place_O():
    for rowo in range(grid_size):
        for colo in range(grid_size):
            if(board[rowo][colo]==0):
                board[rowo][colo]="O"
                return True
    return False


# Проверить на победу

def check_if_anyone_won():
    global winner
    #Проверить, выиграл ли кто-то по горизонтали
    for row in range(3):
        if (board[row][0]==board[row][1]
            ==board[row][2]!=0):
            winner=board[row][0]
            return True
    #Проверить, выиграл ли кто-то по вертикали
    for col in range(3):
        if (board[0][col]==board[1][col]
            ==board[2][col]!=0):
            winner=board[0][col]
            return True
    #Проверить, выиграл ли кто-то по диагонали
    if (board[0][0]==board[1][1]
        ==board[2][2]!=0):
        winner=board[0][0]
        return True
    if (board[0][2]==board[1][1]
        ==board[2][0]!=0):
        winner=board[0][2]
        return True

    #никто не выиграл вернуть false

    return False

#Проверка на ничью
def check_if_board_if_full():
    for row in range(3):
        for col in range(3):
            if board[row][col]==0:
                return False
    return True




#играть снова

def check_for_quit_event():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_y:
                initialize_game_values()
                game_window.fill(WHITE)
                return True
            elif event.key==pygame.K_n:
                pygame.quit()
                quit()

def initialize_game_values():
    global board
    global game_over
    global X_placed
    global O_placed
    global clock
    global group

    game_over = False
    X_placed = False
    O_placed = False

    board = GameBoard(grid_size)

    clock = pygame.time.Clock()

    group = pygame.sprite.Group()

    initialize_game_board()

#Создание игрового окна
def initialize_game_board():
    for row in range(3):
        for column in range(3):
            game_board_square=GameBoardSquareSprite(
                (0,255,0), row, column,
                grid_width, grid_height)
            group.add(game_board_square)


def initialize_game():
    global game_window
    global font
    global smallfont

    initialize_game_values()
    # Инициализация игры
    pygame.init()
    game_window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Tic-Tac-Toe')
    # Создание объектов шрифта
    font = pygame.font.Font(None, 150)
    smallfont = pygame.font.Font(None, 50)

    initialize_game_board()

    return game_window


game_window = initialize_game()


def check_for_win_or_draw():
    global game_over
    if (board.check_if_anybody_won()):
        game_over = True
    elif (board.check_if_its_a_draw()):
        game_over = True
        board.winner = 'Nobody'

    return game_over


def draw_game_over_screen():
    game_window.fill(WHITE)
    winner_message = board.get_winner_display_message()

    text = font.render(winner_message, True, BLACK)

    # get the width of the text
    text_width = text.get_width()

    play_again_text = smallfont.render('Play Again (y/n)?', True, BLACK)

    play_again_text_width = play_again_text.get_width()

    game_window.blit(
        text, (window_width/2 - text_width/2, window_height/2 - 100))

    game_window.blit(play_again_text,
                     (window_width/2 - play_again_text_width/2, window_height/2 + 50))

# Основной игровой цикл

while True:
    # обработка состояния Game Over
    if game_over:
        pygame.display.flip()
        pygame.time.delay(1000)
        draw_game_over_screen()
        check_for_quit_event()
        # запустите обработку события, чтобы проверить выход
    else:
        game_window.fill(WHITE)#проверка белого фона
        # для выхода и нажатия мыши
        run_event_processing()
        # Проверить победу или ничью
        game_over = check_for_win_or_draw()
        draw_the_board()#нарисуйте игровое поле
        pygame.display.flip()#обновите экран

        # проверить, выиграл ли кто-нибудь после того,
        # как X был размещен
        if game_over:
            continue

        #ИИ идет сюда чтобы поставит О
        if X_placed:
            #Подождите 1/2 секунды, чтобы это выглядело
            #Так, будто ИИ думает
            pygame.time.delay(500)
            (O_placed, rowo, colo)=board.run_better_algorithm_to_place_O()
            if O_placed:
                letterO=LetterSprite(
                    'O',colo,rowo,
                    grid_width,
                    grid_height)
                group.add(letterO)
                O_placed = False

            game_over=board.check_if_anybody_won()
            #Снова нарисуйте доску, чтобы показать букву О
            #которую мы только что поставили
            draw_the_board()
            X_placed=False

        #обновите экран
        pygame.display.flip()

        #ограничить цикл до 60 кадров в секунду
        clock.tick(60)



pygame.quit()
