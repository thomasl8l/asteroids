import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
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

    # Create groups for sprites
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    # Initialize player sprite, centered in the view
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)

    # Initialize asteroids
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
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
        # Draw sprites in view
        for sprite in drawable:
            sprite.draw(screen)
        # Detect collisions
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # Finally, refresh screen
        pygame.display.flip()
        # Restrict to 60fps; convert to seconds
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
