import pygame
import sys
import math
import random


class Particle:
    """
    A base class for particles.

    Attributes:
        x (float): The x-coordinate of the particle.
        y (float): The y-coordinate of the particle.
        radius (int): The radius of the particle.
        color (tuple): The color of the particle.
        shape (str): The shape of the particle ('circle' or 'square').

    Methods:
        move(): Moves the particle (to be implemented in subclasses).
        update_color(): Updates the color of the particle (to be implemented in subclasses).
    """

    def __init__(self, x, y, radius, shape):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 255, 255)  # Default white color
        self.shape = shape  # 'circle' or 'square'

    def move(self):
        pass

    def update_color(self, width, height):
        pass

    def collision_behaviour(self):
        pass

    def speed(self):
        return 0


class LinearParticle(Particle):
    """
    A class representing a particle that moves linearly.

    Attributes:
        speed_x (float): The speed of the particle along the x-axis.
        speed_y (float): The speed of the particle along the y-axis.

    Methods:
        move(): Moves the particle and bounces off the edges.
        update_color(): Updates the color based on the x-coordinate.
    """

    def __init__(self, x, y, radius, speed_x, speed_y, shape='circle'):
        super().__init__(x, y, radius, shape)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def update_color(self, width, height):
        if self.x < width // 2:
            self.color = (255, 165, 0)  # Orange
        else:
            self.color = (0, 0, 255)  # Blue

    def collision_behaviour(self):
        # Collision detected
        self.speed_y = -self.speed_y
        self.speed_x = -self.speed_x

    def speed(self):
        return math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)


class CircularParticle(Particle):
    """
    A class representing a particle that moves in a circular orbit.

    Attributes:
        center_x (float): The x-coordinate of the center of the orbit.
        center_y (float): The y-coordinate of the center of the orbit.
        orbit_radius (float): The radius of the orbit.
        angle (float): The current angle in the orbit.
        angle_speed (float): The speed of the particle along the orbit.

    Methods:
        move(): Moves the particle along its circular orbit.
        update_color(): Updates the color based on the y-coordinate.
    """

    def __init__(self, x, y, radius, center_x, center_y, orbit_radius, angle_speed, shape='circle'):
        super().__init__(x, y, radius, shape)
        self.center_x = center_x
        self.center_y = center_y
        self.orbit_radius = orbit_radius
        self.angle = 0
        self.angle_speed = angle_speed

    def move(self):
        self.angle += self.angle_speed
        self.x = self.center_x + self.orbit_radius * math.cos(self.angle)
        self.y = self.center_y + self.orbit_radius * math.sin(self.angle)

    def update_color(self, width, height):
        if self.y < height // 2:
            self.color = (255, 0, 0)  # Red
        else:
            self.color = (0, 255, 0)  # Green

    def collision_behaviour(self):
        self.angle_speed = -self.angle_speed

    def speed(self):
        return self.angle_speed * self.orbit_radius


class Simulator:
    """
    A class to simulate the movement and interaction of particles.

    Attributes:
        width (int): The width of the simulation screen.
        height (int): The height of the simulation screen.
        particles (list): A list of particles in the simulation.
        contact_aware (bool): A flag to enable or disable collision detection.
        screen (pygame.Surface): The pygame screen object.
        clock (pygame.time.Clock): The pygame clock object.

    Methods:
        init_pygame(): Initializes pygame.
        add_particle(particle): Adds a particle to the simulation.
        draw(): Draws the particles and simulation boundaries on the screen.
        check_collisions(): Checks and handles collisions between particles.
        run(): Runs the simulation loop.
    """

    def __init__(self, width, height, contact_aware=False):
        self.width = width
        self.height = height
        self.particles = []
        self.contact_aware = contact_aware
        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def add_particle(self, particle):
        self.particles.append(particle)

    def random_placement(self, radius):
        """
        Generates a random position for a particle ensuring it stays within the screen bounds.
        Parameters:
            radius (int): The radius of the particle to ensure it doesn't spawn out of bounds.
        Returns:
            tuple: A tuple containing the x and y coordinates for the particle.
        """
        x = random.randint(radius, self.width - radius)
        y = random.randint(radius, self.height - radius)
        assert radius <= x <= self.width - radius
        assert radius <= y <= self.height - radius
        return x, y

    def in_board(self, particle):
        # Bounce off the edges
        if particle.x - particle.radius <= 0 or particle.x + particle.radius >= self.width:
            return False
        if particle.y - particle.radius <= 0 or particle.y + particle.radius >= self.height:
            return False
        return True

    def move_in_board(self, particle):
        if particle.x - particle.radius <= 0:
            particle.x = particle.radius
        if particle.x + particle.radius >= self.width:
            particle.x = self.width - particle.radius
        if particle.y - particle.radius <= 0:
            particle.y = particle.radius
        if particle.y + particle.radius >= self.height:
            particle.y = self.height - particle.radius
    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        pygame.draw.line(self.screen, (255, 255, 255), (self.width // 2, 0), (self.width // 2, self.height), 1)
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.height // 2), (self.width, self.height // 2), 1)

        for particle in self.particles:
            if particle.shape == 'circle':
                pygame.draw.circle(self.screen, particle.color, (int(particle.x), int(particle.y)), particle.radius)
            elif particle.shape == 'square':
                pygame.draw.rect(self.screen, particle.color,
                                 (int(particle.x - particle.radius), int(particle.y - particle.radius),
                                  particle.radius * 2, particle.radius * 2))
            else:
                raise ValueError("Invalid particle shape")

    def check_collisions(self):
        for i, particle1 in enumerate(self.particles):
            for j, particle2 in enumerate(self.particles):
                if i >= j:
                    continue  # Avoid checking the same pair twice and self-collision

                dx = particle1.x - particle2.x
                dy = particle1.y - particle2.y
                distance = math.hypot(dx, dy)
                min_distance = particle1.radius + particle2.radius

                # Collision detected and being within board
                collision_detection_applied = False
                if distance < min_distance:
                    particle1.collision_behaviour()
                    particle2.collision_behaviour()
                    collision_detection_applied = True
                if not self.in_board(particle1):
                    self.move_in_board(particle1)
                    if not collision_detection_applied:
                        particle1.collision_behaviour()
                if not self.in_board(particle2):
                    self.move_in_board(particle2)
                    if not collision_detection_applied:
                        particle2.collision_behaviour()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Move particles
            for particle in self.particles:
                particle.move()

                particle.update_color(self.width, self.height)

            if self.contact_aware:
                self.check_collisions()

            # Draw everything
            self.draw()

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Screen dimensions
    screen_width = 800
    screen_height = 600

    # Create the simulator
    simulator = Simulator(screen_width, screen_height, contact_aware=True)

    # Add multiple particles
    num_particles = 5
    particle_radius = 10
    for _ in range(num_particles):
        x, y = simulator.random_placement(particle_radius)
        radius = 10
        speed_x = 5
        speed_y = 5
        shape = 'circle' if _ % 2 == 0 else 'square'
        simulator.add_particle(LinearParticle(x, y, radius, speed_x, speed_y, shape))

    for _ in range(num_particles):
        center_x, center_y = simulator.random_placement(particle_radius)
        orbit_radius = 100 + 50 * (_ % 3)
        angle_speed = 0.02 * (_ % 4 + 1)
        radius = 10
        shape = 'circle' if _ % 2 == 0 else 'square'
        simulator.add_particle(
            CircularParticle(center_x, center_y, radius, center_x, center_y, orbit_radius, angle_speed, shape))

    # Run the simulation
    simulator.run()
