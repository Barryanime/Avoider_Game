# import sys, pygame, math
import sys
import pygame
# Starter code for an avoid game. Written by David Johnson for CS 1400 University of Utah.

# Finished game authors:
# Barry Lin


def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check if the non-transparent pixels of one contacts the other.
    """
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap


def level_2():
    # Initialize pygame
    pygame.init()

    map1 = pygame.image.load("map1.png")
    # Store window width and height in different forms for easy access
    map_size = map1.get_size()
    map_rect = map1.get_rect()

    end_screen = pygame.image.load("Game Over.png")
    end_screen_rect = end_screen.get_rect()

    # create the window based on the map1 size
    screen = pygame.display.set_mode(map_size)
    map1 = map1.convert_alpha()
    map1.set_colorkey((192, 179, 120))
    map_mask = pygame.mask.from_surface(map1)

    # Create the player data
    player = pygame.image.load("Player 1.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (20, 35))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    # Create the key
    key = pygame.image.load("key1.png").convert_alpha()
    key = pygame.transform.smoothscale(key, (25, 25))
    key_rect = key.get_rect()
    key_rect.center = (315, 75)
    key_mask = pygame.mask.from_surface(key)

    # Create second key
    key2 = pygame.image.load("key2.png").convert_alpha()
    key2 = pygame.transform.smoothscale(key2, (25, 25))
    key2_rect = key2.get_rect()
    key2_rect.center = (275, 500)
    key2_mask = pygame.mask.from_surface(key2)

    # Create third key
    key3 = pygame.image.load("key3.png").convert_alpha()
    key3 = pygame.transform.smoothscale(key3, (25, 25))
    key3_rect = key3.get_rect()
    key3_rect.center = (750, 20)
    key3_mask = pygame.mask.from_surface(key3)

    # Create the chest
    chest = pygame.image.load("chest.png").convert_alpha()
    chest = pygame.transform.smoothscale(chest, (100, 56))
    chest_rect = chest.get_rect()
    chest_rect.center = (365, 315)
    chest_mask = pygame.mask.from_surface(chest)

    # Create the start icon
    start = pygame.image.load("Start-icon.png").convert_alpha()
    start = pygame.transform.smoothscale(start, (50, 50))
    start_rect = start.get_rect()
    start_rect.center = (525, 300)
    start_mask = pygame.mask.from_surface(start)

    # Create the game over screen

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    my_font = pygame.font.SysFont('monospace', 24)

    # The started variable records if the start color has been clicked and the level started
    started = False
    print(started)
    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    dead = False

    # This state variable shows whether the key is found yet or not
    found_key = False
    found_key2 = False
    found_key3 = False
    found_chest = False
    found_start = False

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pixel_collision(player_mask, player_rect, start_mask, start_rect):
                    started = True
                    print(started)
            if pixel_collision(player_mask, player_rect, map_mask, map_rect):
                if started:
                    dead = True

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player_rect.center = pos

        # See if we touch the maze walls
        if pixel_collision(player_mask, player_rect, map_mask, map_rect):
            print("colliding", frame_count)  # Don't leave this in the game

        # See if we touch the chest
        if pixel_collision(player_mask, player_rect, chest_mask, chest_rect):
            print("colliding chest", frame_count)  # Don't leave this in the game

        # See if we touch the key
        if pixel_collision(player_mask, player_rect, key_mask, key_rect):
            print("colliding key", frame_count)  # Don't leave this in the game

        # See if we touch second key
        if pixel_collision(player_mask, player_rect, key2_mask, key2_rect):
            print("colliding second key", frame_count)  # Don't leave this in the game

        # See if we touch third key
        if pixel_collision(player_mask, player_rect, key3_mask, key3_rect):
            print("colliding third key", frame_count)  # Don't leave this in the game

        # Check if we contact the key
        if not found_key and pixel_collision(player_mask, player_rect, key_mask, key_rect):
            found_key = True

        # Check if we contact second key
        if not found_key2 and pixel_collision(player_mask, player_rect, key2_mask, key2_rect):
            found_key2 = True

        # Check if we contact third key
        if not found_key3 and pixel_collision(player_mask, player_rect, key3_mask, key3_rect):
            found_key3 = True

        # Check if we contact the chest
        if not found_chest and pixel_collision(player_mask, player_rect, chest_mask, chest_rect):
            found_chest = True
            print("colliding with chest")

        # Check if we contact start icon
        if not found_start and pixel_collision(player_mask, player_rect, start_mask, start_rect):
            found_start = True

        # Draw the background
        screen.fill((192, 179, 120))
        screen.blit(map1, map_rect)

        # Draw start icon only if it has not been clicked
        if not started:
            screen.blit(start, start_rect)
            found_start = False
            found_chest = False
            found_key = False
            found_key2 = False
            found_key3 = False

        if started:
            # Only draw the key if the key is not collected
            if not found_key:
                screen.blit(key, key_rect)
                found_chest = False

            # Only draw second key if the key is not collected
            if not found_key2:
                screen.blit(key2, key2_rect)

            # Only draw third key if the key is not collected
            if not found_key3:
                screen.blit(key3, key3_rect)

            # Draw the chest if the key is found
            if found_key:
                screen.blit(chest, chest_rect)

            # Go to Level 2 if chest is found
            if found_chest:
                level_3()

        # Draw the player character
        screen.blit(player, player_rect)

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label = my_font.render("Hint: The chest will appear once you found the right key", True, (255, 0, 0))
        screen.blit(label, (20, 20))

        # Draw the game over screen when you are dead
        if dead:
            screen.blit(end_screen, end_screen_rect)

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    pygame.quit()
    sys.exit()


def level_3():
    # Initialize pygame
    pygame.init()

    map1 = pygame.image.load("map2.png")
    # Store window width and height in different forms for easy access
    map_size = map1.get_size()
    map_rect = map1.get_rect()

    # Create the end screen
    end_screen = pygame.image.load("Game Over.png")
    end_screen_rect = end_screen.get_rect()

    # Create the finish screen
    finish = pygame.image.load("finish.png")
    finish_rect = finish.get_rect()

    # create the window based on the map1 size
    screen = pygame.display.set_mode(map_size)
    map1 = map1.convert_alpha()
    map1.set_colorkey((109, 126, 49))
    map_mask = pygame.mask.from_surface(map1)

    # Create the player data
    player = pygame.image.load("Player 1.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (20, 35))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    # Create the crystal
    crystal = pygame.image.load("crystal.png").convert_alpha()
    crystal = pygame.transform.smoothscale(crystal, (35, 35))
    crystal_rect = crystal.get_rect()
    crystal_rect.center = (640, 170)
    crystal_mask = pygame.mask.from_surface(crystal)

    # Create the wall
    wall = pygame.image.load("wall.png").convert_alpha()
    wall = pygame.transform.smoothscale(wall, (90, 115))
    wall_rect = wall.get_rect()
    wall_rect.center = (490, 392)
    wall_mask = pygame.mask.from_surface(wall)

    # Create second crystal
    crystal2 = pygame.image.load("crystal2.png").convert_alpha()
    crystal2 = pygame.transform.smoothscale(crystal2, (35, 35))
    crystal2_rect = crystal2.get_rect()
    crystal2_rect.center = (200, 100)
    crystal2_mask = pygame.mask.from_surface(crystal2)

    # Create second wall
    wall2 = pygame.image.load("wall2.png").convert_alpha()
    wall2 = pygame.transform.smoothscale(wall2, (80, 115))
    wall2_rect = wall2.get_rect()
    wall2_rect.center = (120, 315)
    wall2_mask = pygame.mask.from_surface(wall2)

    # Create third crystal
    crystal3 = pygame.image.load("crystal3.png").convert_alpha()
    crystal3 = pygame.transform.smoothscale(crystal3, (35, 35))
    crystal3_rect = crystal3.get_rect()
    crystal3_rect.center = (500, 560)
    crystal3_mask = pygame.mask.from_surface(crystal3)

    # Create fourth crystal
    crystal4 = pygame.image.load("crystal2.png").convert_alpha()
    crystal4 = pygame.transform.smoothscale(crystal4, (35, 35))
    crystal4_rect = crystal4.get_rect()
    crystal4_rect.center = (235, 290)
    crystal4_mask = pygame.mask.from_surface(crystal4)

    # Create fifth crystal
    crystal5 = pygame.image.load("crystal.png").convert_alpha()
    crystal5 = pygame.transform.smoothscale(crystal5, (35, 35))
    crystal5_rect = crystal5.get_rect()
    crystal5_rect.center = (500, 170)
    crystal5_mask = pygame.mask.from_surface(crystal5)

    # Create third wall
    wall3 = pygame.image.load("wall3.png").convert_alpha()
    wall3 = pygame.transform.smoothscale(wall3, (80, 115))
    wall3_rect = wall3.get_rect()
    wall3_rect.center = (325, 455)
    wall3_mask = pygame.mask.from_surface(wall3)

    # Create the final key
    key = pygame.image.load("Black Key.png").convert_alpha()
    key = pygame.transform.smoothscale(key, (35, 35))
    key_rect = key.get_rect()
    key_rect.center = (665, 425)
    key_mask = pygame.mask.from_surface(key)

    # Create fourth wall
    wall4 = pygame.image.load("wall4.png").convert_alpha()
    wall4 = pygame.transform.smoothscale(wall4, (90, 115))
    wall4_rect = wall4.get_rect()
    wall4_rect.center = (283, 510)
    wall4_mask = pygame.mask.from_surface(wall4)

    # Create the chest
    chest = pygame.image.load("chest.png").convert_alpha()
    chest = pygame.transform.smoothscale(chest, (100, 56))
    chest_rect = chest.get_rect()
    chest_rect.center = (50, 560)
    chest_mask = pygame.mask.from_surface(chest)

    # Create the start icon
    start = pygame.image.load("Start-icon.png").convert_alpha()
    start = pygame.transform.smoothscale(start, (50, 50))
    start_rect = start.get_rect()
    start_rect.center = (700, 550)
    start_mask = pygame.mask.from_surface(start)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    my_font = pygame.font.SysFont('monospace', 24)

    # The started variable records if the start color has been clicked and the level started
    started = False
    print(started)
    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    dead = False

    # This state variable shows whether the key is found yet or not
    found_crystal = False
    found_crystal2 = False
    found_crystal3 = False
    found_crystal4 = False
    found_crystal5 = False
    found_chest = False
    found_start = False
    found_wall = False
    found_wall2 = False
    found_wall3 = False
    found_wall4 = False
    found_key = False
    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pixel_collision(player_mask, player_rect, start_mask, start_rect):
                    started = True
                    print(started)
            if pixel_collision(player_mask, player_rect, map_mask, map_rect):
                if started:
                    dead = True
            if pixel_collision(player_mask, player_rect, wall_mask, wall_rect):
                if started and found_wall:
                    dead = True
            if pixel_collision(player_mask, player_rect, wall2_mask, wall2_rect):
                if started and found_wall2:
                    dead = True
            if pixel_collision(player_mask, player_rect, wall3_mask, wall3_rect):
                if started and found_wall3:
                    dead = True
            if pixel_collision(player_mask, player_rect, wall4_mask, wall4_rect):
                if started and found_wall4:
                    dead = True

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player_rect.center = pos

        # See if we touch the maze walls
        if pixel_collision(player_mask, player_rect, map_mask, map_rect):
            print("colliding", frame_count)  # Don't leave this in the game

        # See if we touch the chest
        if pixel_collision(player_mask, player_rect, chest_mask, chest_rect):
            print("colliding chest", frame_count)  # Don't leave this in the game

        # See if we touch the crystal
        if pixel_collision(player_mask, player_rect, crystal_mask, crystal_rect):
            print("colliding crystal", frame_count)  # Don't leave this in the game

        # See if we touch second crystal
        if pixel_collision(player_mask, player_rect, crystal2_mask, crystal2_rect):
            print("colliding second crystal", frame_count)  # Don't leave this in the game

        # See if we touch third crystal
        if pixel_collision(player_mask, player_rect, crystal3_mask, crystal3_rect):
            print("colliding third crystal", frame_count)  # Don't leave this in the game

        # See if we touch the wall
        if pixel_collision(player_mask, player_rect, wall_mask, wall_rect):
            print("colliding wall", frame_count)

        # See if we touch second wall
        if pixel_collision(player_mask, player_rect, wall2_mask, wall2_rect):
            print("colliding second wall", frame_count)

        # See if we touch third wall
        if pixel_collision(player_mask, player_rect, wall3_mask, wall3_rect):
            print("colliding third wall", frame_count)

        # See if we touch start icon
        # if pixel_collision(player_mask, player_rect, start_mask, start_rect):
        #     print("colliding start icon", frame_count)  # Don't leave this in the game

        # Check if we contact the key
        if not found_crystal and pixel_collision(player_mask, player_rect, crystal_mask, crystal_rect):
            found_crystal = True

        # Check if we contact second crystal
        if not found_crystal2 and pixel_collision(player_mask, player_rect, crystal2_mask, crystal2_rect):
            found_crystal2 = True

        # Check if we contact third crystal
        if not found_crystal3 and pixel_collision(player_mask, player_rect, crystal3_mask, crystal3_rect):
            found_crystal3 = True

        # Check if we contact fourth crystal
        if found_crystal3:
            if not found_crystal4 and pixel_collision(player_mask, player_rect, crystal4_mask, crystal4_rect):
                found_crystal4 = True

        # Check if we contact fifth crystal
        if found_crystal3:
            if not found_crystal5 and pixel_collision(player_mask, player_rect, crystal5_mask, crystal5_rect):
                found_crystal5 = True

        # Check if we contact the chest
        if not found_chest and pixel_collision(player_mask, player_rect, chest_mask, chest_rect):
            found_chest = True

        # Check if we contact start icon
        if not found_start and pixel_collision(player_mask, player_rect, chest_mask, chest_rect):
            found_start = True

        if not found_wall and pixel_collision(player_mask, player_rect, wall_mask, wall_rect):
            found_wall = True

        if not found_wall2 and pixel_collision(player_mask, player_rect, wall2_mask, wall2_rect):
            found_wall2 = True

        if not found_wall3 and pixel_collision(player_mask, player_rect, wall3_mask, wall3_rect):
            found_wall3 = True

        if not found_wall4 and pixel_collision(player_mask, player_rect, wall4_mask, wall4_rect):
            found_wall4 = True

        if not found_key and pixel_collision(player_mask, player_rect, key_mask, key_rect):
            found_key = True

        # Draw the background
        screen.fill((192, 179, 120))
        screen.blit(map1, map_rect)

        if not started:
            screen.blit(start, start_rect)
            found_crystal = False
            found_crystal2 = False
            found_crystal3 = False

        if started:
            # Only draw the crystal if the crystal is not collected
            if not found_crystal:
                screen.blit(crystal, crystal_rect)
                screen.blit(wall, wall_rect)

            # Only draw crystal key if the crystal is not collected
            if not found_crystal2:
                screen.blit(crystal2, crystal2_rect)
                screen.blit(wall2, wall2_rect)

            # Only draw third crystal if the crystal is not collected
            if not found_crystal3:
                screen.blit(crystal3, crystal3_rect)
                screen.blit(wall3, wall3_rect)

            # Draw the chest if the key is found
            if found_crystal:
                found_wall = False

            if found_crystal2:
                found_wall2 = False

            if found_crystal3:
                found_wall3 = False
                if not found_key:
                    screen.blit(key, key_rect)
                    screen.blit(wall4, wall4_rect)
                    found_wall4 = True
                if found_key:
                    found_wall4 = False
                if not found_crystal4:
                    screen.blit(crystal4, crystal4_rect)
                    screen.blit(wall2, wall2_rect)
                    found_wall2 = True
                if not found_crystal5:
                    screen.blit(crystal5, crystal5_rect)
                    screen.blit(wall, wall_rect)
                    found_wall = True
            # Draw the end chest
            screen.blit(chest, chest_rect)
            if found_chest:
                screen.blit(finish, finish_rect)

        # Draw the player character
        screen.blit(player, player_rect)

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label = my_font.render("Hint: Collect crystals to make wall disappear", True, (255, 255, 0))
        screen.blit(label, (20, 20))

        if dead:
            screen.blit(end_screen, end_screen_rect)
        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    pygame.quit()
    sys.exit()


def main():
    # Initialize pygame
    pygame.init()

    map1 = pygame.image.load("map3.png")
    # Store window width and height in different forms for easy access
    map_size = map1.get_size()
    map_rect = map1.get_rect()

    end_screen = pygame.image.load("Game Over.png")
    end_screen_rect = end_screen.get_rect()

    # create the window based on the map1 size
    screen = pygame.display.set_mode(map_size)
    map1 = map1.convert_alpha()
    map1.set_colorkey((51, 135, 146))
    map_mask = pygame.mask.from_surface(map1)

    # Create the player data
    player = pygame.image.load("Player2.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (240, 125))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    # Create the package
    key = pygame.image.load("package.png").convert_alpha()
    key = pygame.transform.smoothscale(key, (100, 100))
    key_rect = key.get_rect()
    key_rect.center = (415, 75)
    key_mask = pygame.mask.from_surface(key)

    # Create second package
    key2 = pygame.image.load("package.png").convert_alpha()
    key2 = pygame.transform.smoothscale(key2, (100, 100))
    key2_rect = key2.get_rect()
    key2_rect.center = (650, 500)
    key2_mask = pygame.mask.from_surface(key2)

    # Create third package
    key3 = pygame.image.load("package.png").convert_alpha()
    key3 = pygame.transform.smoothscale(key3, (100, 100))
    key3_rect = key3.get_rect()
    key3_rect.center = (300, 300)
    key3_mask = pygame.mask.from_surface(key3)

    # Create the bomb
    bomb = pygame.image.load("bomb.png").convert_alpha()
    bomb = pygame.transform.smoothscale(bomb, (100, 100))
    bomb_rect = key.get_rect()
    bomb_rect.center = (415, 300)
    bomb_mask = pygame.mask.from_surface(bomb)

    # Create second bomb
    bomb2 = pygame.image.load("bomb.png").convert_alpha()
    bomb2 = pygame.transform.smoothscale(bomb2, (100, 100))
    bomb2_rect = bomb2.get_rect()
    bomb2_rect.center = (275, 500)
    bomb2_mask = pygame.mask.from_surface(bomb2)

    # Create third bomb
    bomb3 = pygame.image.load("bomb.png").convert_alpha()
    bomb3 = pygame.transform.smoothscale(bomb3, (100, 100))
    bomb3_rect = bomb3.get_rect()
    bomb3_rect.center = (175, 200)
    bomb3_mask = pygame.mask.from_surface(bomb3)

    # Create the chest
    chest = pygame.image.load("chest2.png").convert_alpha()
    chest = pygame.transform.smoothscale(chest, (56, 100))
    chest_rect = chest.get_rect()
    chest_rect.center = (715, 315)
    chest_mask = pygame.mask.from_surface(chest)

    # Create the start icon
    start = pygame.image.load("Start-icon.png").convert_alpha()
    start = pygame.transform.smoothscale(start, (50, 50))
    start_rect = start.get_rect()
    start_rect.center = (100, 300)
    start_mask = pygame.mask.from_surface(start)

    # Create the game over screen

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font - there is some problem on my Mac that makes this pause for 10s of seconds sometimes.
    # I will see if I can find a fix.
    my_font = pygame.font.SysFont('monospace', 24)

    # The started variable records if the start color has been clicked and the level started
    started = False
    print(started)
    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    dead = False

    # This state variable shows whether the key is found yet or not
    found_key = False
    found_key2 = False
    found_key3 = False
    found_bomb = False
    found_bomb2 = False
    found_bomb3 = False
    found_chest = False
    found_start = False

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pixel_collision(player_mask, player_rect, start_mask, start_rect):
                    started = True
                    print(started)
            if pixel_collision(player_mask, player_rect, map_mask, map_rect):
                if started:
                    dead = True
            if pixel_collision(player_mask, player_rect, bomb_mask, bomb_rect):
                if started:
                    dead = True
            if pixel_collision(player_mask, player_rect, bomb2_mask, bomb2_rect):
                if started:
                    dead = True
            if pixel_collision(player_mask, player_rect, bomb3_mask, bomb3_rect):
                if started:
                    dead = True

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player_rect.center = pos

        # Check if we contact the key
        if not found_key and pixel_collision(player_mask, player_rect, key_mask, key_rect):
            found_key = True

        # Check if we contact second key
        if not found_key2 and pixel_collision(player_mask, player_rect, key2_mask, key2_rect):
            found_key2 = True

        # Check if we contact third key
        if not found_key3 and pixel_collision(player_mask, player_rect, key3_mask, key3_rect):
            found_key3 = True

        # Check if we contact the bomb
        if not found_bomb and pixel_collision(player_mask, player_rect, bomb_mask, bomb_rect):
            found_key = True

        # Check if we contact second bomb
        if not found_bomb2 and pixel_collision(player_mask, player_rect, bomb2_mask, bomb2_rect):
            found_bomb2 = True

        # Check if we contact third bomb
        if not found_bomb3 and pixel_collision(player_mask, player_rect, bomb3_mask, bomb3_rect):
            found_bomb3 = True

        # Check if we contact the chest
        if not found_chest and pixel_collision(player_mask, player_rect, chest_mask, chest_rect):
            found_chest = True
            print("colliding with chest")

        # Check if we contact start icon
        if not found_start and pixel_collision(player_mask, player_rect, start_mask, start_rect):
            found_start = True

        # Draw the background
        screen.fill((51, 135, 146))
        screen.blit(map1, map_rect)

        # Draw start icon only if it has not been clicked
        if not started:
            screen.blit(start, start_rect)
            found_start = False
            found_chest = False
            found_key = False
            found_key2 = False
            found_key3 = False
            found_bomb = False
            found_bomb2 = False
            found_bomb3 = False

        if started:
            screen.blit(bomb, bomb_rect)
            screen.blit(bomb2, bomb2_rect)
            screen.blit(bomb3, bomb3_rect)

            # Only draw the key if the key is not collected
            if not found_key:
                screen.blit(key, key_rect)
                found_chest = False

            # Only draw second key if the key is not collected
            if not found_key2:
                screen.blit(key2, key2_rect)

            # Only draw third key if the key is not collected
            if not found_key3:
                screen.blit(key3, key3_rect)

            # Draw the chest if the key is found
            if found_key and found_key2 and found_key3:
                screen.blit(chest, chest_rect)

            # Go to Level 2 if chest is found
            if found_chest:
                level_2()

        # Draw the player character
        screen.blit(player, player_rect)

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label = my_font.render("Hint: Collect all packages to find chest, avoid bombs", True, (255, 0, 0))
        screen.blit(label, (20, 20))

        # Draw the game over screen when you are dead
        if dead:
            screen.blit(end_screen, end_screen_rect)

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    pygame.quit()
    sys.exit()


# Start the program
main()
