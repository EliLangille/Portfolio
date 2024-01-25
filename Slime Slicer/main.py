# PROG 1700 - NSCC
# Final Project - PyGame

# Slime Slicer
# Created by Eli Langille
# Dec 8, 2023

import datetime
import pygame


def record_score(file, score):
    """Records a given int score and the current date to a given file path

    :param file: A string representing a file path
    :param score: An int representing a game score
    :return:
    """
    # Gets and formats the current date
    timestamp = datetime.datetime.now()
    formatted_timestamp = timestamp.strftime("%Y-%m-%d")

    # Records score and the formatted date to the file
    with open(file, "a") as file:
        file.write(f"{score} --- {formatted_timestamp}\n")


def get_high_scorer(file):
    """Searches a scoresheet file and returns the line with the highest score

    :param file: A string representing a file path
    :return: A list with a score int and the date it was recorded
    """
    # Initialize variables
    play_history = []
    highest_scorer = [0, "0000-00-00"]

    # Open file to read
    with open(file, 'r') as file:
        for line in file:
            # If line not empty
            if line != "\n" and line != "":
                # Split each line (a score and a date) into 2 variables in a list, and format them
                line_data = line.split(' --- ')
                line_data[0] = int(line_data[0])  # Set kill count as an int
                line_data[1] = line_data[1][:-1]  # remove the "\n"

                # Append the new list to the play_history list
                play_history.append(line_data)

    # For each item in play_history, update the high score line when applicable
    for i in range(len(play_history)):
        if play_history[i][0] > highest_scorer[0]:
            highest_scorer = play_history[i]

    return highest_scorer


