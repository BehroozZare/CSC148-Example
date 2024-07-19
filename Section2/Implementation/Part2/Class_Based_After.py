import pygame
import sys
import math
import numpy as np
import imageio
import random


class AstronomicalBody:
    def __init__(self, id: int, x: float, y: float, radius: float, type: str):
        self.id = id  # body identifier
        self.x = x  # x position in 2D space
        self.y = y  # y position in 2D space
        self.radius = radius  # the radius of the body (assuming it's a circle)
        self.color = (255, 255, 255)  # Default white color
        self.type = type  # 'planet', star, etc

    def move(self, time_step):
        """
        Move the body in the 2D space
        """
        pass

    def get_color(self):
        """
        Get the color of the body
        """
        return self.color

    def get_type(self):
        """
        Get the type of the body
        """
        return self.type


class Planet(AstronomicalBody):
    def __init__(self, id: int, x: float, y: float, radius: float, type: str, center_x: float, center_y: float,
                 orbit_radius: float, angle_speed: float):
        super().__init__(id, x, y, radius, type)
        self.center_x = center_x
        self.center_y = center_y
        self.orbit_radius = orbit_radius
        self.angle = math.atan2(y - center_y, x - center_x) if center_x is not None and center_y is not None else 0
        self.angle_speed = angle_speed

    def move(self, time_step: float):
        if self.orbit_radius is not None:
            self.angle += self.angle_speed * time_step
            self.x = self.center_x + self.orbit_radius * math.cos(self.angle)
            self.y = self.center_y + self.orbit_radius * math.sin(self.angle)

    def get_color(self):
        colors = [
            (169, 169, 169),  # Mercury (Grey)
            (255, 140, 0),  # Venus (Orange)
            (0, 0, 255),  # Earth (Blue)
            (255, 0, 0),  # Mars (Red)
            (255, 215, 0),  # Jupiter (Golden)
            (139, 69, 19),  # Saturn (Brown)
            (0, 255, 255),  # Uranus (Cyan)
            (0, 0, 139)  # Neptune (Dark Blue)
        ]
        self.color = colors[self.id] if self.id < len(colors) else (255, 255, 255)
        return self.color


class Star(AstronomicalBody):
    def __init__(self, id: int, x: float, y: float, radius: float, type: str):
        super().__init__(id, x, y, radius, type)

    def move(self, time_step: float):
        self.x = self.x
        self.y = self.y

    def get_color(self):
        colors = [
            (255, 255, 0),  # Sun (Yellow)
        ]
        self.color = colors[self.id] if self.id < len(colors) else (255, 255, 255)
        return self.color


class Meteor(AstronomicalBody):
    def __init__(self, id: int, x: float, y: float, radius: float, type: str, speed: float, max_distance: float):
        super().__init__(id, x, y, radius, type)
        self.speed = speed
        self.max_distance = max_distance
        self.delta_x = 0
        self.delta_y = 0
        self.traveled_distance = 0
        self.color = (255,255,255)

    def move(self, time_step: float):
        x_displacement = self.speed * time_step
        y_displacement = self.speed * time_step
        self.x += x_displacement
        self.y += y_displacement
        self.delta_x += x_displacement
        self.delta_y += y_displacement
        self.traveled_distance += math.sqrt(
            self.delta_x * self.delta_x + self.delta_y * self.delta_y) * time_step

        # Check if the meteor has traveled beyond the maximum distance
        if self.traveled_distance >= self.max_distance:
            # Reset the distance traveled
            self.traveled_distance = 0
            # Randomly reposition the meteor
            self.x = random.uniform(0, screen_width)
            self.y = random.uniform(0, screen_height)


class Simulator:
    def __init__(self, width, height, time_step, astronomical_bodies, save_gif=False, gif_name='simulation.gif'):
        self.width = width
        self.height = height
        self.time_step = time_step
        self.astronomical_bodies = astronomical_bodies
        self.save_gif = save_gif
        self.gif_name = gif_name
        self.frames = []

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        for body in self.astronomical_bodies:
            if body.get_type() == 'planet':
                pygame.draw.circle(self.screen, (255, 255, 255), (body.center_x, body.center_y),
                                   body.orbit_radius, 1)

            pygame.draw.circle(self.screen, body.get_color(), (int(body.x), int(body.y)), body.radius)

    def run(self):
        self.init_pygame()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for body in self.astronomical_bodies:
                body.move(self.time_step)

            self.draw()

            if self.save_gif:
                frame = pygame.surfarray.array3d(self.screen)
                frame = np.transpose(frame, (1, 0, 2))
                self.frames.append(frame)

            pygame.display.flip()
            self.clock.tick(60)

        if self.save_gif:
            imageio.mimsave(self.gif_name, self.frames, fps=30, loop=0)

        pygame.quit()
        sys.exit()


def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list()) -> list[tuple]:
    assert solar_distances != []
    assert screen_height != 0
    assert screen_width != 0

    furthest_planet_distance = sum(solar_distances)
    screen_size = min(screen_height, screen_width) // 2

    scaling_factor = screen_size / furthest_planet_distance
    screen_distances = [distance * scaling_factor for distance in solar_distances]
    distance_to_sun_in_screen = 0
    init_pos = []
    for s_dist in screen_distances:
        distance_to_sun_in_screen += s_dist
        init_pos.append((distance_to_sun_in_screen + screen_width // 2, screen_height // 2))

        assert distance_to_sun_in_screen <= screen_size

    return init_pos


if __name__ == "__main__":
    x = 80
    screen_width = 16 * x
    screen_height = 9 * x

    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2

    astronomical_objects = []
    time_step = 0.05
    save_gif = True
    gif_name = 'animation.gif'

    solar_distances = [31, 31, 31, 31, 62, 31, 31, 31]
    init_positions = compute_init_positions(screen_height, screen_width, solar_distances)

    size_divider = 1.3

    sun = Star(0, screen_center_x, screen_center_y, 30 // size_divider, 'star')
    astronomical_objects.append(sun)

    planet_params = [
        (0, 0.02, 5),  # Mercury
        (1, 0.015, 7),  # Venus
        (2, 0.01, 8),  # Earth
        (3, 0.008, 6),  # Mars
        (4, 0.005, 12),  # Jupiter
        (5, 0.004, 10),  # Saturn
        (6, 0.003, 9),  # Uranus
        (7, 0.002, 8)  # Neptune
    ]

    speed_multiplier = 50

    for i, (planet_id, angle_speed, radius) in enumerate(planet_params):
        init_pos = init_positions[i]
        planet = Planet(
            planet_id,
            init_pos[0],
            init_pos[1],
            radius // size_divider,
            'planet',
            screen_center_x,
            screen_center_y,
            init_pos[0] - screen_center_x,
            angle_speed * speed_multiplier
        )
        astronomical_objects.append(planet)

    # Add meteors
    for id in range(0, 10):
        meteor = Meteor(id, random.uniform(0, screen_width),
                        random.uniform(0, screen_height),
                        2, 'Meteor', random.uniform(20, 60), random.uniform(500, 1000))
        astronomical_objects.append(meteor)

    simulator = Simulator(screen_width, screen_height, time_step, astronomical_objects, save_gif, gif_name)
    simulator.run()
