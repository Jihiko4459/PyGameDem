import pygame
from tkinter import messagebox
from TicTacToeCell import TicTacToeCell
from TicTacToeForPerverts2.SuperTicTacToeBoard import SuperTicTacToeBoard


def text(text: str):
    #   Преобразует заданную строку в pygame surface
    return font.render(text, True, BLACK)


# Определите цвета
WHITE=(255,255,255)
BLACK=(0,0,0)
# размеры игрового окна
screen_width = 800
screen_height = 800

# Инициализировать игру
pygame.init()
player2_img = pygame.image.load("images/player2.jpg")
pygame.display.set_icon(player2_img)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Крестики-нолики для извращенцев")

# Инициализировать игровое поле
board = SuperTicTacToeBoard(
    topleft=[100, 150], width=600
)

available_local_board = -1  #доступны все малые доски
mouse_pos = None  # значение mouse_pos равно None пока не произошёл щелчок мыши
first_player = 1
active_player = first_player  # первым ходит первый игрок
screen_bg_color = WHITE
title = "Крестики-нолики для извращенцев"



font = pygame.font.SysFont(name="comic sans ms",
                                 size=50)

player_text = text("Игрок ")
player_text_tl = (
    board.topleft[0],
    (board.topleft[1] - player_text.get_height()) // 2
)
active_player_icon = TicTacToeCell(
    topleft=(board.topleft[0] + player_text.get_width(),
            player_text_tl[1]),
    width=player_text.get_height()
)
active_player_icon.update(state=active_player)
# Определяет текстовые элементы для отображения информации о состоянии игры
# когда игра начнется, сообщите, кто из игроков по очереди (активен):
#   "Игрок {icon}, ваш ход!"
your_turn_text = text(", ваш ход!")
game_info_tl = (
   board.topleft[0] + player_text.get_width()
    + active_player_icon.width,
    player_text_tl[1]
)
# когда в игре определится победитель, сообщите, кто из игроков выиграл:
#   "Игрок {icon}, вы победили!"
winner_text = text(", вы победили!")
# когда игра закончится вничью, скажите игрокам, что игра окончена:
#   "Ничья!"
game_is_a_draw_text = text("Ничья!")










# Обновляет доступность текущего атрибута available_local_board
def update_availability(make_available: bool):#make_available: определяет доступность малых досок
    if board.winner():
        # если есть глобальный победитель, сделайте недоступными все местные доски объявлений.
        for local_board in board:
            local_board.update(state=-1)
    else:
        state = 0 if make_available else -1
        if available_local_board == -1:
            # обновите информацию о доступности всех местных досок объявлений
            for local_board in board:
                local_board.update(state=state)
        else:
            board[available_local_board].update(state=state)


#Чередуйте игроков 1 и 2 по очереди. Если в игре уже есть
# победитель, не меняйте значок активного игрока (это значок победителя).
def update_active_player():
    global active_player

    if board.winner() <= 0:  #  нет глобального победителя
        active_player = 1 if active_player == 2 else 2
        # также обновляется значок, который отображается в информации об игре (текст).
        active_player_icon.update(state=active_player)


# Положение последней выбранной ячейки определяет следующую доступную локальную ячейку.
# доска. Если на этой локальной доске уже есть победитель, становятся доступны все локальные доски
def update_available_local_board(local_board: int):
    #local_board: (индекс) следующего доступного местного совета директоров
    global available_local_board

    if board[local_board].winner():
        available_local_board = -1  # make all the boards available
    else:
        available_local_board = local_board


# Помечает данную ячейку для данного игрока. Проверяет состояние
# игры, как только ячейка помечена (глобальное вино, местное вино, локальный розыгрыш, то же самое)
# и соответствующим образом обновляет ее. Воспроизводит звук, если он включен.
def mark_cell(player: int, local_board: int, cell: int):
    # player: какой игрок помечает клетку
    # local_board: доска, к которой принадлежит ячейка
    # cell: ячейка, отмеченная данным игроком

    # Отметьте ячейку с данным игроком
    board.update(state=player, local_board=local_board, cell=cell)

    #проверьте состояние досок после того, как будет отмечена новая ячейка
    if board.winner() > 0:  # в игре есть победитель
        # установите, чтобы на экране отображался значок победителя
        active_player_icon.update(state=board.winner())

