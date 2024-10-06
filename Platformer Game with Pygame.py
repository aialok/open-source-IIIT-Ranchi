#pip install pygame

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 60
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Platformer Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.velocity_y = 0
        self.jumping = False
        self.on_ground = False
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        # Left and Right movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Keep the player on the screen horizontally
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH
        
        # Check if the player is on the ground
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.jumping = False
            self.on_ground = True
    
    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.jumping = True
            self.on_ground = False

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create platforms
platform1 = Platform(200, 400, 200, 20)
platform2 = Platform(500, 300, 200, 20)
platform3 = Platform(100, 500, 150, 20)

all_sprites.add(platform1, platform2, platform3)
platforms.add(platform1, platform2, platform3)

# Main game loop
def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
        
        # Update player
        player.update()
        
        # Check for collisions between the player and platforms
        for platform in platforms:
            if player.rect.colliderect(platform.rect) and player.velocity_y > 0:
                player.rect.bottom = platform.rect.top
                player.velocity_y = 0
                player.jumping = False
                player.on_ground = True
        
        # Clear the screen
        screen.fill((135, 206, 235))  # Sky blue background
        
        # Draw all sprites
        all_sprites.draw(screen)
        
        # Refresh the screen
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
