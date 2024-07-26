import pygame
import sys
import math
import numpy as np
import imageio
from pygame import Surface
from pygame.time import Clock
import python_ta
from python_ta.contracts import check_contracts

def create_planet(id: int, x: float, y: float, radius: float,
                  center_x: float = None, center_y: float = None, angle_speed: float = None) -> dict:
    """Return a planet dictionary with the given parameters
    >>> create_planet(0, 4, 4, 30, 0, 0, 5)
    {'id': 0, 'x': 4, 'y': 4, 'radius': 30, 'color': (255, 255, 255), 'shape': 'circle', 'center_x': 0, 'center_y': 0, 'orbit_radius': 5.656854249492381, 'angle': 0.7853981633974483, 'angle_speed': 5}

    Preconditions:
      - radius > 0
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
        'center_x': center_x,
        'center_y': center_y,
        'orbit_radius': orbit_radius,
        'angle': math.atan2(y - center_y, x - center_x),
        'angle_speed': angle_speed
    }


def move_planet(planet: list, time_step: float) -> None:
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


def update_color(planet: dict) -> None:
    """Update color of planets in each frame

    Preconditions:
      - planet['id'] != None
    """
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


def init_pygame(width: float, height: float)-> Surface | Clock:
    """Initialize Pygame and return the screen and clock

    Preconditions:
        - width > 0
        - height > 0
    """
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    return screen, clock


def draw(screen: Surface, objects: dict) -> None:
    """draw the scene in each frame
    
    Preconditions:
        - screen != None
    """
    screen.fill((0, 0, 0))  # Fill the screen with black
    for obj in objects:
        if 'orbit_radius' in obj and obj['orbit_radius'] > 0:  # Only draw orbits for planets
            pygame.draw.circle(screen, (255, 255, 255), (obj['center_x'], obj['center_y']),
                               obj['orbit_radius'], 1)

        pygame.draw.circle(screen, obj['color'], (int(obj['x']), int(obj['y'])), obj['radius'])


def run_simulation(width: float, height: float, time_step: float, astronomical_objects: list, save_gif: bool = False, gif_name: bool = 'simulation.gif') -> None:
    """Given the screen dimensions, time step, astronomical objects, and other parameters, run the simulation
    
    Preconditions:
        - width > 0
        - height > 0
        - time_step > 0
        - astronomical_objects != []
    """
    screen, clock = init_pygame(width, height)
    frames = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move objects
        for obj in astronomical_objects:
            move_planet(obj, time_step)

        for obj in astronomical_objects:
            update_color(obj)

        # Draw everything
        draw(screen, astronomical_objects)

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
    """Return the initial position of each planet in the screen with the given screen height and width and solar distances
    >>> compute_init_positions(558,992,[31, 31, 31, 31, 62, 31, 31, 31])
    [(527.0, 279), (558.0, 279), (589.0, 279), (620.0, 279), (682.0, 279), (713.0, 279), (744.0, 279), (775.0, 279)]

    Preconditions:
        - solar_distances != []
        - screen_height != 0
        - time_step > 0
        - screen_width != 0
    """
    # Compute the distance between the sun and the last planet
    furthest_planet_distance = sum(solar_distances)
    # Compute the screen size
    screen_size = min(screen_height, screen_width) // 2

    # Compute the scaling factor
    scaling_factor = screen_size / furthest_planet_distance
    screen_distances = []
    for distance in solar_distances:
        screen_distances.append(distance * scaling_factor)
        
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
    python_ta.check_all(config="PyTA_Config.txt")
    # Screen dimensions
    x = 80
    screen_width = 16 * x
    screen_height = 9 * x

    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2

    # Create the simulator
    astronomical_objects = []
    time_step = 0.05
    save_gif = True
    gif_name = 'buggy_animation.gif'

    # distances of planets to the sun (example values)
    solar_distances = [31, 31, 31, 31, 62, 31, 31, 31]

    # Compute the initial position of each planet
    init_positions = compute_init_positions(screen_height, screen_width, solar_distances)

    # Control the size of the astronomical objects in the simulation
    size_divider = 1.3

    # Add the Sun
    sun = create_planet(0, screen_center_x, screen_center_y, 30 / size_divider, screen_center_x,
                        screen_center_y, 0)
    astronomical_objects.append(sun)

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

    # variable to make the simulation go faster
    speed_multiplier = 50


    #Adding the planets to the astronomical_objects list
    for i, (planet_id, angle_speed, radius) in enumerate(planet_params):
        init_pos = init_positions[i]
        planet = create_planet(
            planet_id,
            init_pos[0],
            init_pos[1],
            radius // size_divider,
            screen_center_x,
            screen_center_y,
            angle_speed * speed_multiplier
        )
        astronomical_objects.append(planet)

    # Run the simulation
    run_simulation(screen_width, screen_height, time_step, astronomical_objects, save_gif, gif_name)
