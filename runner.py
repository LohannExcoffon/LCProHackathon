from ursina import *
import random
from time import sleep
from billboard import Billboard
from obstacle import Obstacle
from player import Player

# Create the Ursina app
app = Ursina()

window.fullscreen = False
window.size = (1152, 720)
window.borderless = False  # Ensure the window has borders
window.show_entity_count = False 
window.update_aspect_ratio()

# Define variables
player_speed = 5
last_update_time = time.time()
obstacle_speed = 5
spawn_interval = 2
lane_width = 2
lanes = [-lane_width, 0, lane_width]
score = 0  # Initialize the score
passed = False

# Define obstacle colors and safe color
color_map = {1:Vec4(186/255, 23/255, 143/255, 1), 2:Vec4(77/255, 32/255, 203/255, 1), 3:Vec4(37/255, 150/255, 215/255, 1)}
safe_color = random.choice(list(color_map.keys()))

# Define the player entity
player = Player(0,0.5,-5,(1,1,1))

# Define the ground
ground = Entity(
    model='plane',
    scale=(50, 1, 50),
    color=color.white,
    texture = 'floor.jpg',
    collider='box'
)

# Define side walls for aesthetics at the edges of the player's movement range
left_wall = Entity(
    model='cube',
    color=color.dark_gray,
    texture = 'wall.jpg',
    scale=(0.5, 5, 50),  # Make the wall thinner
    position=(-lane_width - 0.8, 2.5, 0)  # Positioned just outside the left lane
)

right_wall = Entity(
    model='cube',
    color=color.dark_gray,
    texture = 'wall.jpg',
    scale=(0.5, 5, 50),  # Make the wall thinner
    position=(lane_width + 0.8, 2.5, 0)  # Positioned just outside the right lane
)

# Define the billboard to show the safe color
billboard = Billboard(lane_width,color_map[safe_color])


camera.position = (0, 15, -25)  # Higher position, behind the player
camera.rotation_x = 30  # Tilt the camera down to look at the player
score_text = Text(text="Score: "+str(score), scale=2, position=(-0.7, 0.45,-0.05), color=color.white, font='assets/Orbitron-Bold.ttf',parent=camera.ui)
name_text = Text(text="AstroRun", scale=2, position=(0.35, 0.45,-0.05), color=color.white, font='assets/Orbitron-Bold.ttf',parent=camera.ui)

# List to keep track of obstacles
obstacles = []
# Function to create a long obstacle with a color
def create_obstacle():
    global safe_color
    open_lane = random.choice(lanes)  # Choose a random lane to keep open

    # Shuffle the colors to ensure three different colors
    row_colors = list(color_map.values())
    random.shuffle(row_colors)

    for i, lane in enumerate(lanes):
        # Assign the safe color to the lane that is open
        if lane == open_lane:
            obstacle_color = color_map[safe_color]
        else:
            obstacle_color = row_colors.pop(0) if row_colors[0] != color_map[safe_color] else row_colors.pop(1)
        
        # Create the obstacle entity
        obstacle = Obstacle(lane,0.5,20,obstacle_color)
        obstacles.append(obstacle)

def update():
    global score, player_speed, last_update_time, obstacle_speed, passed, spawn_interval

    current_time = time.time()

    if current_time - last_update_time >= 1:
        obstacle_speed += 0.1  # Increase the speed
        spawn_interval *= 0.98
        player_speed *= 1.01
        last_update_time = current_time

    # Player movement
    if held_keys['a']:
        player.move(-time.dt * player_speed,lane_width)
    if held_keys['d']:
        player.move(time.dt * player_speed,lane_width)


    # Update obstacles
    obstacles_to_remove = []
    for obstacle in obstacles:
        obstacle.move(-(time.dt * obstacle_speed))
        if obstacle.get_z() < -10:
            obstacles_to_remove.append(obstacle)
        elif player.get_z() - obstacle.get_z() < 1.3 and player.get_z() - obstacle.get_z() >= 1.2:
            change_billboard()
    
    # Adjust score
    if passed:
        score+=1
        passed = False
    

    # Remove and destroy obstacles after processing
    for obstacle in obstacles_to_remove:
        obstacles.remove(obstacle)
        destroy(obstacle.get_shape())

    # Check for collisions
    for obstacle in obstacles:
        if player.get_shape().intersects(obstacle.get_shape()).hit:
            if obstacle.get_color() == color_map[safe_color]:
                # Safe collision
                print(f"Safe Pass! Current Score: {score}")
            else:
                # Game over
                print(f"Game Over! Final Score: {score}")
                loseSound.play()
                gameSound.stop()
                sleep(loseSound.length)
                application.quit()

    score_text.text = "Score: "+str(score)


# Function to show the correct color on the billboard
def change_billboard():
    global safe_color, passed
    safe_color = random.choice(list(color_map.keys()))  # Randomly select a new safe color
    billboard.change_color(color_map[safe_color])  # Show the safe color on the billboard
    passed = True


# Function to clear the billboard color
def clear_billboard():
    billboard.change_color(color.clear) # Clear the billboard color


# Function to spawn obstacles periodically
def spawn_obstacles():
    create_obstacle() 
    invoke(spawn_obstacles, delay=spawn_interval)


# Creates sounds
gameSound = Audio(sound_file_name='gameSound.wav', volume=1, loop=True, autoplay=True)
loseSound = Audio(sound_file_name='lose.wav', volume=1, loop=False, loops=1, autoplay=False)

# Start the obstacle spawning
spawn_obstacles()

# Run the game
app.run()
