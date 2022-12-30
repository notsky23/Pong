# Implementation of classic arcade game Pong
import sys
import pygame
from pygame.locals import *
import random
import math

pygame.init()
fps = pygame.time.Clock()

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
counter = 0
score1 = 0
score2 = 0

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

score_color1 = WHITE
score_color2 = WHITE

#paddles position and velocity
paddle1_pos = [0, HEIGHT / 2]
paddle1_vel = [0, 0]
paddle2_pos = [WIDTH, HEIGHT / 2]
paddle2_vel = [0, 0]

random_x = random.choice([1, -1])
random_y = -1
if random_x > 0:
    RIGHT = True
    LEFT = False
elif random_x < 0:
    RIGHT = False
    LEFT = True

#ball position and velocity
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [(random_x * (random.randrange(120, 240)) / 60), (random_y * (random.randrange(60, 180)) / 60)]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, counter, score1, score2, score_color1, score_color2 # these are vectors stored as lists
    counter = 0
    
    if ((ball_pos[0] - 10 - PAD_WIDTH) <= 0):
        score2 += 1
        score_color1 = RED
        score_color2 = GREEN
    elif ((ball_pos[0] + 10 + PAD_WIDTH) >= WIDTH):
        score1 += 1
        score_color1 = GREEN
        score_color2 = RED
        
    ball_pos = [WIDTH / 2, HEIGHT / 2]
                
    if RIGHT:
        ball_vel = [(random.randrange(120, 240)) / 60, -1 * (random.randrange(60, 180)) / 60]
    elif LEFT:
        ball_vel = [-1 * (random.randrange(120, 240)) / 60, -1 * (random.randrange(60, 180)) / 60]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel, BALL_RADIUS, RIGHT, LEFT  # these are numbers
    global score1, score2, score_color1, score_color2  # these are ints
    
    paddle1_pos = [0, HEIGHT / 2]
    paddle1_vel = [0, 0]

    paddle2_pos = [WIDTH, HEIGHT / 2]
    paddle2_vel = [0, 0]
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    BALL_RADIUS = 10
    
    score1 = 0
    score2 = 0
    
    score_color1 = WHITE
    score_color2 = WHITE
    
    random_x = random.choice([1, -1])
    random_y = -1
    if random_x > 0:
        RIGHT = True
        LEFT = False
    elif random_x < 0:
        RIGHT = False
        LEFT = True
    
    ball_vel = [(random_x * (random.randrange(120, 240)) / 60), (random_y * (random.randrange(60, 180)) / 60)]
    
