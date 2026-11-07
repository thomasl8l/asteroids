import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player


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

    # The player sprite, centered in the view
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)

    # The game loop, infinite
    while True:
        log_state()
        # Handle any input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Draw the background
        screen.fill("black")

        # Position player for this frame
        player.update(dt)
        # Draw player in view
        player.draw(screen)

        # Finally, refresh screen
        pygame.display.flip()
        # Restrict to 60fps; convert to seconds
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
