from tkinter import Grid
import pygame 
import random 

pygame.font.init()


#global variables 
screen_width  = 800
screen_height = 700 
play_width    = 300
play_height   = 600
block_size    = 30

top_left_x = (screen_width - play_width)
top_left_y = (screen_height - play_height)


#shapes 

S = [['.....',
      '......',
      '..00..',
      '.00...',
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

shapes = [S, Z , I , O , J , L, T]
shape_colors = [(178,102,255),(255,255,102),(102,102,255),(255,102,178),(255,102,102),(102,255,178),(153,204,255)]

class Piece(object):
    def __init__( self ,x ,y ,shape ):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 

# Drawing the grid

def create_grid(locked_pos={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
    for i  in range(len(grid)):
           for j in range (len(grid[i])):
               if (j,i) in locked_pos:
                 c  = locked_pos[(j,i)]
               grid[i][j] = c 
    return grid 

#getting random shape
def get_shape():
      global shapes, shape_colors
      return Piece(5,0,random.choice(shapes))

#draw all of the objects to the screen
def draw_text_middle(surface, text, size, color):
      surface.fill((0,0,0))
      
      font = pygame.font.Font("comicsans", size, bold = True)
      label = font.render(text, 1, color)

      surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2))

#draws grey grid lines 
def draw_grid(surface, grid):  
      sx = top_left_x
      sy = top_left_y

      for i in range(len(grid)):
            pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+i*block_size)) #horizontal lies
            for j in range(len(grid[i])): 
                  pygame.draw.line(surface, (128,128,128), (sx+j*block_size, sy), (sx+j*block_size, sy+play_height)) #vertical lines

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
      accepted_positions = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
      accepted_positions = [j for sub in accepted_positions for j in sub]
      formatted  = convert_shape_format(shape)

      for pos in formatted:
            if pos not in accepted_positions:
                  if pos[1] > -1:
                        return False
      
      return True

#check if user has lost the game/ check if any position in given list is above screen
def check_lost(positions):
      for pos in positions:
            x, y = pos
            if y < 1:
                 return True
      return False

def clear_rows():

#displays next falling shape on the right side of the screen
def draw_next_shape(shape, surface):
      font = pygame.font.Font('comicsans', 30)
      label = font.render('Next shape', 1, (255,255,255))

      sx = top_left_x + play_width + 50
      sy = top_left_y + play_height/2 - 100
      format = shape.shape[shape.rotation % len(shape.shape)]

      for i,line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                  if column == '0':
                        pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
      
      surface.blit(label, (sx + 10, sy - 30))

def update_score():

def max_score():

def draw_window():

def main(win):
      global Grid

      locked_position = {}
      grid = create_grid(locked_position)

      change_peice = False
      run = True 
      current_piece = get_shape()
      clock = pygame.time.Clock()
      fall_time = 0

      while run:

            fall_speed = 0.27

            grid = create_grid(locked_position)
            fall_time += clock.get_rawtime()
            clock.tick()

            #piece falling code
            if fall_time/1000 >= fall_speed:
                  fall_time = 0
                  current_piece.y += 1
                  if not valid_space(current_piece, grid) and current_piece.y > 0:
                        current_piece.y -= 1
                        change_piece = True

            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False
                        pygame.display.quit()
                        quit()
                  
                  if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                              current_piece.x -= 1
                              if not valid_space(current_piece, grid):
                                    current_piece.x += 1

                        elif event.key == pygame.K_RIGHT:
                              current_piece.x += 1
                              if not valid_space(current_piece, grid):
                                    current_piece.x -= 1
                        
                        elif event.key == pygame.K_UP:
                              current_piece.rotation = current_piece.rotation+1%len(current_piece.shape) #rotate shape
                              if not valid_space(current_piece, grid):
                                    current_piece.rotation-1%len(current_piece.shape)
                        
                        if event.key == pygame.K_DOWN:
                              current_piece.y += 1 #move shape down
                              if not valid_space(current_piece, grid):
                                    current_piece.y -= 1

            shape_pos = convert_shape_format(current_piece)

            #add color of piece to the grid for drawing
            for i in range(len(shape_pos)):
                  x, y  = shape_pos[i]
                  if y > -1: #if we are not aboove the screen
                        grid[y][x] = current_piece.color

            #if piece hits grouond
            if change_piece:
                  for pos in shape_pos:
                        p = (pos[0], pos[1])
                        locked_position[p] = current_piece.color
                  current_piece = next_piece
                  next_piece = get_shape()
                  change_piece = False 

            draw_window(win)

            draw_next_shape(next_piece, win)
            pygame.display.update()

            if check_lost(locked_position):
                  run = False

def main_menu():

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")



      







