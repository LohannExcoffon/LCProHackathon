from ursina import *
import random
from time import sleep
from billboard import Billboard

# Create the Ursina app
app = Ursina()

# Define variables
player_speed = 5
last_update_time = time.time()
obstacle_speed = 5
spawn_interval = 1.5
lane_width = 2
lanes = [-lane_width, 0, lane_width]
score = 0  # Initialize the score

# Define obstacle colors and safe color
colors = [color.red, color.yellow, color.green]
safe_color = random.choice(colors)

score_text = Text(text=str(score), scale=2, position=(-0.7, 0.45), color=color.black)

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
    color=color.white,
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

# Define the billboard to show the safe color
billboard = Billboard(lane_width,color.black)

# List to keep track of obstacles
obstacles = []

# Adjust the camera position and rotation
camera.position = (0, 15, -25)  # Higher position, behind the player
camera.rotation_x = 30  # Tilt the camera down to look at the player


# Function to create a long obstacle with a color
def create_obstacle():
    global safe_color
    open_lane = random.choice(lanes)  # Choose a random lane to keep open
    for lane in lanes:
        # Assign the safe color to the lane that is open
        if lane == open_lane:
            obstacle_color = safe_color
        else:
            obstacle_color = random.choice(colors)  # Random color for other lanes

        obstacle = Entity(
            model='cube',
            color=obstacle_color,
            scale=(2, 1, 1),  # Slightly more than lane width to ensure coverage
            position=(lane, 0.5, 20),  # Adjusted Y position to match player level
            collider='box'
        )
        obstacles.append(obstacle)


# Function to update the game state
def update():
    global score, player_speed, last_update_time, obstacle_speed

    current_time = time.time()

    if current_time - last_update_time >= 1:
        obstacle_speed += 0.01  # Increase the speed
        last_update_time = current_time

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
            score_text.text = str(score)  # Update score display

    # Check for collisions
    for obstacle in obstacles:
        if player.intersects(obstacle).hit:
            if obstacle.color == safe_color:
                # Safe collision
                print(f"Safe Pass! Current Score: {score}")
            else:
                # Game over
                print(f"Game Over! Final Score: {score}")
                loseSound.play()
                sleep(loseSound.length)
                application.quit()


# Function to show the correct color on the billboard
def show_billboard_color():
    global safe_color
    safe_color = random.choice(colors)  # Randomly select a new safe color
    billboard.change_color(safe_color)  # Show the safe color on the billboard
    invoke(clear_billboard, delay=1.5)  # Clear the color after 1.5 seconds


# Function to clear the billboard color
def clear_billboard():
    billboard.change_color(color.clear) # Clear the billboard color


# Function to spawn obstacles periodically
def spawn_obstacles():
    create_obstacle()
    show_billboard_color()  # Show the safe color on the billboard each time
    invoke(spawn_obstacles, delay=spawn_interval)


# Creates sounds
gameSound = Audio(sound_file_name='gameSound.wav', volume=1, loop=True, autoplay=True)
loseSound = Audio(sound_file_name='loseSound.wav', volume=1, loop=False, loops=1, autoplay=False)

# Start the obstacle spawning
spawn_obstacles()

# Run the game
app.run()
