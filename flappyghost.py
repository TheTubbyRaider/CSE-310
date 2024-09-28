import arcade
import random

# Constants for screen dimensions and game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Flappy Ghost"
PLAYER_SCALING = 0.2
OBSTACLE_SCALING = 0.7
OBSTACLE_GAP = 150  # Base gap size for the ghost to fit through
GAP_VARIATION = 100  # Maximum variation for the gap
OBSTACLE_HORIZONTAL_SPACING = 300  # Fixed distance between the obstacles
GRAVITY = 1.0  # Increased gravity
PLAYER_JUMP_SPEED = 10
OBSTACLE_SPEED = 3  # Starting speed of obstacles
GROUND_HEIGHT = 50
PLAYER_HEIGHT = PLAYER_SCALING * 100  # Approximate height of the player based on scaling

class FlappyBirdGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables for player, obstacles, and physics engine
        self.player_sprite = None
        self.obstacle_list = None
        self.physics_engine = None

        # Variables for the game state
        self.player_alive = True
        self.score = 0
        self.high_score = 0
        self.start_game = False
        self.passed_obstacles = []  # Track obstacles that have been passed
        self.obstacle_speed = OBSTACLE_SPEED
        self.new_high_score = False  # Track if a new high score was achieved

    def setup(self):
        """ Set up the game and initialize variables """
        arcade.set_background_color(arcade.color.BLACK)

        self.player_sprite = arcade.Sprite("ghost.jpg", PLAYER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = SCREEN_HEIGHT // 2

        self.obstacle_list = arcade.SpriteList()
        self.passed_obstacles = []  # Reset passed obstacles for a new game
        self.new_high_score = False  # Reset new high score flag

        # Set up the physics engine for gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY)

        arcade.schedule(self.add_obstacle, 1)  # Add an obstacle every second

    def on_draw(self):
        """ Render the screen """
        arcade.start_render()

        if not self.start_game:  # Start Screen
            self.draw_start_screen()
        elif self.player_alive:  # Game Screen
            self.draw_game_screen()
        else:  # Death Screen
            self.draw_death_screen()

    def draw_start_screen(self):
        """ Draw the start screen """
        arcade.draw_text("Flappy Ghost", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, arcade.color.WHITE, 54, anchor_x="center")
        arcade.draw_text("Press SPACE to Start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, arcade.color.WHITE, 24, anchor_x="center")
        
        # Display the high score
        arcade.draw_text(f"High Score: {self.high_score}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60, arcade.color.WHITE, 24, anchor_x="center")

        arcade.draw_text("Click to Exit", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, arcade.color.WHITE, 24, anchor_x="center")

    def draw_game_screen(self):
        """ Draw the game screen """
        self.player_sprite.draw()
        self.obstacle_list.draw()
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, GROUND_HEIGHT, 0, arcade.color.GREEN)
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)

    def draw_death_screen(self):
        """ Draw the death screen """
        arcade.draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, arcade.color.WHITE, 54, anchor_x="center")
        arcade.draw_text(f"Score: {self.score}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, 24, anchor_x="center")
        
        # New high score message
        if self.new_high_score:
            arcade.draw_text("NEW HIGH SCORE!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, arcade.color.YELLOW, 24, anchor_x="center")

        # Spaced out words for the death screen
        arcade.draw_text("Press R to Restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60, arcade.color.WHITE, 24, anchor_x="center")

    def on_update(self, delta_time):
        """ Update the game state """
        if self.start_game and self.player_alive:
            self.physics_engine.update()

            # Rotate the ghost based on its vertical velocity
            if self.player_sprite.change_y < 0:  # Falling down
                self.player_sprite.angle -= 2
            elif self.player_sprite.change_y > 0:  # Jumping up
                self.player_sprite.angle += 2

            # Limit the angle to prevent excessive rotation
            self.player_sprite.angle = max(-45, min(self.player_sprite.angle, 15))

            if arcade.check_for_collision_with_list(self.player_sprite, self.obstacle_list):
                self.player_alive = False  # Stop the game if collided

            # Scroll the obstacles to the left and check for scoring
            for obstacle in self.obstacle_list:
                obstacle.center_x -= self.obstacle_speed

                # Check for passing the upper obstacle and mark both as passed
                if (obstacle.center_x + obstacle.width / 2 < self.player_sprite.center_x) and (obstacle not in self.passed_obstacles):
                    self.passed_obstacles.append(obstacle)  # Mark this obstacle as passed
                    self.score += 1  # Increment score when passing an obstacle

                # Remove obstacles that have gone off screen
                if obstacle.right < 0:
                    obstacle.remove_from_sprite_lists()

            # Increase speed slightly every 20 points
            if self.score > 0 and self.score % 20 == 0:  
                self.obstacle_speed += 0.1  # Gradual speed increase

            if self.player_sprite.center_y <= GROUND_HEIGHT + self.player_sprite.height / 2:
                self.player_sprite.center_y = GROUND_HEIGHT + self.player_sprite.height / 2
                self.player_sprite.change_y = 0  # Stop falling

    def on_key_press(self, key, modifiers):
        """ Handle key presses """
        if not self.start_game and key == arcade.key.SPACE:
            self.start_game = True
            self.setup()  # Start the game

        if self.start_game and self.player_alive and key == arcade.key.SPACE:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
            self.player_sprite.angle = 15  # Reset angle when jumping

        if not self.player_alive and key == arcade.key.R:
            # Restart the game and go back to home screen
            self.player_alive = True
            if self.score > self.high_score:  # Update high score
                self.high_score = self.score
                self.new_high_score = True  # Flag for new high score
            else:
                self.new_high_score = False  # Reset flag if not a new high score
                
            self.score = 0
            self.obstacle_speed = OBSTACLE_SPEED  # Reset speed
            self.obstacle_list = arcade.SpriteList()
            self.player_sprite.center_y = SCREEN_HEIGHT // 2
            self.player_sprite.angle = 0
            self.start_game = False  # Go back to start screen

    def on_mouse_press(self, x, y, button, modifiers):
        """ Handle mouse press events """
        if not self.start_game:  # Check if we are on the start screen
            arcade.close_window()  # Exit the game if clicked on "Click to Exit"

    def add_obstacle(self, delta_time):
        """ Add an obstacle to the game """
        upper_obstacle = arcade.Sprite("stalactite.png", OBSTACLE_SCALING)  # Upper obstacle
        upper_obstacle.center_x = SCREEN_WIDTH + upper_obstacle.width / 2  # Position right outside the screen
        upper_obstacle.top = SCREEN_HEIGHT  # Fix the top of the stalactite to the top of the screen

        lower_obstacle = arcade.Sprite("tree.png", OBSTACLE_SCALING * 0.5)  # Lower obstacle with reduced scaling
        lower_obstacle.center_x = SCREEN_WIDTH + upper_obstacle.width / 2 + OBSTACLE_HORIZONTAL_SPACING  # Position with fixed spacing to the right
        lower_obstacle.bottom = GROUND_HEIGHT  # Set the bottom of the tree to the ground

        # Calculate the height of the upper obstacle to maintain the gap with random variation
        random_offset = random.randint(-GAP_VARIATION // 2, GAP_VARIATION // 2)
        upper_obstacle.bottom = SCREEN_HEIGHT - OBSTACLE_GAP + random_offset  # Randomly position the bottom of the upper obstacle
        lower_obstacle.top = GROUND_HEIGHT + OBSTACLE_GAP + random_offset  # Randomly position the top of the lower obstacle

        self.obstacle_list.append(upper_obstacle)
        self.obstacle_list.append(lower_obstacle)

# Main entry point
def main():
    game = FlappyBirdGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
