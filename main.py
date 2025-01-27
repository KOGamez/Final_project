import pygame, sys, time # import pygame and sys

#sounds
pygame.mixer.init()

pygame.mixer.music.load('themesong.wav')


pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)
clock = pygame.time.Clock() # set up the clock

from pygame.locals import * # import pygame modules
pygame.init() # initiate pygame

pygame.display.set_caption('Pygame Window') # set the window name

WINDOW_SIZE = (800,400) # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate screen

display = pygame.Surface((600, 200)) # create a smaller surface for scaling

# Load player image
player_image = pygame.image.load('Player_standingv3-1.png.png')


# Load environment assets
grass_image = pygame.image.load('gras version 1-1.png (1).png') # load grass texture
TILE_SIZE = grass_image.get_width() # get tile size from grass image width

dirt_image = pygame.image.load('dirt_texture versio1-1.png (1).png') # load dirt texture
Wheat_image = pygame.image.load('Wheat.png') # load dirt texture
### Tile map for game world layout
game_map = [
    ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
    ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
    ['1','0','0','0','0','0','0','0','5','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','8','7','0','0','0','0','0','0','1'],
    ['1','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','1'],
    ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
    ['1','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1'],
    ['1','2','0','0','0','0','0','0','0','0','0','0','0','4','0','0','3','2','2','2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','6','0','2','1'],
    ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1','1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
    ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']
]

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
    
    display.fill((146, 244, 255))  # Background color

    tile_rects = []  # List of all solid tiles
    y = 0
    for row_index, row in enumerate(game_map):  # Iterate through tile map
        x = 0  # Reset x for each row
        for col_index, tile in enumerate(row):
            if tile == '1':  # Dirt tile
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':  # Grass tile
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '3':  # Wheat tile
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                # Check collision with wheat tile
                wheat_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if 224 <= player_rect.x <= 270 and player_rect.y >= 60:  # If player collides within the x range
                    
                    game_map[row_index][col_index] = '0'  # Replace wheat tile with empty space                
            if tile == '4':  # Wheat tile
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                # Check collision with wheat tile
                wheat_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
                if 176 <= player_rect.x <= 224 and player_rect.y > 61:  # If player collides within the x range
                   
                    game_map[row_index][col_index] = '0'  # Replace wheat tile with empty space
            if tile == '5':  # Wheat tile
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                # Check collision with wheat tile
                wheat_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
               
                if 96 <= player_rect.x <= 144 and player_rect.y <= 12:  # If player collides within the x range
                    pygame.mixer.music.play()
                    game_map[row_index][col_index] = '0'  # Replace wheat tile with empty space        
            if tile == '6':  # Wheat tile
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                # Check collision with wheat tile
                wheat_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
               
                if 512 <= player_rect.x <= 538 and player_rect.y >= 60:  # If player collides within the x range
                    
                    game_map[row_index][col_index] = '0'  # Replace wheat tile with empty space 
            if tile == '7':  # Wheat tile
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                # Check collision with wheat tile
                wheat_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
               
                if 448 <= player_rect.x <= 500 and player_rect.y <= 12:  # If player collides within the x range
                   
                    game_map[row_index][col_index] = '0'  # Replace wheat tile with empty space     
            if tile == '8':  # Wheat tile
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                display.blit(Wheat_image, (x * TILE_SIZE, y * TILE_SIZE))
                # Check collision with wheat tile
                wheat_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
               
                if 430 <= player_rect.x <= 448 and player_rect.y <= 12:  # If player collides within the x range
                    
                    game_map[row_index][col_index] = '0'  # Replace wheat tile with empty space   
                    
            if tile != '0':  # Add solid tiles to list
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1  # Increment x after processing each tile
        y += 1  # Increment y after processing each row




    # Handle player velocity and collisions
    player_movement = [0, 0]  # Reset movement
    if moving_right:
        player_movement[0] += 2  # Move right
    if moving_left:
        player_movement[0] -= 2  # Move left
        
    player_movement[1] += player_y_momentum  # Apply gravity
    player_y_momentum += 0.2  # Increase momentum (fall speed)
    if player_y_momentum > 3:  # Terminal velocity
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:  # Landed on the ground
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x, player_rect.y))  # Draw player

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:  # Quit game
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:  # Key press
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:  # Jump
                if air_timer < 6:  # Prevent double jump
                    player_y_momentum = -5
        if event.type == KEYUP:  # Key release
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    
    # Scale display surface to window size
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()  # Update display
    clock.tick(60)  # Maintain 60 FPS