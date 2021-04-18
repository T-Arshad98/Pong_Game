# Pong V2
# This is a game where a ball bounces off the 4 edges of the screen and
# paddles. If it hits the left or right edge of the screen, the opposite 
# side gets a point. If it hits the inner side of the paddle, it bounce;
# otherwise, it goes through. V2 doesn't allow paddles movements.

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
        self.game_over = False
        
        self.text_size = 80
        self.text_color = "white"
        window.set_font_size(self.text_size)
        window.set_font_color(self.text_color)     
        
        self.score = [0,0]    
        self.rect_left = Rect((90,170),(10,60))
        self.rect_right = Rect((400,170),(10,60))         
        self.balls = [ball(6, "white", [10, 3], self.window, [250, 200], self.score, self.rect_left, self.rect_right)] # ball properties in an array, can add more ball objects
        self.pause_time = 1/59  #how much time to wait between updates, smaller time is faster game, but also choppier

    def play(self):
        # while window is not trying to be closed, run the game
        while self.close_clicked == False:
            self.handle_events()      
            self.draw_frame()  
            # if game is not over (score not reached 11), update the state
            if self.game_over == False:
                self.update_state()
            sleep(self.pause_time)
                
    def handle_events(self):
        # check if window is trying to be closed. If it is, set bool to true
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.close_clicked = True
        #check if score has reached 11, which is when the game should stop
        if self.score[0] == 11:
            self.game_over = True
        elif self.score[1] == 11:
            self.game_over = True
            
    def draw_frame(self):
        # draw/redraw everything on the screen
        self.window.clear() 
        # draw the rectangular paddles
        pygame.draw.rect(self.window.get_surface(), pygame.Color('white'), self.rect_left)
        pygame.draw.rect(self.window.get_surface(), pygame.Color('white'), self.rect_right)  
        # draw the left score on the top left corner
        self.window.draw_string(str(self.score[0]), 0, 0)
        #draw the right score on the top right corner
        self.window.draw_string(str(self.score[1]), ((self.window.get_width())-(self.window.get_string_width(str(self.score[1])))), 0)
        
        for ball in self.balls:
            ball.draw()
        self.window.update()
    
    def update_state(self):
        # move the ball
        for ball in self.balls:
            ball.move()
       

class ball:
    def __init__(self, size, color, velocity, window, position, score, rect_left, rect_right):
        # attributes of the ball(s)
        self.size = size
        self.color = color
        self.velocity = velocity
        self.window = window
        self.position = position
        self.score = score
        self.rect_left = rect_left
        self.rect_right = rect_right
    
    def move(self):
        self.position[0] = self.position[0] + self.velocity[0]
        self.position[1] = self.position[1] + self.velocity[1]      
        self.screen_bounce()
        self.paddles_bounce()
        
    def screen_bounce(self):
        # possibly bounces the ball around the screen sides
        # self - the ball to bounce
        # change the score if the ball hits the left or right edge
        
        if self.position[1] <= 0:
            self.velocity[1] = -self.velocity[1]
        elif self.position[1] >= self.window.get_height():
            self.velocity[1] = -self.velocity[1]          
            
        if self.position[0] <= 0:
            self.velocity[0] = -self.velocity[0]  
            self.score[0] += 1            
        elif self.position[0] >= self.window.get_width():
            self.velocity[0] = -self.velocity[0]  
            self.score[1] += 1        
            
    def paddles_bounce(self):
        # possibly bounces the ball on the paddles
        # self - the ball to bounce     
        
        # if ball collides with left paddle
        if self.rect_left.collidepoint(self.position):
            # if velocity is negative, make it positive
            if self.velocity[0] < 0:
                self.velocity[0] = -self.velocity[0]  
                
        # if ball collides with right paddle
        if self.rect_right.collidepoint(self.position):
            # if velocity is positive, make it negative
            if self.velocity[0] > 0:
                self.velocity[0] = -self.velocity[0]                 
            
    def draw(self):
        # draws the ball
        # self - the ball to draw
        pygame.draw.circle(
            self.window.get_surface(), 
            pygame.Color(self.color), 
            self.position, 
            self.size)

main()