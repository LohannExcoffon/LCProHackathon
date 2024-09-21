import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Running Man")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_width, player_height = 40, 60
player_x, player_y = 50, HEIGHT - player_height - 20
player_speed_y = 0
jump_power = -15
gravity = 1

# Obstacle settings
obstacle_width, obstacle_height = 20, 60
obstacle_speed = 5
obstacle_gap = 200  # Gap between obstacles
obstacles = []

# Score
score = 0
font = pygame.font.SysFont(None, 36)


# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


# Function to create obstacles
def create_obstacle():
    obstacle_x = WIDTH + random.randint(0, 100)
    obstacle_y = HEIGHT - obstacle_height - 20
    return [obstacle_x, obstacle_y]


# Function to draw player
def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, [x, y, player_width, player_height])


# Function to draw obstacles
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, [obstacle[0], obstacle[1], obstacle_width, obstacle_height])


# Function to check collision
def check_collision(player_rect, obstacles):
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if player_rect.colliderect(obstacle_rect):
            return True
    return False


# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_y == HEIGHT - player_height - 20:
                player_speed_y = jump_power

    # Player movement
    player_speed_y += gravity
    player_y += player_speed_y
    if player_y > HEIGHT - player_height - 20:
        player_y = HEIGHT - player_height - 20
        player_speed_y = 0

    # Update obstacles
    if not obstacles or obstacles[-1][0] < WIDTH - obstacle_gap:
        obstacles.append(create_obstacle())
    for obstacle in obstacles:
        obstacle[0] -= obstacle_speed
    obstacles = [obs for obs in obstacles if obs[0] > -obstacle_width]

    # Check collision
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    if check_collision(player_rect, obstacles):
        print(f"Game Over! Final Score: {score}")
        pygame.quit()
        quit()

    # Draw player and obstacles
    draw_player(player_x, player_y)
    draw_obstacles(obstacles)

    # Update score
    score += 1
    display_score(score)

    # Update screen and tick clock
    pygame.display.update()
    clock.tick(FPS)

# Quit pygame
pygame.quit()