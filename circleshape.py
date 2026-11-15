import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.mass = radius ** 2

    def momentum(self) -> pygame.Vector2:
        return self.velocity * self.mass

    def collides_with(self, other: "CircleShape") -> bool:
        min_distance = self.radius + other.radius
        distance = self.position.distance_to(other.position)
        return distance <= min_distance

    def bounce_off(self, other):
        """
        Bounces two circles off each other elastically.
        Modifies self.velocity and other.velocity in-place.
        """
        # 1. Get the normal vector pointing from Circle 2 to Circle 1
        normal = self.position - other.position
        
        # Avoid division by zero if positions are exactly identical
        if normal.length_squared() == 0:
            return 
            
        # 2. Get the squared distance between centers
        distance_squared = normal.length_squared()
        
        # 3. Calculate the relative velocity vector
        rel_velocity = self.velocity - other.velocity
        
        # 4. Use the dot product to find out how much velocity
        #    is traveling along the normal line
        # (If this value is > 0, they are already moving apart, so don't bounce again!)
        velocity_along_normal = rel_velocity.dot(normal)
        if velocity_along_normal > 0:
            return
    
        # 5. Calculate the scalar impulse (the magnitude of the bounce force)
        # Using your area-masses:
        #     (2 * m2) / (m1 + m2) * (vel_along_normal / dist_squared)
        impulse_factor = (2 * velocity_along_normal) / (self.mass + other.mass)
        
        # 6. Apply the bounce to both velocity vectors
        self.velocity -= (impulse_factor * other.mass) * (normal / distance_squared)
        other.velocity += (impulse_factor * self.mass) * (normal / distance_squared)

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass
