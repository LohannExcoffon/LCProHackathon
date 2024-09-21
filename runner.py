from ursina import *
import random

# Create the Ursina app
app = Ursina()

# Define variables
player_speed = 5
obstacle_speed = 5
spawn_interval = 1.5
lane_width = 2
lanes = [-lane_width, 0, lane_width]
score = 0  # Initialize the score

# Define the player entity
player = Entity(
    model='cube',
    color=color.azure,
    scale=(1, 1, 1),
    position=(0, 0.5, -5),
    collider='box'
)

# Define the ground
ground = Entity(
    model='plane',
    scale=(50, 1, 50),
    color=color.light_gray,
    texture='white_cube',
    texture_scale=(50, 50),
    collider='box'
)

# Define side walls for aesthetics at the edges of the player's movement range
left_wall = Entity(
    model='cube',
    color=color.dark_gray,
    scale=(0.5, 5, 50),  # Make the wall thinner
    position=(-lane_width - 0.8, 2.5, 0)  # Positioned just outside the left lane
)

right_wall = Entity(
    model='cube',
    color=color.dark_gray,
    scale=(0.5, 5, 50),  # Make the wall thinner
    position=(lane_width + 0.8, 2.5, 0)  # Positioned just outside the right lane
)

# List to keep track of obstacles
obstacles = []

# Adjust the camera position and rotation
camera.position = (0, 15, -25)  # Higher position, behind the player
camera.rotation_x = 30  # Tilt the camera down to look at the player


# Function to create a long obstacle with only one open lane
def create_obstacle():
    open_lane = random.choice(lanes)  # Choose a random lane to keep open
    for lane in lanes:
        if lane != open_lane:  # Create obstacles on all lanes except the open one
            obstacle = Entity(
                model='cube',
                color=color.red,
                scale=(2, 1, 1),  # Slightly more than lane width to ensure coverage
                position=(lane, 0.5, 20),  # Adjusted Y position to match player level
                collider='box'
            )
            obstacles.append(obstacle)


# Function to update the game state
def update():
    global score

    # Player movement
    if held_keys['a']:
        player.x -= time.dt * player_speed
    if held_keys['d']:
        player.x += time.dt * player_speed

    # Keep player within lanes
    player.x = max(-lane_width, min(lane_width, player.x))

    # Update obstacles
    for obstacle in obstacles:
        obstacle.z -= time.dt * obstacle_speed
        if obstacle.z < -10:
            obstacles.remove(obstacle)
            destroy(obstacle)
            score += 1  # Increase score as obstacles pass by

    # Check for collisions
    for obstacle in obstacles:
        if player.intersects(obstacle).hit:
            print(f"Game Over! Final Score: {score}")
            application.quit()


# Function to spawn obstacles periodically
def spawn_obstacles():
    create_obstacle()
    invoke(spawn_obstacles, delay=spawn_interval)


# Start the obstacle spawning
spawn_obstacles()

# Run the game
app.run()




