import pygame, sys # import pygame and sys

clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

pygame.display.set_caption('Pygame Window') # set the window name

WINDOW_SIZE = (600,400) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((300, 200)) # create a smaller surface for scaling

# Load player image
player_image = pygame.image.load('Player_standing-1.png (3).png').convert()
player_image.set_colorkey((255, 255, 255)) # make white transparent

# Load environment assets
grass_image = pygame.image.load('gras version 1-1.png (1).png') # load grass texture
TILE_SIZE = grass_image.get_width() # get tile size from grass image width

dirt_image = pygame.image.load('dirt_texture versio1-1.png (1).png') # load dirt texture

### Tile map for game world layout
game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

# ### Collision detection for tiles
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile): # check if rectangles collide
            hit_list.append(tile)
    return hit_list

### Function to handle player movement and collision response
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0] # move horizontally
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0: # moving right
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0: # moving left
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1] # move vertically
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0: # moving down
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0: # moving up
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

# Player movement state
moving_right = False
moving_left = False

player_y_momentum = 0 # gravity effect
air_timer = 0 # tracks time in the air

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height()) # player rectangle
test_rect = pygame.Rect(100,100,100,50) # test rectangle

# ### Main game loop
while True:
    display.fill((146,244,255)) # background color

    tile_rects = [] # list of all solid tiles
    y = 0
    for row in game_map: # iterate through tile map
        x = 0
        for tile in row:
            if tile == '1': # dirt tile
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2': # grass tile
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0': # add solid tiles to list
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    # ### Handle player velocity and collisions
    player_movement = [0, 0] # reset movement
    if moving_right:
        player_movement[0] += 2 # move right
    if moving_left:
        player_movement[0] -= 2 # move left
    player_movement[1] += player_y_momentum # apply gravity
    player_y_momentum += 0.2 # increase momentum (fall speed)
    if player_y_momentum > 3: # terminal velocity
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']: # landed on the ground
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1
    
    display.blit(player_image, (player_rect.x, player_rect.y)) # draw player

    # ### Event handling
    for event in pygame.event.get():
        if event.type == QUIT: # quit game
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN: # key press
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP: # jump
                if air_timer < 6: # prevent double jump
                    player_y_momentum = -5
        if event.type == KEYUP: # key release
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE) # scale display surface
    screen.blit(surf, (0, 0))
    pygame.display.update() # update display
    clock.tick(60) # maintain 60 fps
