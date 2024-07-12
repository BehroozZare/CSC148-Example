import pygame
import sys
import math
import numpy as np
import imageio


def create_planets(id, x, y, radius, shape, center_x=None, center_y=None, orbit_radius=None, angle_speed=None):
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
        'angle': math.atan2(y - center_y, x - center_x) if center_x is not None and center_y is not None else 0,
        'angle_speed': angle_speed
    }


def move_planet(planet, time_step):
    if planet['orbit_radius'] is not None:
        planet['angle'] += planet['angle_speed'] * time_step
        planet['x'] = planet['center_x'] + planet['orbit_radius'] * math.cos(planet['angle'])
        planet['y'] = planet['center_y'] + planet['orbit_radius'] * math.sin(planet['angle'])


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
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    return screen, clock


def draw(screen, planets):
    screen.fill((0, 0, 0))  # Fill the screen with black
    for planet in planets:
        if planet['orbit_radius'] > 0:  # Only draw orbits for planets with a non-zero orbit radius
            pygame.draw.circle(screen, (255, 255, 255), (planet['center_x'], planet['center_y']),
                               planet['orbit_radius'], 1)
    for planet in planets:
        if planet['shape'] == 'circle':
            pygame.draw.circle(screen, planet['color'], (int(planet['x']), int(planet['y'])), planet['radius'])
        else:
            raise ValueError("Invalid planet shape")


def run_simulation(width, height, time_step, planets, save_gif=False, gif_name='simulation.gif'):
    screen, clock = init_pygame(width, height)
    frames = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move planets
        for planet in planets:
            move_planet(planet, time_step)

        for planet in planets:
            update_color(planet)

        # Draw everything
        draw(screen, planets)

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
    astronomical_objects = []
    time_step = 0.05
    save_gif = True
    gif_name = 'animation.gif'

    # distances of planets to the sun (example values)
    solar_distances = [31, 31, 31, 31, 62, 31, 31, 31]

    # Compute the initial position of each planet
    init_positions = compute_init_positions(screen_height, screen_width, solar_distances)

    size_divider = 1.3

    # Add the Sun
    sun = create_planets(0, screen_center_x, screen_center_y, 30 // size_divider, 'circle', screen_center_x,
                          screen_center_y, 0, 0)
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

    speed_multiplier = 50

    for i, (planet_id, angle_speed, radius) in enumerate(planet_params):
        init_pos = init_positions[i]
        planet = create_planets(
            planet_id,
            init_pos[0],
            init_pos[1],
            radius // size_divider,
            'circle',
            screen_center_x,
            screen_center_y,
            init_pos[0] - screen_center_x,
            angle_speed * speed_multiplier
        )
        astronomical_objects.append(planet)

    # Run the simulation
    run_simulation(screen_width, screen_height, time_step, astronomical_objects, save_gif, gif_name)