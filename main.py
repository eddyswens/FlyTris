from doctest import debug
import pygame
import random
import time

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

fall_speeds = { 0: 8, 
                1: 7,
                2: 6,
                3: 5,
                4: 4,
                5: 4,
                6: 3,
                7: 2,
                8: 1,
                9: 1,
                10: 1,
                11: 1,
                12: 1,
                13: 1,
                14: 1,
                15: 1,
                16: 1,
                17: 1,
                18: 1   }

scores_from_num_of_lines = {1: 40,
                            2: 100,
                            3: 300,
                            4: 1200 }

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30

# Скорость выражается в тиках на одну клетку (60 тиков в секунду +-2 тика)
FPS = 20

START_LEVEL = 0
FALL_SPEED = fall_speeds[START_LEVEL] # in ticks
ARR = 1 # in ticks
DAS = 4 # in ticks
SOFT_DROP_SPEED = 1 # in ticks

GAMEPAD_CONTROL = False

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# COLORS DICT
colors = {
    "red" : (255, 0, 0),
    "blue" : (0, 0, 255)
}

# SHAPE FORMATS

S = [['.....',
      '..00.',
      '.00..',
      '.....',
      '.....'],

     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....'],
      
     ['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
      
     ['.....',
      '.0...',
      '.00..',
      '..0..',
      '.....']]

Z = [['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],

     ['.....',
      '...0.',
      '..00.',
      '..0..',
      '.....'],

     ['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],

     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '0000.',
      '.....',
      '.....',
      '.....'],

     ['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],

     ['.....',
      '.....',
      '0000.',
      '.....',
      '.....'],

     ['.0...',
      '.0...',
      '.0...',
      '.0...',
      '.....']]

O = [['.....',
      '.00..',
      '.00..',
      '.....',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],

     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],

     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],

     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],

     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],

     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],

     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],

     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],

     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],

     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
# shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]
shape_colors = [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (0, 0, 255), (0, 0, 255), (0, 0, 255)]
# index 0 - 6 represent shape

NUMS = [
    [[1, 1, 1],
     [1, 0, 1],
     [1, 0, 1],
     [1, 0, 1],
     [1, 1, 1]],

    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 0],
     [0, 1, 0],
     [1, 1, 1]],

    [[1, 1, 1],
     [0, 0, 1],
     [1, 1, 1],
     [1, 0, 0],
     [1, 1, 1]],

    [[1, 1, 1],
     [0, 0, 1],
     [1, 1, 1],
     [0, 0, 1],
     [1, 1, 1]],

    [[1, 0, 1],
     [1, 0, 1],
     [1, 1, 1],
     [0, 0, 1],
     [0, 0, 1]],

    [[1, 1, 1],
     [1, 0, 0],
     [1, 1, 1],
     [0, 0, 1],
     [1, 1, 1]],

    [[1, 1, 1],
     [1, 0, 0],
     [1, 1, 1],
     [1, 0, 1],
     [1, 1, 1]],

    [[1, 1, 1],
     [0, 0, 1],
     [0, 0, 1],
     [0, 0, 1],
     [0, 0, 1]],

    [[1, 1, 1],
     [1, 0, 1],
     [1, 1, 1],
     [1, 0, 1],
     [1, 1, 1]],

    [[1, 1, 1],
     [1, 0, 1],
     [1, 1, 1],
     [0, 0, 1],
     [1, 1, 1]]
]

# Инициализация геймпадов
pygame.joystick.init()

# Проверка наличия подключенных геймпадов
if pygame.joystick.get_count() == 0:
    print("Нет подключенных геймпадов")
    GAMEPAD_CONTROL = False
else:
    # Подключение к первому найденному геймпаду
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Подключен геймпад:", joystick.get_name())
    GAMEPAD_CONTROL = True


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_soft_dropping = False


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

def create_mat(row, cols):
    return [[0 for x in range(cols)] for x in range(row)]


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False 


def get_shape():
    global shapes, shape_colors

    shape_from_heap = Piece(5, 0, random.choice(shapes))
    i = shapes.index(shape_from_heap.shape)

    shapes.pop(i)
    shape_colors.pop(i)
    
    if len(shapes) == 0:
        shapes = [S, Z, I, O, J, L, T]
        # shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]
        shape_colors = [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (0, 0, 255), (0, 0, 255), (0, 0, 255)]

    return shape_from_heap


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
    top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30),
                         (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))  # vertical lines

