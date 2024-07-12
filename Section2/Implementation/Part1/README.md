![Solar System Simulation](../Figures/PlanetWithMeteor.gif)

# Expanding Solar System - Part 1!

## Objective

For this section, we want to understand the structure of the given simulator code and then integrate the meteor into the code. Note that we do not need to understand every details about the code that is given to us to work with. We first need to build a mental image of how the developers of the code thought about the process. When we have some abstract view, we can then think about ways to actually change the underlying code and expand it effectively. For the following read, I suggest to have the code [Simulator File](Function_Based_Before.py) also opened for easier read.

The way that I approach any unfamilier code base, is to find the starting point! Looking at the ```if __name__ == "__main__":``` part of the [Simulator File](Function_Based_Before.py), we can quickly see where the procedure is going to start. Let's analyze this procedure together and think about how the developers of this code think about their simulator.

```python
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
```

Here using the comments, we can quickly see that the structure of this part is first some variables relted to screen. There are also for variables related to the simulator. We then see solar_distances that we are familier with followed by the function that we have developed. I currently don't know what is this size_divider, so we will leave it as that for now. We then see that a create_planets function exists that create a variable sun and this sun is stored in ```astronomical_objects``` list. Let's quickly see what is this create_planets function. If it is small, we can have clearer view.


```python
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
```

Looking at the create_planets function, it returns a dictionary. The structure of the dictionary is also clear. So we know now that this simulator use a dictionary to store the information about each planet. Following back the computational pipeline, we will reach to this block of code.


```python
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
```

There is a ```planet_params``` which is used in the for loop. We also have ```speedup_multiplier``` which is used in the for loop to create the planets dictionary. So basically this for loop creates other planets and everything is feed to ```run_simulation``` function. We don't necessary have to understand ```speed_multiplier``` or ```planet_params``` as we only care about computational flow. Let's see how ```run_simulation``` function works. 


```python
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
```

Let's remind ourselves of what we are searching for. We want to understand the structure of the simulator code enough so that we can integrate our meteors into it. So far, we realize that the meteors should be represented as dictionaries, similar to how planets are. Now, in this `run_simulation`, we should follow the lines that relate to the planets input. Let's continue analyzing the code.

In this function, there is `init_pygame`, whose purpose I don't yet understand. Then, there is a `while running` loop which is always True, so it is probably something that allows us to run the simulation indefinitely. There is an if statement that checks events and has `running=False`. I don't know what it is doing, but if the `if` statement is true, then the `while` loop stops. Then we have `move_planets`, `update_colors`, and `draw_function`, which directly interact with the planets dictionary. Finally, there are some options such as `save_gif` that, since they are not interacting with the `move_planet`, are not important (at least for now, based on our first pass on the code).