import pygame
import time
import random

pygame.init()

# Game display
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DODGE IT NICO!")

# Load images
MENU_BG = pygame.transform.scale(pygame.image.load("bgnico.png"), (WIDTH, HEIGHT))  # Background for the menu
BG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("nico.jpg"), (60, 60)) 

# Size of falling star
STAR_WIDTH = 10
STAR_HEIGHT = 20

FONT = pygame.font.SysFont("Arial Black", 30)

# Level parameters
LEVELS = {
    1: {"star_speed": 2, "star_add_increment": 2000, "stars_per_spawn": 1},
    2: {"star_speed": 3, "star_add_increment": 2500, "stars_per_spawn": 2},
    3: {"star_speed": 5, "star_add_increment": 1000, "stars_per_spawn": 3},
}

leaderboard = []

def draw(player, level, highest_time, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    # Display the current level
    level_text = FONT.render(f"Level: {level}", 1, "white")
    WIN.blit(level_text, (10, 10))  # Position the level text at the top

    # Display the highest time
    highest_time_text = FONT.render(f"Highest Time: {round(highest_time)}", 1, "white")
    WIN.blit(highest_time_text, (10, 50))  # Position the highest time text below the level

    # Display the elapsed time
    time_text = FONT.render(f"Time: {round(elapsed_time)}", 1, "white")
    WIN.blit(time_text, (10, 90))  # Position the time text below the highest time

    # Draw the player image
    WIN.blit(PLAYER_IMAGE, (player.x, player.y))

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def game_over(username, highest_time):
    WIN.fill((0, 0, 0)) 
    lost_text = FONT.render("You Lost!", True, "white")
    play_again_text_r = FONT.render("Press R to Restart", True, "white")
    quit_text_q = FONT.render("Press Q to Quit", True, "white")
    main_menu_text_b = FONT.render("Press B to go to Main Menu", True, "white")
    
    # Center the lost text
    WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2 - 20))
    
    # Position the options below the lost text
    WIN.blit(play_again_text_r, (WIDTH / 2 - play_again_text_r.get_width() / 2, HEIGHT / 2 + 10))
    WIN.blit(quit_text_q, (WIDTH / 2 - quit_text_q.get_width() / 2, HEIGHT / 2 + 50))
    WIN.blit(main_menu_text_b, (WIDTH / 2 - main_menu_text_b.get_width() / 2, HEIGHT / 2 + 90))

    # Display the leaderboard at the top of the screen
    leaderboard_text = FONT.render("Leaderboard:", True, "white")
    WIN.blit(leaderboard_text, (WIDTH / 2 - leaderboard_text.get_width() / 2, 20))  # Position at the top center
    
    # Sort and display the leaderboard
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
    for i, (name, time) in enumerate(sorted_leaderboard[:5]):  # Show top 5
        entry_text = FONT.render(f"{i + 1}. {name}: {round(time)}", True, "white")
        WIN.blit(entry_text, (WIDTH / 2 - entry_text.get_width() / 2, 50 + i * 30))  # Position entries below the leaderboard title

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    return False  # Quit the game
                if event.key == pygame.K_b:
                    return False  # Go back to the main menu