def clear_rows(grid, locked):
    inc = 0
    cleared_rows = []

    # Проход по строкам сетки в обратном порядке (снизу вверх)
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            cleared_rows.append(i)
            # Удаление позиций из locked
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    # Сдвиг строк вниз
    if inc > 0:
        # Проход по всем заблокированным позициям в порядке их y-координаты (сверху вниз)
        for i in range(len(grid) - 1, -1, -1):
            if i in cleared_rows:
                continue
            # Количество очищенных строк ниже текущей позиции
            shift = sum(1 for row in cleared_rows if row > i)
            if shift > 0:
                for j in range(len(grid[i])):
                    if (j, i) in locked:
                        locked[(j, i + shift)] = locked.pop((j, i))

    return inc

def draw_stats(scr, lvl, surface):
    font = pygame.font.SysFont('comicsans', 30)
    score_label = font.render(f"Score: {scr}", 1, (255, 255, 255))
    level_label = font.render(f"Level: {lvl}", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy1 = top_left_y + play_height / 2
    sy2 = sy1 + 100

    surface.blit(score_label, (sx, sy1))
    surface.blit(level_label, (sx, sy2))



def draw_next_shape(shape, surface):
    nextShapeMat = [[0 for j in range(5)] for i in range(5)]

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 200
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)
                nextShapeMat[i][j] = 1
    # print(nextShapeMat)
    surface.blit(label, (sx + 10, sy - 30))
    return nextShapeMat


def draw_window(surface):
    surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()

def get_global_time():
    return round(time.time() * 1000)


