from typing import Any

import pygame
import sys
import math
import numpy as np
import imageio
import random


class Particle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    Attributes:
    - item:
        The data stored in this node.
    - next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: '_Node | None'  # Fix type annotation

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.

    Private Attributes:
    - _first: The first node in this linked list, or None if this list is empty.
    """
    _first: '_Node | None'

    def __init__(self) -> None:
        """Initialize an empty linked list.
        """
        self._first = None
        self.size = 0

    def append(self, item: Any) -> None:
        """Add the given item to link list while maintain the order."""
        pass

    def get(self, index: int) -> Any:
        """Return the item of a Node at position <index> in this linked list.
        """
        pass

    def pop(self, index: int) -> Any:
        """Remove the node and return the item at position <index>.
        """
        pass


class Simulator:
    def __init__(self, width, height, max_particles,
                 save_gif=False, gif_name='simulation.gif'):
        self.clock = None
        self.screen = None
        self.width = width
        self.height = height
        self.inserted_particles = LinkedList()
        self.save_gif = save_gif
        self.gif_name = gif_name
        self.total_particles_pos = list()
        self.max_added_particles = max_particles
        self.added_particles_cnt = 0
        self.mark_particles = list()
        self.frames = []

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def get_color(self, particle):
        x = particle.x
        y = 0
        # Color
        r = int(127 * math.sin(2 * math.pi * x / self.width) + 128)
        g = int(127 * math.sin(4 * math.pi * x / self.width) + 128)
        b = int(127 * math.sin(math.pi * x / self.width) + 128)
        return r, g, b

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        if self.added_particles_cnt < self.max_added_particles:
            # pick a random particle from total_particles_pos using index
            index = -1
            while index == -1 or self.mark_particles[index] is True:
                index = int(random.uniform(0, len(self.total_particles_pos)))
            self.mark_particles[index] = True
            # Add the particle to inserted_particles
            self.inserted_particles.append(self.total_particles_pos[index])
            # Increase the counter
            self.added_particles_cnt += 1
        else:  # remove a particle from the inserted_particles
            # if the list is not empty then remove one particle
            if self.inserted_particles.size > 0:
                self.inserted_particles.pop(0)
            else:
                # Reset the process
                self.added_particles_cnt = 0
                self.mark_particles = [False] * len(self.total_particles_pos)

        for idx in range(self.inserted_particles.size):
            particle = self.inserted_particles.get(idx)
            pygame.draw.circle(self.screen, self.get_color(particle),
                               (int(particle.x), int(particle.y)),
                               particle.radius)

    def run(self):
        self.init_pygame()
        self.compute_total_particles_position()
        #an array of false values
        self.mark_particles = [False] * len(self.total_particles_pos)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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

    def compute_total_particles_position(self) -> None:
        for h in range(10, self.height, 10):
            for w in range(10, self.width, 10):
                particle = Particle(w, h, 5)
                self.total_particles_pos.append(particle)


if __name__ == "__main__":
    SCREEN_SCALER = 80
    SCREEN_WIDTH = 16 * SCREEN_SCALER
    SCREEN_HEIGHT = 9 * SCREEN_SCALER

    TIME_STEP = 0.05
    SAVE_GIF = True
    GIF_NAME = 'animation.gif'
    MAX_NUM_PARTICLES = 200

    simulator = Simulator(SCREEN_WIDTH, SCREEN_HEIGHT, MAX_NUM_PARTICLES,
                          SAVE_GIF, GIF_NAME)
    simulator.run()