def split_frame_sheet(frame_sheet, frame_count):
    """Takes a given image containing sprite animation frames, splits them into individual frames, converts them to
    Surface objects, and appends them to a list which is returned.

    :param frame_sheet: An image containing frames for a sprite's animation
    :param frame_count: An int for the number of frames
    :return: A list of the split frames
    """
    # Split apart the frames into a pre-created list using the sprite's dimensions, converting them as needed
    frames = []
    for i in range(frame_count):
        frame_rect = pygame.Rect(i * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        frame = frame_sheet.subsurface(frame_rect)
        frames.append(frame)

    return frames


def flip_animation(animation):
    """Takes a list of frames (Surface objects) for an animation and flips them horizontally

    :param animation: The list of frames
    :return: The new list of flipped frames
    """
    # Initialize new list
    new_animation = []

    # Flip each frame and append them to the new list
    for frame in animation:
        new_animation.append(pygame.transform.flip(frame, True, False))

    return new_animation


def draw_start_screen():
    """Draws a starting screen for the game with a controls guide"""
    # Render text
    left = TITLE_FONT.render("Left: A", 1, BLACK)
    right = TITLE_FONT.render("Right: D", 1, BLACK)
    attack = TITLE_FONT.render("Attack: Space", 1, BLACK)

    # Draw the background
    WINDOW.blit(BACKGROUND, (0, 0))

    # Draw the controls guide
    WINDOW.blit(left, (WIDTH / 2 - left.get_width() / 2,
                       HEIGHT / 2 - left.get_height() - right.get_height()))
    WINDOW.blit(right, (WIDTH / 2 - right.get_width() / 2,
                        HEIGHT / 2 - right.get_height() / 2))
    WINDOW.blit(attack, (WIDTH / 2 - attack.get_width() / 2,
                         HEIGHT / 2 + attack.get_height()))

    # Update screen to load changes
    pygame.display.update()

    # Hold the screen for 4 seconds
    pygame.time.delay(4000)


def draw_game(sprite, sprite_frame, slimes, kills, screen_type=0):
    """ Draws a frame for the main game

    :param sprite: A Rect object representing the sprite
    :param sprite_frame: The current frame of the sprite's animation
    :param slimes: A 2D list of slime Rect objects, a left list and a right list
    :param kills: An int for the current number of slime kills
    :param screen_type: An int determining which game screen to draw (gameplay, death, win/loss, high score)
    :return:
    """
    # Render score text
    score = TITLE_FONT.render(f"Kills: {kills}", 1, BLACK)

    # Draw background
    WINDOW.blit(BACKGROUND, (0, 0))

    # Draw the current frame of the sprite's animation
    WINDOW.blit(sprite_frame, (sprite.x, sprite.y))

    # Draw slimes from left side
    for slime in slimes[0]:
        WINDOW.blit(pygame.transform.flip(SLIME_IMAGE, True, False), (slime.x, slime.y))
    # Draw slimes from right side
    for slime in slimes[1]:
        WINDOW.blit(SLIME_IMAGE, (slime.x, slime.y))

    # Draw score when playing
    if screen_type == 0:
        WINDOW.blit(score, (20, 20))

    # For any post-game screen
    else:
        # Creates a dimming effect to be drawn
        dim_effect = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(dim_effect, TRANSLUCENT_GREY, dim_effect.get_rect())

        # Draw the dimming effect
        WINDOW.blit(dim_effect, (0, 0))

        # If death screen
        if screen_type == 1:
            # Renders the death message to draw
            death_message = DEATH_FONT.render("You Died", 1, RED)

            # Draws the text
            WINDOW.blit(death_message, (WIDTH / 2 - death_message.get_width() / 2,
                                        HEIGHT / 2 - death_message.get_height() / 2))

        # Else (if Win/Loss screen or High Score screen)
        else:
            # Get previous high score entry
            high_score = get_high_scorer(SCOREKEEPER_FILE_PATH)

            # If Win/Loss screen
            if screen_type == 2:
                # If player set a new high score and the win statement
                if kills > high_score[0]:
                    result_pt1 = TITLE_FONT.render("You Beat", 1, WHITE)
                # Else, set loss statement
                else:
                    result_pt1 = TITLE_FONT.render("You Did Not Beat", 1, WHITE)

                # Set 2nd line of text
                result_pt2 = TITLE_FONT.render("The High Score", 1, WHITE)

                # Draws the win/loss result
                WINDOW.blit(result_pt1, (WIDTH / 2 - result_pt1.get_width() / 2,
                                         HEIGHT / 2 - result_pt1.get_height() - 10))
                WINDOW.blit(result_pt2, (WIDTH / 2 - result_pt2.get_width() / 2,
                                         HEIGHT / 2 + 10))

            # Else (High score screen)
            else:
                # If player set a new high score, set win statement
                if kills > high_score[0]:
                    title = TITLE_FONT.render("New High Score", 1, WHITE)
                    high_score = [kills, datetime.datetime.now().strftime("%Y-%m-%d")]
                # Else, set loss statement
                else:
                    title = TITLE_FONT.render("Previous High Score", 1, WHITE)

                # Render high score data as text
                score = NORMAL_FONT.render(f"{high_score[0]} Kills", 1, GREY)
                date = NORMAL_FONT.render(f"{high_score[1]}", 1, GREY)

                # Gets height needed to align texts
                title_height = title.get_height()
                score_height = score.get_height()

                # Draws the high score
                WINDOW.blit(title, (WIDTH / 2 - title.get_width() / 2,
                                    HEIGHT / 2 - title_height - score_height))
                WINDOW.blit(score, (WIDTH / 2 - score.get_width() / 2,
                                    HEIGHT / 2 - score_height / 2))
                WINDOW.blit(date, (WIDTH / 2 - date.get_width() / 2,
                                   HEIGHT / 2 + score_height))

    # Update screen to load changes
    pygame.display.update()


def process_keys(sprite, keys_pressed, sprite_status):
    """ Processes player input (movement or attacks) and updates a given list storing sprite status info

    :param sprite: A rect object representing the player's sprite
    :param keys_pressed: A list of Booleans representing the keys being pressed currently
    :param sprite_status: A list holding info about the sprite's current status [facing left, action]
    :return: Updated sprite_status
    """
    # Space: Attack
    if keys_pressed[pygame.K_SPACE]:
        sprite_status[1] = 2
    # Both A and D: Idle
    elif keys_pressed[pygame.K_a] and keys_pressed[pygame.K_d]:
        sprite_status[1] = 0
    # A: Move Left
    elif keys_pressed[pygame.K_a]:
        if sprite.x - SPRITE_SPEED > -25:
            sprite.x -= SPRITE_SPEED
            sprite_status[0], sprite_status[1] = True, 1
        else:
            sprite_status[0], sprite_status[1] = True, 0
    # D: Move Right
    elif keys_pressed[pygame.K_d]:
        if sprite.x + SPRITE_SPEED < WIDTH - 275:
            sprite.x += SPRITE_SPEED
            sprite_status[0], sprite_status[1] = False, 1
        else:
            sprite_status[0], sprite_status[1] = False, 0
    # Idle facing previous direction if no other appropriate action
    else:
        sprite_status[1] = 0

    return sprite_status


def handle_slimes(slimes, kills, last_slime, current_time, sprite_status):
    """Handles slime spawns and movement

    :param slimes: A 2D list of Rect objects representing slime enemies coming from left and right
    :param kills: An int for the number of slime kills
    :param last_slime: An int representing the milliseconds since the last slime was spawned
    :param current_time: An int representing the current time
    :param sprite_status: A list containing sprite info
    :return: Returns last_slime, either as given or a newly updated one if a slime was spawned
    """
    # Set slime speed between min and max based on kills
    slime_speed = SLIME_MIN_SPEED + kills / SLIME_SPEED_MODIFIER
    if slime_speed > SLIME_MAX_SPEED:
        slime_speed = SLIME_MAX_SPEED

    # Set slime spawn time between min and max based on kills
    slime_delay = SLIME_DELAY_MAX - SLIME_DELAY_MODIFIER * kills
    if slime_delay < SLIME_DELAY_MIN:
        slime_delay = SLIME_DELAY_MIN

    # Set slime spawn cap based on kills
    slime_cap = SLIME_CAP_MIN + kills // SLIME_CAP_MODIFIER
    if slime_cap > SLIME_CAP_MAX:
        slime_cap = SLIME_CAP_MAX

    # Move the slimes
    for slime in slimes[0]:
        slime.x += slime_speed
    for slime in slimes[1]:
        slime.x -= slime_speed

    # If it's time to spawn a slime and there are less than the max currently alive
    if current_time - last_slime >= slime_delay and len(slimes[0]) + len(slimes[1]) < slime_cap:
        # Spawn a slime on the left if facing right
        if not sprite_status[0]:  # Would be easier to do "if" than "if not" but this was a bug patch
            slime = pygame.Rect(-SLIME_WIDTH, SLIME_Y, SLIME_WIDTH, SLIME_HEIGHT)
            slimes[0].append(slime)
        # Spawn a slime on the right if facing left
        else:
            slime = pygame.Rect(WIDTH, SLIME_Y, SLIME_WIDTH, SLIME_HEIGHT)
            slimes[1].append(slime)

        # Update last_slime time
        last_slime = current_time

    return last_slime


def handle_attacks(sprite, slimes, kills, sprite_status):
    """Handles player and slime attacks and deaths

    :param sprite: A Rect object representing the sprite
    :param slimes: A 2D list of slime Rect objects, a left list and a right list
    :param kills: An int for the current number of slime kills
    :param sprite_status: A list containing sprite info
    :return: Up-to-date kills int
    """
    # Get sprite's center position
    sprite_center = sprite.x + SPRITE_WIDTH / 2

    # For each slime with left spawn
    for slime in slimes[0]:
        slime_center = slime.x + SLIME_WIDTH / 2

        # If sprite is facing left and attacking, and slime is within sword range
        if sprite_status == [True, 2] and 0 < sprite_center - slime_center < SPRITE_SWORD_WIDTH:
            # Remove the slime, update kills, and play slime death sound
            slimes[0].remove(slime)
            kills += 1
            SLIME_DEATH_SOUND.play()

        # Elif the slime is touching the player, post the PLAYER_ATTACKED event
        elif sprite_center - slime_center < SPRITE_BODY_WIDTH:
            pygame.event.post(pygame.event.Event(PLAYER_ATTACKED))

    # For each slime with right spawn
    for slime in slimes[1]:
        slime_center = slime.x + SLIME_WIDTH / 2

        # If sprite is facing right and attacking, and slime is within sword range
        if sprite_status == [False, 2] and 0 < slime_center - sprite_center < SPRITE_SWORD_WIDTH:
            # Remove the slime, update kills, and play slime death sound
            slimes[1].remove(slime)
            kills += 1
            SLIME_DEATH_SOUND.play()

        # Elif the slime is touching the player, post the PLAYER_ATTACKED event
        elif slime_center - sprite_center < SPRITE_BODY_WIDTH:
            pygame.event.post(pygame.event.Event(PLAYER_ATTACKED))

    return kills


def game_end(sprite, slimes, kills):
    """Handles the end of the game and the appropriate screens

    :param sprite: A Rect object representing the sprite
    :param slimes: A 2D list of slime Rect objects, a left list and a right list
    :param kills: An int for the current number of slime kills
    :return:
    """
    GAME_OVER_SOUND.play()

    # For each frame in the DIE animation
    for i in range(DIE_FRAME_COUNT):
        # Draw the game
        draw_game(sprite, DIE[i], slimes, kills, 1)

        # 1 frame per 60ms
        pygame.time.delay(60)

    # Holds the last frame for 1.5 seconds
    pygame.time.delay(1500)

    # Draws the win/loss screen for 3 seconds
    draw_game(sprite, DIE[-1], slimes, kills, 2)
    pygame.time.delay(3000)

    # Draws the high score screen for 5 seconds
    draw_game(sprite, DIE[-1], slimes, kills, 3)

    # Records the current game's score to the scorekeeper file
    record_score(SCOREKEEPER_FILE_PATH, kills)

    # Hold high score screen for 5 seconds
    pygame.time.delay(5000)


def game():
    """A recursive loop to run the game"""
    # Refresh top of event queue to prevent death bugs
    pygame.event.post(pygame.event.Event(NEW_GAME))

    # Create clock to control framerate
    clock = pygame.time.Clock()

    # Create character object
    sprite = pygame.Rect(WIDTH / 2 - SPRITE_WIDTH / 2, SPRITE_Y, SPRITE_WIDTH, SPRITE_HEIGHT)

    # Slime variables
    slimes = [[], []]
    kills = 0
    last_slime = pygame.time.get_ticks()

    # Create sprite status tracker
    # [facing left (True=left, False=right), action (0=idle, 1=run, 2=attack]
    sprite_status = [False, 0]

    # Create variables to change and track frames
    frame_index = 0
    last_sprite_frame = pygame.time.get_ticks()

    # Loop condition
    game_running = True

    # Game loop
    while game_running:
        # Set frame rate
        clock.tick(FPS)

        # Store previous sprite status
        prev_action = sprite_status

        # For each game event
        for event in pygame.event.get():
            # If there is a quit event (press X on window), quit and end loop
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()

        # Get keys being pressed and process key input
        keys_pressed = pygame.key.get_pressed()
        process_keys(sprite, keys_pressed, sprite_status)

        # If sprite is attacking
        if sprite_status[1] == 2:
            # Set attack animation based on direction the sprite is facing
            if sprite_status[0]:
                current_animation = flip_animation(ATTACK)
            else:
                current_animation = ATTACK

        # If sprite is running
        elif sprite_status[1] == 1:
            # Set run animation based on direction the sprite is facing
            if sprite_status[0]:
                current_animation = flip_animation(RUN)
            else:
                current_animation = RUN

        # If sprite is idle
        else:
            # Set idle animation based on direction the sprite is facing
            if sprite_status[0]:
                current_animation = flip_animation(IDLE)
            else:
                current_animation = IDLE

        # Get current game time
        current_time = pygame.time.get_ticks()

        # Handle slime generation and movement, update last_slime if applicable
        last_slime = handle_slimes(slimes, kills, last_slime, current_time, sprite_status)

        # Handle player and slime attacks, update kills if applicable
        kills = handle_attacks(sprite, slimes, kills, sprite_status)

        # If player is hit, game ends
        if event.type == PLAYER_ATTACKED:
            game_end(sprite, slimes, kills)
            break

        # Ensures frame_index is never higher than what the animation allows
        # Frame index does not automatically reset when going from attack to run,
        # but this allows for a stylized "running jab" animation
        if frame_index >= len(current_animation):
            frame_index = 0

        # If it is time to change the sprite's animation frame
        if current_time - last_sprite_frame >= SPRITE_FRAME_DELAY:
            # If the current animation has no more frames, go back to the first frame
            if frame_index + 1 >= len(current_animation):
                frame_index = 0
            # Elif the action hasn't changed, go to the next frame in its animation
            elif prev_action == sprite_status:
                frame_index += 1

            # Update the time of last sprite frame change
            last_sprite_frame = current_time

        draw_game(sprite, current_animation[frame_index], slimes, kills)

    # Restart game
    game()


if __name__ == "__main__":
    # Initialize pygame libraries needed
    pygame.font.init()
    pygame.mixer.init()

    # Framerate
    FPS = 60

    # Positions and sizes
    WIDTH, HEIGHT = 1280, 960
    SPRITE_WIDTH, SPRITE_HEIGHT = 300, 250
    SPRITE_BODY_WIDTH, SPRITE_SWORD_WIDTH = 70, 155  # from sprite center to horizontal edge of hitbox
    SLIME_WIDTH, SLIME_HEIGHT = 200, 200
    SPRITE_Y = 550  # Characters cannot move up or down
    SLIME_Y = 599  # Characters cannot move up or down

    # Events
    PLAYER_ATTACKED = pygame.USEREVENT + 1
    NEW_GAME = pygame.USEREVENT + 3  # Puts a new event in the queue to prevent endless death loops

    # Speeds
    SPRITE_SPEED = 6
    SLIME_MIN_SPEED = 3
    SLIME_MAX_SPEED = 10

    # Spawn and update constraints
    SPRITE_FRAME_DELAY = 60  # milliseconds
    SLIME_DELAY_MAX = 1400  # milliseconds
    SLIME_DELAY_MIN = 200  # milliseconds
    SLIME_CAP_MIN = 1
    SLIME_CAP_MAX = 10

    # Slime stat multipliers
    SLIME_SPEED_MODIFIER = 7
    SLIME_DELAY_MODIFIER = 20
    SLIME_CAP_MODIFIER = 10

    # Frame counts for each animation png sheet
    ATTACK_FRAME_COUNT = 15  # milliseconds
    DIE_FRAME_COUNT = 4
    IDLE_FRAME_COUNT = 1
    RUN_FRAME_COUNT = 8

    # Designate color RGB values
    BLACK = (0, 0, 0)
    GREY = (180, 180, 180)
    TRANSLUCENT_GREY = (0, 0, 0, 160)
    WHITE = (255, 255, 255)
    RED = (230, 0, 0)

    # Scorekeeper filepath
    SCOREKEEPER_FILE_PATH = "scorekeeper.txt"

    # Retrieve font file and create font assets
    DEATH_FONT = pygame.font.Font("Assets/pixelmix.ttf", 140)
    TITLE_FONT = pygame.font.Font("Assets/pixelmix.ttf", 80)
    NORMAL_FONT = pygame.font.Font("Assets/pixelmix.ttf", 60)

    # Retrieve sounds
    GAME_OVER_SOUND = pygame.mixer.Sound("Assets/game_over.wav")
    SLIME_DEATH_SOUND = pygame.mixer.Sound("Assets/slime_death.wav")

    # Retrieve images
    BACKGROUND = pygame.transform.scale(
        pygame.image.load('Assets/dungeon.jpeg'), (WIDTH, HEIGHT))
    SLIME_IMAGE = pygame.transform.scale(
        pygame.image.load('Assets/slime.png'), (SLIME_WIDTH, SLIME_HEIGHT))
    ATTACK_ANIMATION = pygame.transform.scale(
        pygame.image.load('Assets/attack.png'), (SPRITE_WIDTH * ATTACK_FRAME_COUNT, SPRITE_HEIGHT))
    DIE_ANIMATION = pygame.transform.scale(
        pygame.image.load('Assets/die.png'), (SPRITE_WIDTH * DIE_FRAME_COUNT, SPRITE_HEIGHT))
    IDLE_ANIMATION = pygame.transform.scale(
        pygame.image.load('Assets/idle.png'), (SPRITE_WIDTH * IDLE_FRAME_COUNT, SPRITE_HEIGHT))
    RUN_ANIMATION = pygame.transform.scale(
        pygame.image.load('Assets/run.png'), (SPRITE_WIDTH * RUN_FRAME_COUNT, SPRITE_HEIGHT))

    # Split each frame sheet into a list of individual frames
    ATTACK = split_frame_sheet(ATTACK_ANIMATION, ATTACK_FRAME_COUNT)
    DIE = split_frame_sheet(DIE_ANIMATION, DIE_FRAME_COUNT)
    IDLE = split_frame_sheet(IDLE_ANIMATION, IDLE_FRAME_COUNT)
    RUN = split_frame_sheet(RUN_ANIMATION, RUN_FRAME_COUNT)

    # Create game window
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slime Slicer")

    draw_start_screen()

    game()