def main():
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    level_time = 0
    score = 0
    das_timer = 0
    mov_timer = 0

    ticks = 0
    fall_timer = 0
    soft_drop_timer = 0
    soft_drop_allowed = True
    is_das_delay = False
    is_moving_allowed = True
    lines_cleared = 0
    current_level = 0

    button_down_pressed = False
    button_right_pressed = False
    button_left_pressed = False

    global_time_now = get_global_time()
    last_update_global_time = global_time_now
    last_send_global_time = global_time_now

    next_color_to_send = "red"
    grid_updated = False
    grid_to_send = create_mat(20, 10)
    next_shape_to_send = create_mat(5, 5)
    score_to_send = 0

    while run:
        global_time_now = get_global_time()
        if global_time_now - last_update_global_time >= 100:
            last_update_global_time = get_global_time()

            # Создание сетки
            grid = create_grid(locked_positions)


            # Таймеры и счетчики
            # Получить количество мс между двумя тиками
            level_time += clock.get_time()
            if level_time > 1000:
                level_time = 0
                ticks = 1

            clock.tick_busy_loop()
            ticks += 1

            # Таймер при активации Soft Drop
            if not soft_drop_allowed:
                if soft_drop_timer >= SOFT_DROP_SPEED:
                    soft_drop_timer = 0
                    soft_drop_allowed = True
                else:
                    soft_drop_timer += 1
            
            # Таймер при активации DAS
            if is_das_delay:
                if das_timer >= DAS:
                    das_timer = 0
                    is_das_delay = False
                else:
                    das_timer += 1

            # Таймер при активации ARR
            if not is_moving_allowed:
                if mov_timer >= ARR:
                    mov_timer = 0
                    is_moving_allowed = True
                else:
                    mov_timer += 1

            # Падение фигуры
            if not current_piece.is_soft_dropping:
                if fall_timer >= FALL_SPEED:
                    fall_timer = 0
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                        current_piece.y -= 1
                        change_piece = True
                else:
                    fall_timer += 1


            # Обработка произошедших за тик событий
            for event in pygame.event.get():

                # ВЫХОД
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()

                # ГЕЙМПАД-КРЕСТОВИНА-НАЖАТИЕ
                if event.type == pygame.JOYHATMOTION:
                    # Крестовина влево - смещение влево
                    if event.value[0] == -1:
                        current_piece.is_moving_left = True
                        is_das_delay = True
                        button_left_pressed = True
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1

                    # Крестовина вправо - смещение вправо 
                    if event.value[0] == 1:
                        current_piece.is_moving_right = True
                        is_das_delay = True
                        button_right_pressed = True
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1

                    # Крестовина вниз - софтдроп
                    if event.value[1] == -1:
                        button_down_pressed = True

                    # Крестовина вверх - харддроп
                    if event.value[1] == 1:
                        hard_drop = True
                        while hard_drop:
                            current_piece.y += 1
                            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                                current_piece.y -= 1
                                change_piece = True
                                hard_drop = False
                    
                    if event.value == (0, 0):
                        button_down_pressed = False
                        button_left_pressed = False
                        button_right_pressed = False
                        current_piece.is_moving_right = False
                        current_piece.is_moving_left = False

                # ГЕЙМПАД-КНОПКИ-НАЖАТИЕ
                if event.type == pygame.JOYBUTTONDOWN:
                    # RESTART ON START
                    if event.button == 9:
                        run = False
                    # Кнопка B - нажатие 
                    if event.button == 1:
                        # Вращать фигуру по часовой
                        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                        if not valid_space(current_piece, grid):
                            current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                    # Кнопка А - нажатие 
                    if event.button == 0:
                        # Вращать фигуру против часовой
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                        if not valid_space(current_piece, grid):
                            current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)

                # КЛАВИАТУРА-НАЖАТИЕ
                if event.type == pygame.KEYDOWN:
                    # RESTART ON ESCAPE
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    # Стрелка влево - нажатие
                    elif event.key == pygame.K_LEFT:
                        current_piece.is_moving_left = True
                        is_das_delay = True
                        button_left_pressed = True
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    # Стрелка вправо - нажатие 
                    elif event.key == pygame.K_RIGHT:
                        current_piece.is_moving_right = True
                        is_das_delay = True
                        button_right_pressed = True
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    # Стрелка вниз - нажатие
                    elif event.key == pygame.K_DOWN:
                        button_down_pressed = True
                    # Стрелка вверх - нажатие 
                    elif event.key == pygame.K_UP:
                        hard_drop = True
                        while hard_drop:
                            current_piece.y += 1
                            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                                current_piece.y -= 1
                                change_piece = True
                                hard_drop = False
                    # x - нажатие 
                    if event.key == pygame.K_x:
                        # Вращать фигуру по часовой
                        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                        if not valid_space(current_piece, grid):
                            current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                    # z - нажатие 
                    if event.key == pygame.K_z:
                        # Вращать фигуру против часовой
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                        if not valid_space(current_piece, grid):
                            current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)

                # КЛАВИАТУРА-ОТПУСК
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:  # Стрелка влево - отпуск
                        current_piece.is_moving_left = False
                        button_left_pressed = False
                    elif event.key == pygame.K_RIGHT:  # Стрелка вправо - отпуск
                        current_piece.is_moving_right = False
                        button_right_pressed = False
                    elif event.key == pygame.K_DOWN:
                        button_down_pressed = False

            # --------------------------!!!--------------------------
            # Движение по удерживанию стрелки вниз находится без условия движения, 
            # по скольку у нее отсутсвуют такие задержки, как ARR и DAS
            # --------------------------!!!--------------------------

            # Ускоренное движение вниз при удержании - софтдроп
            if soft_drop_allowed:
                if button_down_pressed:
                    current_piece.is_soft_dropping = True
                    current_piece.y += 1
                    soft_drop_allowed = False
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                        change_piece = True
                else:
                    current_piece.is_soft_dropping = False

            # Условие движения фигуры при удержании вправо/влево
            allow_move_while_pressed = (current_piece.is_moving_left or current_piece.is_moving_right) and not is_das_delay and is_moving_allowed and current_piece.y > 1        
            if allow_move_while_pressed:
                # Движение влево при удержании
                if button_left_pressed:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                    is_moving_allowed = False
                # Движение вправо при удержании
                if button_right_pressed:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                    is_moving_allowed = False

            # Конвертация фигуры в список занимаемых позиций для добавляения в сетку
            shape_pos = convert_shape_format(current_piece)

            # Добавить фигуру в общую сетку
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color

            # Если фигура приземлилась - необходимо сменить фигуру 
            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = get_shape()
                change_piece = False

                # Проверка на необходимость очищения строки и добавление очков и уровня
                current_lines_out = clear_rows(grid, locked_positions)
                lines_cleared += current_lines_out
                if current_lines_out:
                    score += scores_from_num_of_lines[current_lines_out] * (current_level + 1)
                    current_level = lines_cleared // 10
                    print(f"Score is {score}")
                    print(f"Level is {current_level}")

            

            draw_window(win)
            nextShapeMat = draw_next_shape(next_piece, win)
            draw_stats(score, current_level, win)
            pygame.display.update()

            # Проверка на проигрыш
            if check_lost(locked_positions):
                run = False

            grid_updated = True 
    
        # --------------------------!!!--------------------------
        # INTERACTIVE MOMENTS - 20 FPS
        # --------------------------!!!--------------------------
        
        if global_time_now - last_send_global_time >= 50:
            # try:
            #     print(1000/(global_time_now - last_send_global_time))  # DEBUG - CHECK FPS FOR SENDING
            # except:
            #     pass
            last_send_global_time = get_global_time()

            if grid_updated:
                grid_to_send = grid.copy()
                next_shape_to_send = nextShapeMat.copy()
                score_to_send = score
                grid_updated = False

            current_color = next_color_to_send
            if current_color == "red":
                next_color_to_send = "blue"
            else:
                next_color_to_send = "red"

            next_shape_matrix = generate_next_shape_mat(next_shape_to_send)
            score_matrix = generate_score_mat(score_to_send)

            packet_send(grid_to_send, next_shape_matrix,  current_color)

        # --------------------------!!!--------------------------
        # INTERACTIVE MOMENTS END
        # --------------------------!!!--------------------------


        # --------------------------!!!--------------------------
        # DEBUG
        # --------------------------!!!--------------------------

        # try:
        #     print(1000/(level_time - last_time))  # DEBUG - CHECK FPS FOR UPDATING GAME
        # except:
        #     pass
        # last_time = level_time

        # --------------------------!!!--------------------------
        # DEBUG END
        # --------------------------!!!--------------------------

    draw_text_middle("You Lost", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(500)

def horizontal_concat(matrix1, matrix2):
    return [row1 + row2 for row1, row2 in zip(matrix1, matrix2)]

def packet_send(main_matrix, next_shape_mat, color):
    singleColorMat = color2flagMat(main_matrix, color)  # Выделяем из всей матрицы только фигуры нужного цвета
    scaledMainMat = scaleMat(singleColorMat)
    scaledNextShapeMat = scaleMat(next_shape_mat)  # ЗДЕСЬ ОТПРАВКА

def generate_next_shape_mat(mat):
    return [row[0:4] for row in mat[1:3]]

def generate_score_mat(score):
    score_mat = create_mat(5, 3)
    first = score % 10
    second = (score//10) % 10
    third = (score//100) % 10
    fourth = score//1000
    score_mat = horizontal_concat(NUMS[fourth], NUMS[third])
    score_mat = horizontal_concat(score_mat, NUMS[second])
    score_mat = horizontal_concat(score_mat, NUMS[first])
    print(score_mat)


def scaleMat(mat):
    rows = len(mat)
    cols = len(mat[0])
    scaledMat = create_mat(rows*2, cols*2)
    for row in range(rows):
        for col in range(cols):
            val = mat[row][col]
            scaledMat[2*row][2*col] = val
            scaledMat[2*row+1][2*col] = val
            scaledMat[2*row][2*col+1] = val
            scaledMat[2*row+1][2*col+1] = val
    return scaledMat

    
def color2flagMat(colorMat, color):
    flagMat = create_mat(20, 10)
    color_to_find = colors[color]
    for row in range(20):
        for col in range(10):
            if colorMat[row][col] == color_to_find:
                flagMat[row][col] = 1
            else:
                flagMat[row][col] = 0
    return flagMat


def color2binaryMat(colorMat):
    binaryMat = create_mat(20, 10)
    for row in range(20):
        for col in range(10):
            if colorMat[row][col] == (0, 0, 0):
                binaryMat[row][col] = 0
            else:
                binaryMat[row][col] = 1
    return binaryMat


def main_menu():
    run = True
    while run:

        win.fill((0, 0, 0))
        draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYAXISMOTION:
                main()

    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game