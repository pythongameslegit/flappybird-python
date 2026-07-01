import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -6.5
PIPE_SPEED = 3
PIPE_GAP = 150
FPS = 60

# Colors (RGB)
SKY_BLUE = (113, 197, 207)
YELLOW = (247, 212, 59)
GREEN = (115, 191, 46)
WHITE = (255, 255, 255)

# Setup Screen and Clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 15

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += int(self.velocity)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.top_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - PIPE_GAP
        self.width = 60
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        # Top Pipe
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        pygame.draw.rect(screen, GREEN, top_rect)

        # Bottom Pipe
        bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height)
        pygame.draw.rect(screen, GREEN, bottom_rect)

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height)
        return top_rect, bottom_rect

def check_collision(bird, pipes):
    # Boundary check (ceiling and floor)
    if bird.y - bird.radius <= 0 or bird.y + bird.radius >= SCREEN_HEIGHT:
        return True

    # Pipe collision check
    bird_rect = bird.get_rect()
    for pipe in pipes:
        top_rect, bottom_rect = pipe.get_rects()
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
    return False

def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_over = False

    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        bird = Bird()
                        pipes = [Pipe()]
                        score = 0
                        game_over = False
                    else:
                        bird.flap()

        # 2. Game Logic
        if not game_over:
            bird.update()

            # Move pipes
            for pipe in pipes:
                pipe.update()

            # Spawn new pipes when the last pipe has traveled far enough
            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

            # Remove old pipes that left the screen
            if pipes[0].x < -pipes[0].width:
                pipes.pop(0)

            # Score tracking
            for pipe in pipes:
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1

            # Collision detection
            if check_collision(bird, pipes):
                game_over = True

        # 3. Drawing Elements
        screen.fill(SKY_BLUE)

        for pipe in pipes:
            pipe.draw()

        bird.draw()

        # UI Text
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("GAME OVER - Space to Restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
