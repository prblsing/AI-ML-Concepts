Here's a complete implementation of Tetris using Pygame:

```python
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_WIDTH = 300
GRID_HEIGHT = 600
BLOCK_SIZE = 30

TOP_LEFT_X = (SCREEN_WIDTH - GRID_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - GRID_HEIGHT - 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Tetromino shapes
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

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [GREEN, RED, CYAN, YELLOW, BLUE, ORANGE, PURPLE]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_pos:
                grid[y][x] = locked_pos[(x,y)]
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    
    return positions

def valid_space(piece, grid):
    accepted_pos = [[(x, y) for x in range(10) if grid[y][x] == BLACK] for y in range(20)]
    accepted_pos = [x for sub in accepted_pos for x in sub]
    
    formatted = convert_shape_format(piece)
    
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

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    
    surface.blit(label, (TOP_LEFT_X + GRID_WIDTH/2 - (label.get_width()/2), 
                         TOP_LEFT_Y + GRID_HEIGHT/2 - label.get_height()/2))

def draw_grid(surface, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], 
                             (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, 
                              BLOCK_SIZE, BLOCK_SIZE), 0)
    
    pygame.draw.rect(surface, WHITE, (TOP_LEFT_X, TOP_LEFT_Y, GRID_WIDTH, GRID_HEIGHT), 4)

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    
    return inc

def draw_next_shape(piece, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, WHITE)
    
    sx = TOP_LEFT_X + GRID_WIDTH + 50
    sy = TOP_LEFT_Y + GRID_HEIGHT/2 - 100
    format = piece.shape[piece.rotation % len(piece.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, 
                                 (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, 
                                  BLOCK_SIZE, BLOCK_SIZE), 0)

def draw_window(surface, grid, score=0, last_score=0):
    surface.fill(BLACK)
    
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, WHITE)
    
    surface.blit(label, (TOP_LEFT_X + GRID_WIDTH / 2 - label.get_width()/2, 30))
    
    # Current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, WHITE)
    
    sx = TOP_LEFT_X + GRID_WIDTH + 50
    sy = TOP_LEFT_Y + GRID_HEIGHT/2 - 100
    
    surface.blit(label, (sx + 20, sy + 160))
    
    draw_grid(surface, grid)
    pygame.draw.rect(surface, WHITE, (TOP_LEFT_X, TOP_LEFT_Y, GRID_WIDTH, GRID_HEIGHT), 4)

def main(win):
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
            if fall_speed > 0.12:
                fall_speed -= 0.005
        
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
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
        
        shape_pos = convert_shape_format(current_piece)
        
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 100
        
        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        
        if check_lost(locked_positions):
            draw_text_middle(win, "GAME OVER!", 80, WHITE)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

def main_menu(win):
    run = True
    while run:
        win.fill(BLACK)
        draw_text_middle(win, 'Press Any Key To Play', 60, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    
    pygame.display.quit()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')
main_menu(win)
```

This implementation includes:

1. All 7 classic Tetris pieces with correct colors and rotation logic
2. Score tracking
3. Increasing difficulty (speed) as time progresses
4. Next piece preview
5. Grid boundary visualization
6. Game over detection
7. Basic collision detection
8. Line clearing with score bonus
9. Controls:
   - Left/Right arrows to move
   - Up arrow to rotate
   - Down arrow to soft drop
   - Space for hard drop

To run the game:
1. Make sure you have Pygame installed (`pip install pygame`)
2. Save the code in a .py file
3. Run the script

The game features:
- Colorful blocks with different shapes
- Increasing difficulty as you play
- Score tracking
- Next piece preview
- Proper collision detection
- Line clearing mechanics
- Game over state

The game will start with a main menu and you can press any key to start playing. The pieces will gradually fall faster as time progresses, making the game more challenging.
