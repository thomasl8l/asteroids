import pygame
import random
from logger import log_event
from circleshape import CircleShape
from shot import Shot
from constants import (
    LINE_WIDTH,
    ASTEROID_MIN_RADIUS
)


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        self.color: pygame.Color = self.random_color()

    def random_color(self) -> pygame.Color:
        options = ["66", "99"]
        # 1. Generate the random hex pairs
        r_hex = random.choice(options)
        g_hex = random.choice(options)
        b_hex = random.choice(options)
        # 2. Convert hex strings (base 16) to decimal integers
        r = int(r_hex, 16)  # "66" becomes 102, "99" becomes 153
        g = int(g_hex, 16)
        b = int(b_hex, 16)

        return pygame.Color(r, g, b)

    def split(self, shot: Shot) -> None:
        self.kill()
        # Maybe split into smaller asteroids
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        # Adjust vector based on impact with shot
        # (a.vel * a.mass + b.vel * b.mass) / total_mass = velocity
        self.velocity = (
            (self.momentum() + shot.momentum()) / (self.mass + shot.mass)
        )
        # Make two new smaller asteroids
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        vel_1 = self.velocity.rotate(angle)
        vel_2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        # ...first new asteroid
        asteroid_1 = Asteroid(
            self.position.x, self.position.y, new_radius
        )
        asteroid_1.velocity = vel_1 * 1.2
        # ...second new asteroid
        asteroid_2 = Asteroid(
            self.position.x, self.position.y, new_radius
        )
        asteroid_2.velocity = vel_2 * 1.2
        # Ensure they are not colliding
        while asteroid_1.collides_with(asteroid_2):
            asteroid_1.position += asteroid_1.velocity * 0.1
            asteroid_2.position += asteroid_2.velocity * 0.1

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen, self.color, self.position, self.radius
        )

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
