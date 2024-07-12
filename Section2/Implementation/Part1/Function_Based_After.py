import pygame
import sys
import math
import numpy as np
import imageio
import random


def create_planet(id: int, x: float, y: float, radius: float, shape: str,
                  center_x: float = None, center_y: float = None, angle_speed: float = None) -> dict:
    """Return a planet dictionary with the given parameters
    >>> create_planet(0, 4, 4, 30, 'circle', 0, 0, 5)
    {'id': 0, 'x': 4, 'y': 4, 'radius': 30, 'color': (255, 255, 255), 'shape': 'circle', 'center_x': 0, 'center_y': 0, 'orbit_radius': 5.656854249492381, 'angle': 0.7853981633974483, 'angle_speed': 5}

    Preconditions:
      - radius > 0
      - shape == 'circle'
      - center_x != None
      - center_y != None
      - angle_speed != None
    """
    orbit_radius = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    return {
        'id': id,
        'x': x,
        'y': y,
        'radius': radius,
        'color': (255, 255, 255),  # Default white color
        'shape': shape,  # 'circle' or 'square'
        'center_x': center_x,
        'center_y': center_y,
        'orbit_radius': orbit_radius,
        'angle': math.atan2(y - center_y, x - center_x),
        'angle_speed': angle_speed
    }


def create_meteor(id: int, x: float, y: float, radius: float, shape: str, speed: float) -> dict:
    """Return a meteor dictionary with the given parameters
    >>> create_meteor(1, 100, 100, 3, 'circle', 2)
    {'id': 1, 'x': 100, 'y': 100, 'radius': 3, 'color': (255, 255, 255), 'shape': 'circle', 'speed': 2, 'distance_traveled': 0}

    Preconditions:
      - radius > 0
      - speed > 0
      - shape == 'circle'
    """
    return {
        'id': id,
        'x': x,
        'y': y,
        'delta_x': 0,
        'delta_y': 0,
        'radius': radius,
        'color': (255, 255, 255),  # Default white color
        'shape': shape,  # 'circle' or 'square'
        'speed': speed,
        'distance_traveled': 0
    }


def move_planet(planet, time_step):
    """Move a planet in its orbit

    Preconditions:
      - planet['orbit_radius'] != None
      - planet['angle'] != None
      - planet['angle_speed'] != None
      - planet['x'] != None
      - planet['y'] != None
      - planet['center_x'] != None
      - planet['center_y'] != None
      - time_step > 0
    """
    planet['angle'] += planet['angle_speed'] * time_step
    planet['x'] = planet['center_x'] + planet['orbit_radius'] * math.cos(planet['angle'])
    planet['y'] = planet['center_y'] + planet['orbit_radius'] * math.sin(planet['angle'])


def move_meteor(meteor, time_step, screen_width, screen_height, max_distance=500):
    """Move a meteor in a straight line and handle fading/reappearing

    Preconditions:
      - meteor['x'] != None
      - meteor['y'] != None
      - meteor['speed'] > 0
      - time_step > 0
      - max_distance > 0
    """
    meteor['x'] += meteor['speed'] * time_step
    meteor['y'] += meteor['speed'] * time_step
    meteor['delta_x'] += meteor['speed'] * time_step
    meteor['delta_y'] += meteor['speed'] * time_step
    meteor['distance_traveled'] += math.sqrt(meteor['delta_x'] * meteor['delta_x'] + meteor['delta_y'] * meteor['delta_y']) * time_step

    # Check if the meteor has traveled beyond the maximum distance
    if meteor['distance_traveled'] >= max_distance:
        # Reset the distance traveled
        meteor['distance_traveled'] = 0
        # Randomly reposition the meteor
        meteor['x'] = random.uniform(0, screen_width)
        meteor['y'] = random.uniform(0, screen_height)


def update_color(planet):
    colors = [
        (255, 255, 0),  # Sun (Yellow)
        (169, 169, 169),  # Mercury (Grey)
        (255, 140, 0),  # Venus (Orange)
        (0, 0, 255),  # Earth (Blue)
        (255, 0, 0),  # Mars (Red)
        (255, 215, 0),  # Jupiter (Golden)
        (139, 69, 19),  # Saturn (Brown)
        (0, 255, 255),  # Uranus (Cyan)
        (0, 0, 139)  # Neptune (Dark Blue)
    ]
    planet['color'] = colors[planet['id']] if planet['id'] < len(colors) else (255, 255, 255)


def init_pygame(width, height):
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    return screen, clock


def draw(screen, objects):
    screen.fill((0, 0, 0))  # Fill the screen with black
    for obj in objects:
        if 'orbit_radius' in obj and obj['orbit_radius'] > 0:  # Only draw orbits for planets
            pygame.draw.circle(screen, (255, 255, 255), (obj['center_x'], obj['center_y']),
                               obj['orbit_radius'], 1)
    for obj in objects:
        if obj['shape'] == 'circle':
            pygame.draw.circle(screen, obj['color'], (int(obj['x']), int(obj['y'])), obj['radius'])
        else:
            raise ValueError("Invalid object shape")


def run_simulation(width, height, time_step, objects, save_gif=False, gif_name='simulation.gif'):
    screen, clock = init_pygame(width, height)
    frames = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move objects
        for obj in objects:
            if 'orbit_radius' in obj:
                move_planet(obj, time_step)
            elif 'speed' in obj:
                move_meteor(obj, time_step, width, height, random.uniform(500, 1000))

        for obj in objects:
            update_color(obj)

        # Draw everything
        draw(screen, objects)

        # Capture frame for GIF
        if save_gif:
            frame = pygame.surfarray.array3d(screen)
            frame = np.transpose(frame, (1, 0, 2))
            frames.append(frame)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    # Save the GIF
    if save_gif:
        imageio.mimsave(gif_name, frames, fps=30, loop=0)

    sys.exit()


def compute_init_positions(screen_height: int, screen_width: int, solar_distances: list) -> list[tuple]:
    """Return the initial position of each planet
    >>> compute_init_positions(558,992,[31, 31, 31, 31, 62, 31, 31, 31])
    [(527.0, 279), (558.0, 279), (589.0, 279), (620.0, 279), (682.0, 279), (713.0, 279), (744.0, 279), (775.0, 279)]
    """

    # Check the precondition
    assert solar_distances != []
    assert screen_height != 0
    assert screen_width != 0

    # Compute the distance between the sun and the last planet
    furthest_planet_distance = sum(solar_distances)
    # Compute the screen size
    screen_size = min(screen_height, screen_width) // 2

    # Compute the scaling factor
    scaling_factor = screen_size / furthest_planet_distance
    screen_distances = [distance * scaling_factor for distance in solar_distances]
    # Compute the distance between each planet and sun (the center)
    distance_to_sun_in_screen = 0
    init_pos = []
    for s_dist in screen_distances:
        distance_to_sun_in_screen += s_dist
        init_pos.append((distance_to_sun_in_screen + screen_width // 2, screen_height // 2))

        assert distance_to_sun_in_screen <= screen_size

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
    objects = []
    time_step = 0.05
    save_gif = True
    gif_name = 'buggy_animation.gif'

    # distances of planets to the sun (example values)
    solar_distances = [31, 31, 31, 31, 62, 31, 31, 31]

    # Compute the initial position of each planet
    init_positions = compute_init_positions(screen_height, screen_width, solar_distances)

    size_divider = 1.3

    # Add the Sun
    sun = create_planet(0, screen_center_x, screen_center_y, 30 / size_divider, 'circle', screen_center_x,
                        screen_center_y, 0)
    objects.append(sun)

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
        planet = create_planet(
            planet_id,
            init_pos[0],
            init_pos[1],
            radius // size_divider,
            'circle',
            screen_center_x,
            screen_center_y,
            angle_speed * speed_multiplier
        )
        objects.append(planet)

    # Add meteors
    meteors = []
    for i in range(10,20):
        meteor = create_meteor(i, random.uniform(0, screen_width),
                               random.uniform(0, screen_height),
                               2, 'circle', random.uniform(20, 60))
        meteors.append(meteor)

    for meteor in meteors:
        objects.append(meteor)

    # Run the simulation
    run_simulation(screen_width, screen_height, time_step, objects, save_gif, gif_name)
