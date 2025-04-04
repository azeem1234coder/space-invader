import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize the Pygame mixer for sound
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game variables
player_speed = 5
bullet_speed = 7
enemy_speed = 2
enemy_drop_speed = 10
score = 0

# Fonts
font = pygame.font.SysFont('Arial', 30)

# Load sound effects
gunshot_sound = pygame.mixer.Sound('laser-gun-72558.mp3')  # Path to your gunshot sound file
explosion_sound = pygame.mixer.Sound('medium-explosion-40472.mp3')  # Path to your explosion sound file

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.png')  # Load a player image
        self.image = pygame.image.load('player.png')  # Load a player image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = player_speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        gunshot_sound.play()  # Play gunshot sound when player fires

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Simple rectangle bullet
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ww.png')  # Load an enemy image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = enemy_speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

# Explosion Class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Make a simple circular explosion
        pygame.draw.circle(self.image, GREEN, (25, 25), 25)  # Create a green explosion
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 20  # Explosion lasts for 20 frames

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()  # Kill the explosion after it finishes

# Set up sprites and sprite groups
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

bullets = pygame.sprite.Group()

enemies = pygame.sprite.Group()

# Create some enemies
for i in range(50):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Create an empty group for explosions
explosions = pygame.sprite.Group()

# Game Loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    # Update game state
    all_sprites.update()

    # Collision detection
    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        if hit_enemies:
            bullet.kill()
            for enemy in hit_enemies:
                score += 20
                explosion_sound.play()  # Play explosion sound when enemy is hit
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                all_sprites.add(explosion)
                explosions.add(explosion)

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Set frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
