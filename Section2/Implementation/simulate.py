import pygame
import sys
import math
import numpy as np
import imageio


class Particle:
    """
    A base class for particles.

    Attributes:
        id (int): The ID of the particle.
        x (float): The x-coordinate of the particle.
        y (float): The y-coordinate of the particle.
        radius (int): The radius of the particle.
        color (tuple): The color of the particle.
        shape (str): The shape of the particle ('circle' or 'square').

    Methods:
        move(time_step): Moves the particle (to be implemented in subclasses).
        getColor(): Updates the color of the particle.
        collision_behaviour(): Handles collision behavior (to be implemented in subclasses).
        speed(): Returns the speed of the particle.
    """

    def __init__(self, id, x, y, radius, shape):
        self.id = id
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 255, 255)  # Default white color
        self.shape = shape  # 'circle' or 'square'

    def move(self, time_step):
        pass

    def getColor(self):
        pass

    def collision_behaviour(self):
        pass

    def speed(self):
        return 0


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
        move(time_step): Moves the particle along its circular orbit.
        getColor(): Updates the color of the particle based on its ID.
    """

    def __init__(self, id, x, y, radius, center_x, center_y, orbit_radius, angle_speed, shape='circle'):
        super().__init__(id, x, y, radius, shape)
        self.center_x = center_x
        self.center_y = center_y
        self.orbit_radius = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        self.angle = math.atan2(y - center_y, x - center_x)
        self.angle_speed = angle_speed

    def move(self, time_step):
        self.angle += self.angle_speed * time_step
        self.x = self.center_x + self.orbit_radius * math.cos(self.angle)
        self.y = self.center_y + self.orbit_radius * math.sin(self.angle)

    def getColor(self):
        # Define colors for the Sun and planets
        if self.id == 0:
            self.color = (255, 255, 0)  # Sun (Yellow)
        elif self.id == 1:
            self.color = (169, 169, 169)  # Mercury (Grey)
        elif self.id == 2:
            self.color = (255, 140, 0)  # Venus (Orange)
        elif self.id == 3:
            self.color = (0, 0, 255)  # Earth (Blue)
        elif self.id == 4:
            self.color = (255, 0, 0)  # Mars (Red)
        elif self.id == 5:
            self.color = (255, 215, 0)  # Jupiter (Golden)
        elif self.id == 6:
            self.color = (139, 69, 19)  # Saturn (Brown)
        elif self.id == 7:
            self.color = (0, 255, 255)  # Uranus (Cyan)
        elif self.id == 8:
            self.color = (0, 0, 139)  # Neptune (Dark Blue)
        else:
            self.color = (255, 255, 255)  # Default white color

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
        time_step (float): The time step for the simulation.
        screen (pygame.Surface): The pygame screen object.
        clock (pygame.time.Clock): The pygame clock object.

    Methods:
        init_pygame(): Initializes pygame.
        add_particle(particle): Adds a particle to the simulation.
        draw(): Draws the particles and simulation boundaries on the screen.
        run(): Runs the simulation loop.
    """

    def __init__(self, width, height, time_step, save_gif=False, gif_name='simulation.gif'):
        self.width = width
        self.height = height
        self.particles = []
        self.time_step = time_step
        self.save_gif = save_gif
        self.gif_filename = gif_name
        self.frames = []
        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def add_particle(self, particle):
        self.particles.append(particle)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        for particle in self.particles:
            if particle.orbit_radius > 0:  # Only draw orbits for particles with a non-zero orbit radius
                pygame.draw.circle(self.screen, (255, 255, 255), (particle.center_x, particle.center_y),
                                   particle.orbit_radius, 1)

        for particle in self.particles:
            if particle.shape == 'circle':
                pygame.draw.circle(self.screen, particle.color, (int(particle.x), int(particle.y)), particle.radius)
            else:
                raise ValueError("Invalid particle shape")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Move particles
            for particle in self.particles:
                particle.move(self.time_step)

            for particle in self.particles:
                particle.getColor()

            # Draw everything
            self.draw()

            # Capture frame for GIF
            if self.save_gif:
                frame = pygame.surfarray.array3d(self.screen)
                frame = np.transpose(frame, (1, 0, 2))
                self.frames.append(frame)

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

        # Save the GIF
        if self.save_gif:
            imageio.mimsave(self.gif_filename, self.frames, fps=30, loop=0)

        pygame.quit()
        sys.exit()


def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list()) -> list[tuple]:
    """Return the initial position of each planet
    >>> compute_init_positions(558,992,[31, 31, 31, 31, 62, 31, 31, 31])
    [(62.0, 0), (124.0, 0), (186.0, 0), (248.0, 0), (372.0, 0), (434.0, 0), (496.0, 0), (558.0, 0)]
    """

    # Check the precondition
    assert solar_distances != []
    assert screen_height != 0
    assert screen_width != 0

    # Compute the distance between the sun and the last planet
    furthest_planet_distance = sum(solar_distances)
    print("The solar distances are", solar_distances, "- the furthest planet is at", furthest_planet_distance)
    # Compute the screen size
    screen_size = min(screen_height, screen_width) // 2
    print("screen height", screen_height, "- screen width", screen_width,
          "- screen size", screen_size)

    # Compute the scaling factor
    scaling_factor = screen_size / furthest_planet_distance
    screen_distances = [distance * scaling_factor for distance in solar_distances]
    print("Scaler factor:", scaling_factor, "- screen distances", screen_distances)
    # Compute the distance between each planet and sun (the center)
    distance_to_sun_in_screen = 0
    init_pos = []
    for s_dist in screen_distances:
        distance_to_sun_in_screen += s_dist
        init_pos.append((distance_to_sun_in_screen, 0))
        # init_pos.append((distance_to_sun_in_screen + screen_width // 2, screen_height // 2))
        assert distance_to_sun_in_screen <= screen_size

    print("initial positions", init_pos)
    return init_pos


# Example usage
if __name__ == "__main__":
    # Screen dimensions
    x = 80
    screen_width = 16 * x
    screen_height = 9 * x

    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2

    # Create the simulator
    simulator = Simulator(screen_width, screen_height, 0.05, save_gif=True, gif_name='buggy_animation.gif')

    # distances of planets to the sun (example values)
    solar_distances = [31, 31, 31, 31, 62, 31, 31, 31]

    # Compute the initial position of each planet
    init_positions = compute_init_positions(screen_height, screen_width, solar_distances)

    size_divider = 1.3

    # Add the Sun
    sun = CircularParticle(0, screen_width // 2, screen_height // 2, 30 // size_divider, screen_width // 2,
                           screen_height // 2, 0, 0, 'circle')
    simulator.add_particle(sun)

    # Add planets with their computed orbits
    planet_params = [
        (1, 0.02, 5),  # Mercury
        (2, 0.015, 7),  # Venus
        (3, 0.01, 8),  # Earth
        (4, 0.008, 6),  # Mars
        (5, 0.005, 12),  # Jupiter
        (6, 0.004, 10),  # Saturn
        (7, 0.003, 9),  # Uranus
        (8, 0.002, 8)  # Neptune
    ]

    speed_multiplier = 50

    for i, (planet_id, angle_speed, radius) in enumerate(planet_params):
        init_pos = init_positions[i]
        planet = CircularParticle(
            planet_id,
            init_pos[0],
            init_pos[1],
            radius // size_divider,
            screen_center_x,
            screen_center_y,
            init_pos[0] - screen_center_x,
            angle_speed * speed_multiplier,
            'circle'
        )
        simulator.add_particle(planet)

    # Run the simulation
    simulator.run()