def main_menu():
    while True:
        WIN.blit(MENU_BG, (0, 0))
        start_text = FONT.render("START GAME", True, "white")
        leaderboard_text = FONT.render("LEADERBOARD", True, "white")
        help_text = FONT.render("HELP", True, "white")
        quit_text = FONT.render("QUIT GAME", True, "white")

        WIN.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 2 - 20))
        WIN.blit(leaderboard_text, (WIDTH / 2 - leaderboard_text.get_width() / 2, HEIGHT / 2 + 20))
        WIN.blit(help_text, (WIDTH / 2 - help_text.get_width() / 2, HEIGHT / 2 + 60))
        WIN.blit(quit_text, (WIDTH / 2 - quit_text.get_width() / 2, HEIGHT / 2 + 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return True  # Start the game
                if event.key == pygame.K_l:
                    show_leaderboard()  # Show leaderboard
                if event.key == pygame.K_h:
                    show_help()  # Show help
                if event.key == pygame.K_q:
                    pygame.quit()
                    return False  # Quit the game

def show_leaderboard():
    while True:
        WIN.fill((0, 0, 0))
        leaderboard_text = FONT.render("Leaderboard", True, "white")
        WIN.blit(leaderboard_text, (WIDTH / 2 - leaderboard_text.get_width() / 2, HEIGHT / 2 - 200))

        # Sort and display the leaderboard
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
        for i, (name, time) in enumerate(sorted_leaderboard[:5]):  # Show top 5
            entry_text = FONT.render(f"{i + 1}. {name}: {round(time)}", True, "white")
            WIN.blit(entry_text, (WIDTH / 2 - entry_text.get_width() / 2, HEIGHT / 2 - 150 + i * 30))

        back_text = FONT.render("Press B to go back", True, "white")
        WIN.blit(back_text, (WIDTH / 2 - back_text.get_width() / 2, HEIGHT / 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return  # Go back to the main menu

def show_help():
    while True:
        WIN.fill((0, 0, 0))
        help_text1 = FONT.render("GAME MECHANICS:", True, "yellow")
        help_text2 = FONT.render("Avoid the falling stars!", True, "white")
        help_text3 = FONT.render("Use the left and right arrow keys to move.", True, "white")
        back_text = FONT.render("Press B to go back", True, "white")

        WIN.blit(help_text1, (WIDTH / 2 - help_text1.get_width() / 2, HEIGHT / 2 - 100))
        WIN.blit(help_text2, (WIDTH / 2 - help_text2.get_width() / 2, HEIGHT / 2 - 50))
        WIN.blit(help_text3, (WIDTH / 2 - help_text3.get_width() / 2, HEIGHT / 2))
        WIN.blit(back_text, (WIDTH / 2 - back_text.get_width() / 2, HEIGHT / 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return  # Go back to the main menu

def get_username():
    username = ""
    input_active = True
    while input_active:
        WIN.fill((0, 0, 0))
        prompt_text = FONT.render("Enter your username:", True, "white")
        WIN.blit(prompt_text, (WIDTH / 2 - prompt_text.get_width() / 2, HEIGHT / 2 - 50))
        
        username_text = FONT.render(username, True, "white")
        WIN.blit(username_text, (WIDTH / 2 - username_text.get_width() / 2, HEIGHT / 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:  # Enter key pressed
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Backspace key pressed
                    username = username[:-1]
                else:
                    username += event.unicode  # Add the character to the username

    return username

def main(): 
    run = True
    highest_time = 0  # Variable to store the highest time
    level = 1  # Start at level 1

    username = get_username()  # Get the username before starting the game
    if username is None:
        return  # Exit if the user quits

    while run:
        player = pygame.Rect(200, HEIGHT - 60, 60, 60)  # Adjusted for player image size
        clock = pygame.time.Clock()
        start_time = time.time()
        elapsed_time = 0

        # Get level parameters
        star_speed = LEVELS[level]["star_speed"]
        star_add_increment = LEVELS[level]["star_add_increment"]
        stars_per_spawn = LEVELS[level]["stars_per_spawn"]

        star_count = 0
        stars = []
        hit = False

        while True:
            star_count += clock.tick(60)
            elapsed_time = time.time() - start_time

            # Check for level progression
            if elapsed_time > 50 and level < 3:
                level += 1  # Move to the next level
                star_speed = LEVELS[level]["star_speed"]
                star_add_increment = LEVELS[level]["star_add_increment"]
                stars_per_spawn = LEVELS[level]["stars_per_spawn"]

            if star_count > star_add_increment:
                for _ in range(stars_per_spawn):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, 0, STAR_WIDTH, STAR_HEIGHT)  
                    stars.append(star)

                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0  # Reset star count after spawning

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
           
            # Player movement, left and right
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - 5 > 0:
                player.x -= 5
            if keys[pygame.K_RIGHT] and player.x + 5 < WIDTH - 60:  # Adjusted for player image width
                player.x += 5
            
            for star in stars[:]:
                star.y += star_speed  # Use the speed based on the level
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.y + star.height >= player.y and star.colliderect(player):
                    hit = True  # Collision detected
                    break  # Exit the loop to handle game over

            # If a collision was detected, break out of the main game loop
            if hit:
                # Update highest time if the current elapsed time is greater
                if elapsed_time > highest_time:
                    highest_time = elapsed_time
                
                # Add the player's score to the leaderboard
                leaderboard.append((username, highest_time))

                # Show the game over screen
                result = game_over(username, highest_time)
                if result is False:
                    return  # Exit to main menu
                elif result is True:
                    # Reset the game state for a new game
                    level = 1  # Reset level to 1
                    player.x = 200  # Reset player position
                    stars.clear()  # Clear any remaining stars
                    break  # Break out of the inner loop to restart the game

            # Draw the current state of the game
            draw(player, level, highest_time, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    while True:
        if not main_menu():  # Show the main menu and start the game
            break
        main()  # Start the game directly without a menu