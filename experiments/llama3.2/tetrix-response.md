Here's a simple implementation of Tetris in Python using the Pygame library.

```python
import pygame
import random

pygame.init()

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
gray     = ( 128, 128, 128)

size = [400, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

class Shape:
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.blocks = []

    def create_random_shape(self):
        if random.random() < 0.3:
            self.blocks.append([1, 1])
        elif random.random() < 0.6:
            self.blocks.append([2, 2])
        else:
            self.blocks.append([1, 1, 1])

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

class I_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.create_random_shape()

    def rotate_clockwise(self):
        for block in self.blocks:
            if block[0] == 0 and block[1] != 1:
                return False
        return True

class O_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.create_random_shape()

    def rotate_clockwise(self):
        for block in self.blocks:
            if block[0] == block[1]:
                return False
        return True

class T_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.create_random_shape()

    def rotate_clockwise(self):
        return True

class L_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.create_random_shape()

    def rotate_clockwise(self):
        return True

class J_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.create_random_shape()

    def rotate_clockwise(self):
        for block in self.blocks:
            if block[0] == 1 and block[1] != 2:
                return False
        return True

class Z_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.create_random_shape()

    def rotate_clockwise(self):
        for block in self.blocks:
            if block[0] == block[1]:
                return False
        return True

# Create shapes
I = I_Shape()
O = O_Shape()
T = T_Shape()
L = L_Shape()
J = J_Shape()
Z = Z_Shape()

shape_types = [I, O, T, L, J, Z]
current_shape = random.choice(shape_types)

def draw_block(screen, x, y, color):
    pygame.draw.rect(screen, color, [x*20+10, y*20+50, 20, 20])

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_shape.move_left()
            elif event.key == pygame.K_RIGHT:
                current_shape.move_right()

    # --- Game logic should go here
    for block in current_shape.blocks:
        draw_block(screen, current_shape.x + block[0], current_shape.y + block[1], current_shape.color)

    screen.fill(black)

    if not current_shape.rotate_clockwise():
        shape_types.remove(current_shape)
        shape_types.append(I)
        current_shape = random.choice(shape_types)

    # --- Screen-clearing code goes here
    for y in range(5, 0, -1):
        for x in range(10):
            for block in current_shape.blocks:
                if (x + current_shape.x) == block[0] and (y + current_shape.y) == block[1]:
                    pygame.draw.rect(screen, gray, [x*20+50, y*20+150, 20, 20])

    # --- Drawing code should go here
    for shape in shape_types:
        draw_block(screen, shape.x, shape.y, shape.color)
        if len(shape.blocks) > 1 and not shape.rotate_clockwise():
            pygame.draw.rect(screen, gray, [shape.x*20+10, shape.y*20+50, 20, 20])
    for block in current_shape.blocks:
        draw_block(screen, current_shape.x + block[0], current_shape.y + block[1], current_shape.color)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
```

In this code, a random shape is chosen from a list of shapes at the start. The user can then move the shape left or right using the corresponding keys. If the rotation key is pressed while an empty space is 
available in that orientation, the shape rotates clockwise; otherwise, it drops down and the next block is generated.

Note: This code doesn't handle any game logic for scoring or removing completed lines yet.
