import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
FPS = 10

# Colors
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# Tetromino Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        self.grid = [[(0, 0, 0) for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_piece = Tetromino()
        self.score = 0
        self.running = True

    def check_collision(self, dx=0, dy=0, shape=None):
        if shape is None:
            shape = self.current_piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_piece.x + x + dx
                    new_y = self.current_piece.y + y + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and self.grid[new_y][new_x] != (0, 0, 0)):
                        return True
        return False

    def place_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = Tetromino()
        if self.check_collision():  # Check if new piece immediately collides
            self.running = False

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == (0, 0, 0) for cell in row)]
        cleared = ROWS - len(new_grid)
        self.grid = [[(0, 0, 0) for _ in range(COLUMNS)] for _ in range(cleared)] + new_grid
        self.score += cleared * 10

    def move(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
        elif dy:
            self.place_piece()

    def rotate_piece(self):
        new_shape = [list(row) for row in zip(*self.current_piece.shape[::-1])]
        if not self.check_collision(shape=new_shape):
            self.current_piece.shape = new_shape

    def draw(self, screen):
        screen.fill((0, 0, 0))
        # Draw grid
        for y in range(ROWS):
            for x in range(COLUMNS):
                pygame.draw.rect(screen, self.grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0 if self.grid[y][x] != (0, 0, 0) else 1)
        # Draw current piece
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece.color, ((self.current_piece.x + x) * GRID_SIZE, (self.current_piece.y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def update(self):
        self.move(0, 1)

# Main Game Loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Tetris()
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