# Проверьте, не сталкивается ли курсор мыши с какой-либо доступной ячейкой. Если это
# так, обновите поле и параметры игры соответствующим образом, чтобы продолжить
# игра. Если mouse_pos щелкнет по недоступной ячейке или за пределами
# поля, ничего не делайте (дождитесь следующего щелчка мыши).
def process_turn():

    # 1) убедитесь, что мышь нажата на доступную ячейку
    local_board, cell = get_board_and_cell_from_mouse_pos()
    if local_board == -1 or cell == -1:
        # -1 означает, что ни одна доступная ячейка не была выбрана
        return

    # Если была выбрана свободная ячейка, выполните действия, необходимые для начала хода
    # 2) Сделайте недоступной локальную доску, которая была доступна в этот ход
    update_availability(make_available=False)
    # 3) Отметьте ячейку на доске
    mark_cell(player=active_player,
                    local_board=local_board,
                    cell=cell)
    # 4) Пусть неактивный игрок станет активным в следующий ход
    update_active_player()
    # 5) Установите, какая локальная доска будет доступна в следующий ход
    update_available_local_board(local_board=cell)
    # 6) Сделайте эти доски доступными
    update_availability(make_available=True)
    # 7) Следующий игрок готов к игре по очереди.

# Предполагая, что mouse_pos не равно None, проверьте, не совпадает ли позиция мыши
# с какой-либо доступной ячейкой. Возвращает cell_id и
# local_board_id, к которым относится ячейка.
# Если коллизия не обнаружена, верните (-1,-1)
def get_board_and_cell_from_mouse_pos():

    # два целых числа от 0 до 8, представляющих локальную доску и ячейку
    # возвращает значение (-1,-1), если мышь не задела ни одну доступную ячейку
    for local_board_id, local_board in enumerate(board):
        for cell_id, cell in enumerate(local_board):
            if cell.collidepoint(mouse_pos):
                if cell.available:
                    return local_board_id, cell_id
    return -1, -1


# Отображает информацию о состоянии игры. Если игра
# запущена, указывает, какой игрок занимает очередь. Если есть победитель, объявите его
# победитель. Если игра закончилась вничью, сообщите об этом игрокам.
def display_game_information(screen: pygame.Surface):
    # screen: игровая поверхность, на которой отображается текст

    if board.winner() >= 0:
        # если игра не закончилась вничью, укажите активного игрока или победителя
        screen.blit(player_text, player_text_tl)
        active_player_icon.draw(screen)
        if board.winner() > 0:  # активный игрок становится победителем
            screen.blit(winner_text, game_info_tl)

        else: # активный игрок - это игрок, делающий ход
            screen.blit(your_turn_text, game_info_tl)

    else:  # board.winner() == -1
        # игра завершилась вничью, активный игрок не отображается.
        screen.blit(game_is_a_draw_text, player_text_tl)


# Работает с вводимыми пользователем данными (щелчок правой кнопкой мыши).
# Возможные действия: выйти из игры, щелкнуть правой кнопкой мыши
# возвращает булево значение, указывающее, стоит ли выходить из игры
def process_events():
    global mouse_pos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

    return False

# Преобразует щелчки мыши пользователей в соответствующие изменения в игре
# Возможные действия: щелкните по ячейке, нажмите кнопку new_game
def run_logic():
    global mouse_pos

    if mouse_pos is None:
        return  # only react against the player's mouse clicks

    else:  # a cell has been selected
        process_turn()
    # return to default value, wait for the next mouse click
    mouse_pos = None
# Отображает игровые элементы на заданной поверхности.
def draw(screen: pygame.Surface) -> None:
    # screen: поверхность, на которой отображается игровой интерфейс
    screen.fill(screen_bg_color)
    board.draw(screen=screen)
    display_game_information(screen=screen)

    pygame.display.update()

# Запускает основной цикл для воспроизведения игры
clock = pygame.time.Clock()
done = False
while not done:
    done = process_events()
    run_logic()
    draw(screen=screen)
    clock.tick(60)
pygame.quit()


