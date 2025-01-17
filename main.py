import pygame, sys  # Import the pygame and sys modules

clock = pygame.time.Clock()  

from pygame.locals import *  
pygame.init()  #initialize all imported pygame modules

pygame.display.set_caption('Wealth of fields')  #set the title of the window

WINDOW_SIZE = (400, 400)  #size of the window  

player_image = pygame.image.load('Player_standing.png') 

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  #set up the display window

moving_right = False
moving_left = False

player_location = [50,50]
Player_y_momentum = 0

while True:  ##start the main game loop
    screen.fill((146,244,255))
    screen.blit(player_image,player_location)


    #brackets call xyval change
    if player_location_

    #brackets call xval change
    if moving_right == True:
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4

    ##process events in the event for any usser
    for event in pygame.event.get():

         #exit program func  
        if event.type == QUIT:  #quit event is triggered
            pygame.quit()       #uninitialize all pygame modules
            sys.exit()          #exit the program
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False



    pygame.display.update()  #updates any images or updates applied
    clock.tick(60)           #frame rate to 60 frames per second
