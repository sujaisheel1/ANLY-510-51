import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
TILE_SIZE = WIDTH // COLS

# Colors
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pac-Man with Bombs")

# Create pellets at grid positions
pellets = {(x, y) for x in range(COLS) for y in range(ROWS)}

# Generate random bomb positions (avoid starting point)
num_bombs = 10
bombs = set()
while len(bombs) < num_bombs:
    pos = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
    if pos != (0, 0):
        bombs.add(pos)
        pellets.discard(pos)  # remove pellet if bomb is there

# Initial Pac-Man position
pacman_pos = [0, 0]
score = 0
font = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()

def draw():
    screen.fill(BLACK)

    # Draw pellets
    for (x, y) in pellets:
        pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2), 5)

    # Draw bombs
    for (x, y) in bombs:
        pygame.draw.circle(screen, RED, (x * TILE_SIZE + TILE_SIZE//2, y * TILE_SIZE + TILE_SIZE//2), 10)

    # Draw Pac-Man
    pygame.draw.circle(screen, YELLOW, (pacman_pos[0] * TILE_SIZE + TILE_SIZE//2, pacman_pos[1] * TILE_SIZE + TILE_SIZE//2), TILE_SIZE // 2 - 4)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLUE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

def game_over_screen(message, color):
    screen.fill(BLACK)
    msg = font.render(message, True, color)
    screen.blit(msg, (WIDTH // 2 - 80, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Game loop
running = True
while running:
    clock.tick(10)  # 10 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and pacman_pos[0] > 0:
        pacman_pos[0] -= 1
    elif keys[pygame.K_RIGHT] and pacman_pos[0] < COLS - 1:
        pacman_pos[0] += 1
    elif keys[pygame.K_UP] and pacman_pos[1] > 0:
        pacman_pos[1] -= 1
    elif keys[pygame.K_DOWN] and pacman_pos[1] < ROWS - 1:
        pacman_pos[1] += 1

    # Bomb collision
    if tuple(pacman_pos) in bombs:
        game_over_screen("💣 Game Over! You hit a bomb!", RED)
        break

    # Eat pellets
    if tuple(pacman_pos) in pellets:
        pellets.remove(tuple(pacman_pos))
        score += 10

    # Win condition
    if not pellets:
        game_over_screen("🎉 You Win!", YELLOW)
        break

    draw()

pygame.quit()
sys.exit()
