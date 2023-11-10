import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the box's initial position and velocity
x, y = 0, 0
x_vel, y_vel = 2, 2

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOX_COLOR = (0, 0, 255)
BOX_SIZE = 10

# Initialize the list of previous positions
prev_positions = []

# Function to change the box color
def change_box_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Main loop
running = True
while running:
    # Clear the screen
    screen.fill(WHITE)

    # Move the box
    x += x_vel
    y += y_vel

    # Check for collisions with the screen edges
    if x + BOX_SIZE >= WIDTH or x <= 0:
        x_vel = -x_vel
        BOX_COLOR = change_box_color()
    if y + BOX_SIZE >= HEIGHT or y <= 0:
        y_vel = -y_vel
        BOX_COLOR = change_box_color()

    # Draw the lines
    prev_positions.append((x, y))
    if len(prev_positions) > 1:
        pygame.draw.lines(screen, BOX_COLOR, False, prev_positions, 1)

    # Draw the box
    pygame.draw.rect(screen, BOX_COLOR, (x, y, BOX_SIZE, BOX_SIZE))

    # Update the display
    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit