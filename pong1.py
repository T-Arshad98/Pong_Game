# Pong V1
# This is a game where a ball bounces off the 4 edges of the screen and
# paddles. If it hits the left or right edge of the screen, the opposite 
# side gets a point. If it hits the inner side of the paddle, it bounces.
# V1 doesn't keep score or handle the ball colliding, it doesn't allow paddle
# movement, and it wraps instead of bouncing off the edges of the window 
# and paddle.

from uagame import Window
from time import sleep
import pygame
from pygame.locals import *

def main():
    # main algorithm: create the window and play the game
    window = Window('Pong', 500, 400)
    window.set_auto_update(False) # tell the window to only update when told, not automatically
    game = Game(window)
    game.play() # call .play() method to run game which is a Game object
    #window.close(), this doesn't work for some reason
    pygame.display.quit()   # close display
class Game:
    def __init__(self, window):
        # set up new Game object
        # self - the Game to initialize
        # window - uagame.Window object
        self.window = window
        self.close_clicked = False  # tells us if the window is trying to be closed
        self.balls = [ball(6, "white", [15, 5], self.window, [250, 200])] # ball properties in an array, can add more
        self.pause_time = 0.05  #how much time to wait between updates, smaller time is faster game, but also choppier
        
    def play(self):
        # while window is not trying to be closed, run the game
        while self.close_clicked == False:
            self.handle_events()
            self.draw_frame()
            self.update_state()
            sleep(self.pause_time)
                
    def handle_events(self):
        # check if window is trying to be closed. If it is, set bool to true
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.close_clicked = True
        
    def draw_frame(self):
        # draw/redraw everything on the screen
        self.window.clear()
        for ball in self.balls:
            ball.draw()
        rect_left = pygame.draw.rect(self.window.get_surface(), pygame.Color('white'), (90,170,10,60))
        rect_right = pygame.draw.rect(self.window.get_surface(), pygame.Color('white'), (400,170,10,60))
        self.window.update()
    
    def update_state(self):
        # move the ball
        for ball in self.balls:
            ball.move()
       

class ball:
    def __init__(self, size, color, velocity, window, position):
        # attributes of the ball(s)
        self.size = size
        self.color = color
        self.velocity = velocity
        self.window = window
        self.position = position
    
    def move(self):
        self.position[0] = (self.position[0] + self.velocity[0])%500
        self.position[1] = (self.position[1] + self.velocity[1])%400        
        self.wrap()
        #or do it all in one step by using modular arithmetic without Wrap
        #self.position[0] = (self.position[0] + self.velocity[0])%500
        #self.position[1] = (self.position[1] + self.velocity[1])%400

    def wrap(self):
        # possibly wraps the ball around the screen
        # self - the ball to wrap
        if self.position[1] <= 0:
            self.position[1] = self.window.get_height()
        elif self.position[1] >= self.window.get_height():
            self.position[1] = 0
        if self.position[0] <= 0:
            self.position[0] = self.window.get_width()
        elif self.position[0] >= self.window.get_width():
            self.position[0] = 0
    
    def draw(self):
        # draws the ball
        # self - the ball to draw
        pygame.draw.circle(
            self.window.get_surface(), 
            pygame.Color(self.color), 
            self.position, 
            self.size)

main()