"""
Tarea 1: Ackerman steering simulator
Yosthin Daniel Galindo Castro 587226
Profesor: Dr. Andres Hernandez Gutierrez
"""
# Import the pygame module
import pygame

# Import the numpy library
import numpy as np

# import argparse library
import argparse

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_f,
    K_s,
    KEYDOWN,
    QUIT,
)

# Parse the properties given in the command line by the user
parser =argparse.ArgumentParser(description='Enter the properties')
parser.add_argument('--speed', type=float, help='Vehicle speed')
parser.add_argument('--lf', type=float, help=' Distance from vehicle’s centre of mass to the front wheel axle')
parser.add_argument('--lb', type=float, help='Distance from the vehicle’s centre of mass to the back wheel axle')
parser.add_argument('--x0', type=float, help='Initial position of x')
parser.add_argument('--y0', type=float, help='Initial position of y')
parser.add_argument('--phi0', type=float, help=' Initial heading angle')
parser.add_argument('--df0', type=float, help='Initial front wheel rotation angle')
parser.add_argument('--dt', type=float, help='Sampling time interval.')

# Parse all the arguments in the variable "parser"
args = parser.parse_args()

# Define constants like the screen width and height, delta increment, speed increment, etc.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
delta_f_increment = 1.2*np.pi/180
speed_incr = 10/3.6
points = []
Color_line = (255,0,0)
blue = (0, 0, 128)
green = (0, 255, 0)
print(type(green))

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #self.rect = pygame.Rect(rect)
        
        # Load an image of a triangle as the vehicle
        self.surf = pygame.image.load("triangle.png")
        
        # Get all the arguments parsed before and made them an attribute of 'player'
        self.speed = args.speed/3.6
        self.lf = args.lf
        self.lb = args.lb
        self.playerX = SCREEN_WIDTH/2 + args.x0
        self.playerY = SCREEN_HEIGHT/2 + args.y0
        self.phi0 = args.phi0
        self.df0 = args.df0
        self.dt = args.dt
        

    # Move the sprite based on user keypresses
    def update(self, pressed_keys): 
        
        # Up key for moving forward
        if pressed_keys[K_UP]:
            # Right key for increasing delta f
            if pressed_keys[K_RIGHT]:
                self.df = self.df0 + delta_f_increment

             # Left key for decreasing delta f   
            elif pressed_keys[K_LEFT]:
                self.df = self.df0 - delta_f_increment

            # if left and right are not being pressed delta f will be 0 
            else:
                  self.df = 0
                              
            # Ackerman steering equations
            self.beta = np.arctan2(self.lb*np.tan(self.df),(self.lf + self.lb))
            self.playerX += self.speed*self.dt*np.cos(self.phi0+self.beta)
            self.playerY += self.speed*self.dt*np.sin(self.phi0+self.beta)
            self.phi0 -= self.speed * self.dt * ((np.cos(self.beta) * np.tan(self.df)) / (self.lf + self.lb))

        # Down key for moving forward
        if pressed_keys[K_DOWN]:
            
            # Right key for increasing delta f
            if pressed_keys[K_RIGHT]:
                self.df = self.df0 + delta_f_increment
            
            # Left key for decreasing delta f
            elif pressed_keys[K_LEFT]:
                self.df = self.df0 - delta_f_increment

            # if left and right are not being pressed delta f will be 0                 
            else:
                self.df = 0
                
            # Ackerman steering equations
            self.beta = np.arctan2(self.lb*np.tan(self.df),self.lf + self.lb)
            self.playerX -= self.speed*self.dt*np.cos(self.phi0+self.beta) 
            self.playerY -= self.speed*self.dt*np.sin(self.phi0+self.beta)             
            self.phi0 += self.speed * self.dt * ((np.cos(self.beta) * np.tan(self.df)) / (self.lf + self.lb))

        # f key for increasing speed
        if pressed_keys[K_f]:
            # Speed is topped to 250 km/h
            if self.speed < 250/3.6:
                self.speed += speed_incr

            else:
                self.speed = 250/3.67

        # s key for decreasing speed  
        if pressed_keys[K_s]:
            # Speed can not be less than 0
            if self.speed  > 0:
                self.speed -= speed_incr
            else:
                self.speed = 0

        # Keep player on the screen
        if self.playerX < 0:
            self.playerX = 0
        if self.playerX > SCREEN_WIDTH-32:
            self.playerX = SCREEN_WIDTH-32
        if self.playerY < 0:
            self.playerY = 0
        if self.playerY >= SCREEN_HEIGHT-32:
            self.playerY = SCREEN_HEIGHT-32
        
        # append the places where the player has been and draw circles
        points.append((player.playerX,player.playerY))
        for p1,p2 in offset(points):
            if p1 and p2:
                pygame.draw.circle(screen, Color_line,p1, 2)

# Function for getting the previous place where the player was
def offset(iterable):
    prev = None
    for elem in iterable:
        yield prev, elem
        prev = elem


# Initialize pygame
pygame.init()  

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
 
# Instantiate player.
player = Player()

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 15)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
    
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # create a text surface object,
    # on which text is drawn on it.
    text = font.render('Config Params', True, Color_line)
    text2 = "Speed: {} km/h".format(str(player.speed*3.6))
    text2 = font.render(text2, True, Color_line)
    text3 = "Delta T: {} s".format(str(player.dt))
    text3 = font.render(text3, True, Color_line)
    text4 = "Delta f increment: {} deg".format(str(delta_f_increment*180/np.pi))
    text4 = font.render(text4, True, Color_line) 
    text5 = "Lb: {} m".format(str(player.lb))
    text5 = font.render(text5, True, Color_line)
    text6 = "Lf: {} m".format(str(player.lf))
    text6 = font.render(text6, True, Color_line) 
    text_veh = "{} m, {} m, {} degs ".format(str(round(player.playerX-SCREEN_WIDTH/2,4)), str(round(player.playerY-SCREEN_HEIGHT/2,4)), str(round(-player.phi0*180/np.pi,4)))
    text_veh = font.render(text_veh, True, Color_line) 

    # Display the text
    screen.blit(text, (10,10))
    screen.blit(text2, (10,30))
    screen.blit(text3, (10,50))
    screen.blit(text4, (10,70))
    screen.blit(text5, (10,90))
    screen.blit(text6, (10,110))
    screen.blit(text_veh, (player.playerX,player.playerY-20))

    # Draw the player on the screen
    screen.blit(player.surf, (player.playerX,player.playerY))
    
    # Update the display
    pygame.display.flip()
    
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)
