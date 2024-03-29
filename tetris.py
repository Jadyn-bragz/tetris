import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 700
s_height = 700
play_width = 300 # meaning 300 // 10 = 30 width per block
play_height = 600 # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = 50 #(s_width - play_width) // 2
top_left_y = 50 #s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
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
shape_colors = [(178,102,255),(255,255,102),(102,102,255),(255,102,178),(255,102,102),(102,255,178),(153,204,255)]



class Piece(object):  
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

 

# Drawing the grid 
def create_grid(locked_pos={}):  
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid

#convert shape format to list of positions we can return
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


#making sure shapes are moving into a valid space 
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False

#getting random shape
def get_shape():
    return Piece(5, 0, random.choice(shapes))


#draw all of the objects to the screen
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("Algerian", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (400 - (label.get_width()/2), 300))


#draws grey grid lines 
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


#check if user has lost the game/ check if any position in given list is above screen
def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

#displays next falling shape on the right side of the screen
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Algerian', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score, last_score):
    surface.fill((0, 0, 102))

    pygame.font.init()
    font = pygame.font.SysFont('Algerian', 30)
    label = font.render('Tetris', 1, (153, 153, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 15))

    font = pygame.font.SysFont('Algerian', 20)
    label = font.render('Score: ' + str(score), 1, (153, 153, 255))

    sx = top_left_x + play_width + 30
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    label = font.render('High Score: ' + last_score, 1, (153, 153, 255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    #pygame.display.update()


def main(win):  
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_SPACE:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)


#add color of piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

 #if piece hits grouond
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):  
    run = True
    while run:
        win.fill((0,0,102))
        pygame.font.init()

        pygame.draw.rect(win, (0,204,204), (25, 25, 650, 650), 5)

        x, y = pygame.mouse.get_pos()

        titleFont = pygame.font.SysFont('Algerian', 50)
        font = pygame.font.SysFont('Algerian', 30)

        label = titleFont.render('Tetris', 1, (0,204,204))
        win.blit(label, (350 - label.get_width()/2, 250))

        start_label = font.render('START', 1, (0,0,0))
        quit_label = font.render('QUIT', 1, (0,0,0))

        if (200 - start_label.get_width()/2 - 10) <= x <= (200 + start_label.get_width()/2 + 10) and (400 - start_label.get_height()/2 - 10) <= y <= (400 + start_label.get_height()/2 + 10):
            pygame.draw.rect(win, (0,0,204), (200 - start_label.get_width()/2 - 10, 400 - start_label.get_height()/2 + 10, 115, 54))
        else:
            pygame.draw.rect(win, (51,153,255), (200 - start_label.get_width()/2 - 10, 400 - start_label.get_height()/2 + 10, 115, 54))

        if (500 - 115/2) <= x <= (500 + 115/2) and (400 - quit_label.get_height()/2 - 10) <= y <= (400 + quit_label.get_height()/2 + 10):
            pygame.draw.rect(win, (0,0,204), (500 - 115/2, 400 - quit_label.get_height()/2 + 10, 115, 54))
        else:
            pygame.draw.rect(win, (51,153,255), (500 - 115/2, 400 - quit_label.get_height()/2 +  10, 115, 54))

        win.blit(start_label, (200 - start_label.get_width()/2, 400))
        win.blit(quit_label , (500 - quit_label.get_width()/2, 400))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (200 - start_label.get_width()/2 - 115/2) <= x <= (200 + start_label.get_width()/2 + 115/2) and (400 - start_label.get_height()/2 - 54/2) <= y <= (400 + start_label.get_height()/2 + 54/2):
                    main(win)
                elif (500 - quit_label.get_width()/2 - 115/2) <= x <= (500 + quit_label.get_width()/2 + 115/2) and (400 - quit_label.get_height()/2 - 54/2) <= y <= (400 + quit_label.get_height()/2 + 54/2):
                    pygame.quit()

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)
      