def exploding_ball():
    global counter, BALL_RADIUS, ball_pos, RIGHT, LEFT
    
    if counter < 3:
        if (BALL_RADIUS < 20):
            BALL_RADIUS += 1
        elif BALL_RADIUS == 20:
            BALL_RADIUS = 1
            counter += 1
    elif counter == 3:
        if (BALL_RADIUS < 10):
            BALL_RADIUS += 1
        else:
            if RIGHT:
                LEFT = True
                RIGHT = False
                spawn_ball(LEFT)
            elif LEFT:
                LEFT = False
                RIGHT = True
                spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, BALL_RADIUS, RIGHT, LEFT, score_color1, score_color2
        
    # refresh screen
    canvas.fill(BLACK)

    # draw mid line and gutters
    pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # determine whether paddle and ball collide
    if ((ball_pos[0] - 10 - PAD_WIDTH) <= 0) and ((paddle1_pos[1] - HALF_PAD_HEIGHT) <= (ball_pos[1]) <= (paddle1_pos[1] + HALF_PAD_HEIGHT)):
        ball_vel[0] = math.ceil(ball_vel[0] * -1.1)
        ball_vel[1] = math.ceil(ball_vel[1] * 1.1)
        ball_pos[0] = 0 + PAD_WIDTH + 10 + 1
        LEFT = False
        RIGHT = True    
        if ball_vel[0] == 0:
            BALL_RADIUS = 10
            score2 += 1
            score_color1 = RED
            score_color2 = GREEN
            spawn_ball(RIGHT)
    elif ((ball_pos[0] + 10 + PAD_WIDTH) >= WIDTH) and ((paddle2_pos[1] - HALF_PAD_HEIGHT) <= (ball_pos[1]) <= (paddle2_pos[1] + HALF_PAD_HEIGHT)):
        ball_vel[0] = math.ceil(ball_vel[0] * -1.1)
        ball_vel[1] = math.ceil(ball_vel[1] * 1.1)
        ball_pos[0] = WIDTH - PAD_WIDTH - 20 - 1
        LEFT = True
        RIGHT = False
        if ball_vel[0] == 0:
            BALL_RADIUS = 10
            score1 += 1
            score_color1 = GREEN
            score_color2 = RED
            spawn_ball(LEFT)
    elif ((ball_pos[1] - 10) <= 0) or ((ball_pos[1] + 10) >= HEIGHT):
        ball_vel[1] = math.ceil(ball_vel[1] * -1)
    elif ((ball_pos[0] - 10 - PAD_WIDTH) <= 0) or ((ball_pos[0] + 10 + PAD_WIDTH) >= WIDTH):
        ball_vel[0] = 0
        ball_vel[1] = 0
        exploding_ball()
            
    # draw ball
    pygame.draw.circle(canvas, YELLOW, ball_pos, BALL_RADIUS, 0)
    
    # update paddle's vertical position, keep paddle on the screen
    """ Movement of green paddle along the borders"""
    if ((paddle1_pos[1] - HALF_PAD_HEIGHT) > 0) and ((paddle1_pos[1] + HALF_PAD_HEIGHT) < HEIGHT):
        paddle1_pos[1] += paddle1_vel[1]
    elif (paddle1_pos[1] - HALF_PAD_HEIGHT) <= 0:
        paddle1_pos[1] = HALF_PAD_HEIGHT + 1
    elif (paddle1_pos[1] + HALF_PAD_HEIGHT) >= HEIGHT:
        paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT - 1
        
    """ Movement of blue paddle along the borders """
    if ((paddle2_pos[1] - HALF_PAD_HEIGHT) > 0) and ((paddle2_pos[1] + HALF_PAD_HEIGHT) < HEIGHT):
        paddle2_pos[1] += paddle2_vel[1]
    elif (paddle2_pos[1] - HALF_PAD_HEIGHT) <= 0:
        paddle2_pos[1] = HALF_PAD_HEIGHT + 1
    elif (paddle2_pos[1] + HALF_PAD_HEIGHT) >= HEIGHT:
        paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT - 1
        
    # draw paddles
    """ Position of paddles update as velocity is added or subtracted """
    pygame.draw.polygon(canvas, GREEN, ((paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT),
                     (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT)),
                     PAD_WIDTH)
    pygame.draw.polygon(canvas, BLUE, ((paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT),
                     (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)),
                     PAD_WIDTH)
    
    # draw scores
    # canvas.draw_text(str(score1), (130, 50), 50, score_color1)
    # canvas.draw_text(str(score2), (430, 50), 50, score_color2)
    font1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = font1.render(str(score1), True, score_color1)
    canvas.blit(label1, (130, 50))

    font2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = font2.render(str(score2), True, score_color2)
    canvas.blit(label2, (430, 50))
        
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    """ Velocity of green paddle while key is pressed """
    if event.key == K_w:
        paddle1_vel[1] -= 10
    elif event.key == K_s:
        paddle1_vel[1] += 10
    
    """ Velocity of blue paddle while key is pressed """
    if event.key == K_UP:
        paddle2_vel[1] -= 10
    elif event.key == K_DOWN:
        paddle2_vel[1] += 10
    
def keyup(key):
    global paddle1_vel, paddle2_vel

    """ Velocity of green paddle when key is released """
    if event.key in (K_w, K_s):
        paddle1_vel[1] = 0

    """ Velocity of blue paddle when key is released """
    if event.key in (K_UP, K_DOWN):
        paddle2_vel[1] = 0

        
# create frame
# frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Pong')

# register handlers
# frame.set_draw_handler(draw)
# frame.set_keydown_handler(keydown)
# frame.set_keyup_handler(keyup)
# frame.add_button("Restart", new_game, 200)

# start frame
# new_game()
# frame.start()
while True:

    draw(window)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps.tick(60)
