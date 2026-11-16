import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    # Initialize and create a pygame.Surface for screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Manage frames per second (FPS)
    clock = pygame.time.Clock()
    # The delta time, for one frame
    dt = 0.0

    # Create groups (for containers) for sprites
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    # Initialize player sprite, centered in the view
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)

    # Initialize shots (fired from ship)
    Shot.containers = (shots, updatable, drawable)

    # Initialize asteroids
    Asteroid.containers = (asteroids, updatable, drawable)
    # AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    # The game loop, infinite
    while True:
        log_state()
        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Draw the background
        screen.fill("black")

        # Position sprites for this frame
        updatable.update(dt)
        if len(asteroids) < 10:
            asteroid_field.update(dt)
        # Draw sprites in view, keep within bounds
        for sprite in drawable:
            # Horizontal boundaries (Left and Right edges)
            if sprite.position.x - sprite.radius <= 0:
                sprite.position.x = sprite.radius  # Prevent getting stuck outside
                sprite.velocity.x *= -1          # Reverse horizontal direction
            
            elif sprite.position.x + sprite.radius >= SCREEN_WIDTH:
                sprite.position.x = SCREEN_WIDTH - sprite.radius
                sprite.velocity.x *= -1
            
            # Vertical boundaries (Top and Bottom edges)
            if sprite.position.y - sprite.radius <= 0:
                sprite.position.y = sprite.radius  # Prevent getting stuck outside
                sprite.velocity.y *= -1          # Reverse vertical direction
            
            elif sprite.position.y + sprite.radius >= SCREEN_HEIGHT:
                sprite.position.y = SCREEN_HEIGHT - sprite.radius
                sprite.velocity.y *= -1

            sprite.draw(screen)
        # Detect collisions
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split(shot)
                    shot.kill()
            for asteroid_2 in asteroids:
                if asteroid.collides_with(asteroid_2):
                    asteroid.bounce_off(asteroid_2)
                    break
            if player.collides_with(asteroid):
                player.bounce_off(asteroid)
              #   log_event("player_hit")
              #   print("Game over!")
              #   sys.exit()

        # Finally, refresh screen
        pygame.display.flip()
        # Restrict to 60fps; convert to seconds
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
