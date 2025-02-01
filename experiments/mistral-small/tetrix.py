import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
COLORS = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (0, 255, 255)
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Game settings
fps = 10

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetrix Game')

# Create the game board
grid = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]

# Game variables
current_shape = random.choice(SHAPES)
current_color = random.randint(1, len(COLORS) - 1)
shape_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2
shape_y = 0
clock = pygame.time.Clock()
fall_time = 0

def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            color = COLORS[grid[y][x]]
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_shape(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                color = COLORS[current_color]
                pygame.draw.rect(screen, color, ((offset_x + x) * BLOCK_SIZE, (offset_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                try:
                    if grid[offset_y + y][offset_x + x]:
                        return True
                except IndexError:
                    return True
    return False

def join_shape():
    global current_shape, current_color, shape_x, shape_y
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell:
                grid[shape_y + y][shape_x + x] = current_color
    clear_rows()
    current_shape = random.choice(SHAPES)
    current_color = random.randint(1, len(COLORS) - 1)
    shape_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2
    shape_y = 0
    if check_collision(current_shape, shape_x, shape_y):
        run = False

def clear_rows():
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = len(grid) - len(new_grid)
    new_grid = [[0] * len(grid[0]) for _ in range(lines_cleared)] + new_grid
    for new_grid
    return new_grid

# Game loop
run = True
while run:
    screen.fill((0, 0, 0))
    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time / 1000 >= 1 / fps:
        fall_time = 0
        shape_y += 1
        if check_collision(current_shape, shape_x, shape_y):
            shape_y -= 1
            join_shape()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_x = shape_x - 1
                if not check_collision(current_shape, new_x, shape_y):
                    shape_x = new_x
            if event.key == pygame.K_RIGHT:
                new_x = shape_x + 1
                if not check_collision(current_shape, new_x, shape_y):
                    shape_x = new_x
            if event.key == pygame.K_DOWN:
                new_y = shape_y + 1
                if not check_collision(current_shape, shape_x, new_y):
                    shape_y = new_y
            if event.key == pygame.K_UP:
                new_shape = list(zip(*current_shape[::-1]))
                if not check_collision(new_shape, shape_x, shape_y):
                    current_shape = new_shape

    draw_grid()
    draw_shape(current_shape, shape_x, shape_y)
    pygame.display.flip()

pygame.quit()
