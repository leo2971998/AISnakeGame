import pygame
import time
import random

snake_speed = 15

# Window size
window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Load the images for snake head, snake body, and apple
snake_head_img = pygame.image.load('snake_head.png')
snake_head_img = pygame.transform.scale(snake_head_img, (20, 20))

snake_body_img = pygame.image.load('snake_body.png')
snake_body_img = pygame.transform.scale(snake_body_img, (20, 20))

apple_img = pygame.image.load('apple.png')
apple_img = pygame.transform.scale(apple_img, (20, 20))

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# fruit position
fruit_position = [random.randrange(1, (window_x//20)) * 20,
                  random.randrange(1, (window_y//20)) * 20]

fruit_spawn = True

# setting default snake direction towards right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0

# displaying Score function
def show_score(choice, color, font, size, score):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# game over function
def game_over(choice, color, font, size):
    game_over_font = pygame.font.SysFont(font, size)
    game_over_surface = game_over_font.render('Game Over!', True, color)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# AI to make snake auto-play
def auto_play(snake_position, snake_body, fruit_position, direction):
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    pos_if_move = {
        'UP': [snake_position[0], snake_position[1]-20],
        'DOWN': [snake_position[0], snake_position[1]+20],
        'LEFT': [snake_position[0]-20, snake_position[1]],
        'RIGHT': [snake_position[0]+20, snake_position[1]]
    }

    for d in directions:
        if (pos_if_move[d] in snake_body) or (pos_if_move[d][0] < 0) or (pos_if_move[d][0] >= window_x) or (pos_if_move[d][1] < 0) or (pos_if_move[d][1] >= window_y):
            directions.remove(d)

    if not directions:
        return direction

    # Check if snake and apple are in the same row or 1 row apart
    if abs(snake_position[1] - fruit_position[1]) <= 20:
        # Prioritize horizontal movement if apple is to the left or right
        if snake_position[0] > fruit_position[0]:
            if 'LEFT' in directions:
                return 'LEFT'
        else:
            if 'RIGHT' in directions:
                return 'RIGHT'
        # If can't move horizontally, then try vertical
        if snake_position[1] > fruit_position[1] and 'UP' in directions:
            return 'UP'
        elif 'DOWN' in directions:
            return 'DOWN'

    # General case (not in the same row or 1 row apart)
    directions_to_fruit = []
    if snake_position[0] == fruit_position[0]:  # same column
        if snake_position[1] > fruit_position[1]:
            directions_to_fruit.append('UP')
        else:
            directions_to_fruit.append('DOWN')
    else:  # not in the same row or column
        if snake_position[0] > fruit_position[0]:
            directions_to_fruit.append('LEFT')
        elif snake_position[0] < fruit_position[0]:
            directions_to_fruit.append('RIGHT')
        if snake_position[1] > fruit_position[1]:
            directions_to_fruit.append('UP')
        else:
            directions_to_fruit.append('DOWN')

    safe_directions_to_fruit = [d for d in directions if d in directions_to_fruit]
    if safe_directions_to_fruit:
        return safe_directions_to_fruit[0]
    else:
        return directions[0]



# Main Function
while True:

    direction = auto_play(snake_position, snake_body, fruit_position, direction)

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 20
    if direction == 'DOWN':
        snake_position[1] += 20
    if direction == 'LEFT':
        snake_position[0] -= 20
    if direction == 'RIGHT':
        snake_position[0] += 20

    # Rotate the snake head image based on the current direction
    if direction == 'UP':
        rotated_head_img = pygame.transform.rotate(snake_head_img, 90)
    elif direction == 'DOWN':
        rotated_head_img = pygame.transform.rotate(snake_head_img, -90)
    elif direction == 'LEFT':
        rotated_head_img = pygame.transform.flip(snake_head_img, True, False)
    else: # 'RIGHT'
        rotated_head_img = snake_head_img

    # Snake body growing mechanism
    # if fruits and snakes collide then scores will increase
    snake_body.insert(0, list(snake_position))
    if (abs(snake_position[0] - fruit_position[0]) < 20 and
            abs(snake_position[1] - fruit_position[1]) < 20):
        score += 1
        fruit_spawn = False
    else:
        snake_body.pop()

    # Spawning fruit
    # Spawning fruit
    if not fruit_spawn:
        while True:  # Keep trying until we get a valid apple position
            new_fruit_position = [random.randrange(1, (window_x//20)) * 20,
                                  random.randrange(1, (window_y//20)) * 20]
            if new_fruit_position not in snake_body:  # This ensures apple doesn't spawn inside the snake
                fruit_position = new_fruit_position
                fruit_spawn = True  # Move this line here
                break


    # GFX
    game_window.fill(black)
    # Draw the snake head
    game_window.blit(rotated_head_img, (snake_body[0][0], snake_body[0][1]))
    # Draw the rest of the snake body
    for pos in snake_body[1:]:
        game_window.blit(snake_body_img, (pos[0], pos[1]))
    game_window.blit(apple_img, (fruit_position[0], fruit_position[1]))

    # Game Over conditions
    # getting out of bounds
    if (snake_position[0] < 0 or snake_position[0] > window_x-20 or
            snake_position[1] < 0 or snake_position[1] > window_y-20):
        game_over('arial', red, 'arial', 20)
    # Touching the snake body
    for block in snake_body[1:]:
        if (snake_position[0] == block[0] and
                snake_position[1] == block[1]):
            game_over('arial', red, 'arial', 20)

    show_score(1, white, 'arial', 20, score)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
