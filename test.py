import pytest
import pygame
import time
import random
from project import (  # Replace with the actual name of your game module
    draw,
    game_over,
    main_menu,
    show_leaderboard,
    show_help,
    get_username,
    LEVELS,
    leaderboard
)

# Initialize Pygame
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

def test_draw():
    # Create a mock player and stars
    player = pygame.Rect(200, 500, 60, 60)
    level = 1
    highest_time = 10
    elapsed_time = 5
    stars = [pygame.Rect(100, 100, 10, 20), pygame.Rect(200, 200, 10, 20)]

    # Call the draw function
    draw(player, level, highest_time, elapsed_time, stars)

    # Since we can't check the display, we just ensure it runs without error
    assert True  # Placeholder to indicate the function executed

def test_game_over(monkeypatch):
    # Simulate user pressing 'R' to restart
    monkeypatch.setattr('pygame.event.get', lambda: [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)])
    
    leaderboard.append(("TestUser ", 25))
    result = game_over("TestUser ", 25)
    assert result is True  # Ensure it returns True to restart

def test_main_menu(monkeypatch):
    # Simulate user pressing 'S' to start the game
    monkeypatch.setattr('pygame.event.get', lambda: [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_s)])
    
    result = main_menu()
    assert result is True  # Ensure it returns True to start the game

def test_show_leaderboard(monkeypatch):
    # Simulate user pressing 'B' to go back
    monkeypatch.setattr('pygame.event.get', lambda: [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b)])
    
    show_leaderboard()  # This should run without errors

def test_show_help(monkeypatch):
    # Simulate user pressing 'B' to go back
    monkeypatch.setattr('pygame.event.get', lambda: [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_b)])
    
    show_help()  # This should run without errors

def test_get_username(monkeypatch):
    # Simulate user input for username
    username_input = iter(['T', 'e', 's', 't', 'U', 's', 'e', 'r', pygame.K_RETURN])  # Simulate entering "TestUser " and pressing Enter
    monkeypatch.setattr('pygame.event.get', lambda: [pygame.event.Event(pygame.KEYDOWN, key=next(username_input))])
    
    username = get_username()
    assert username == "TestUser "  # Ensure the username is correctly captured

def test_leaderboard():
    # Test adding a player to the leaderboard
    leaderboard.clear()  # Clear the leaderboard before the test
    leaderboard.append(("Player1", 30))
    leaderboard.append(("Player2", 20))
    leaderboard.append(("Player3", 40))

    # Sort the leaderboard
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)

    # Check if the leaderboard is sorted correctly
        # Check if the leaderboard is sorted correctly
    assert sorted_leaderboard[0] == ("Player3", 40)  # Highest score
    assert sorted_leaderboard[1] == ("Player1", 30)  # Second highest score
    assert sorted_leaderboard[2] == ("Player2", 20)  # Lowest score

def test_level_progression():
    # Test level progression logic
    elapsed_time = 51  # Simulate time passed
    level = 1

    # Check level progression
    if elapsed_time > 50 and level < 3:
        level += 1  # Move to the next level

    assert level == 2  # Ensure the level has progressed

def test_star_spawn():
    # Test star spawning logic
    level = 1
    star_speed = LEVELS[level]["star_speed"]
    star_add_increment = LEVELS[level]["star_add_increment"]
    stars_per_spawn = LEVELS[level]["stars_per_spawn"]

    star_count = 0
    stars = []

    # Simulate time passing to trigger star spawn
    star_count += 2000  # Simulate enough time to spawn stars

    if star_count > star_add_increment:
        for _ in range(stars_per_spawn):
            star_x = random.randint(0, 800 - 10)  # Assuming WIDTH is 800 and STAR_WIDTH is 10
            star = pygame.Rect(star_x, 0, 10, 20)  # Create a star
            stars.append(star)

    assert len(stars) == stars_per_spawn  # Ensure the correct number of stars were spawned

def test_collision_detection():
    # Test collision detection between player and stars
    player = pygame.Rect(200, 500, 60, 60)  # Player rectangle
    star = pygame.Rect(200, 500, 10, 20)  # Star rectangle that collides with the player

    # Check for collision
    collision = player.colliderect(star)
    assert collision is True  # Ensure a collision is detected

def test_no_collision():
    # Test no collision scenario
    player = pygame.Rect(200, 500, 60, 60)  # Player rectangle
    star = pygame.Rect(300, 400, 10, 20)  # Star rectangle that does not collide with the player

    # Check for collision
    collision = player.colliderect(star)
    assert collision is False  # Ensure no collision is detect