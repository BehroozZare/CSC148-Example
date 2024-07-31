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

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


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

    def __lt__(self, other):
        return self.item < other.item

    def __eq__(self, other):
        return self.item == other.item


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
        new_node = _Node(item)
        if self._first is None or new_node < self._first:
            new_node.next = self._first
            self._first = new_node
        else:
            current = self._first
            while current.next is not None and current.next < new_node:
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.size += 1

    def get(self, index: int) -> Any:
        """Return the item at position <index> in this linked list.

        Raise IndexError if index >= len(self).
        """
        if index >= self.size or index < 0:
            raise IndexError("Index out of bounds")
        current = self._first
        for _ in range(index):
            current = current.next
        return current.item

    def pop(self, index: int) -> Any:
        """Remove and return node at position <index>.

        Precondition: index >= 0.

        Raise IndexError if index >= len(self).
        """
        if index >= self.size or index < 0:
            raise IndexError("Index out of bounds")
        if index == 0:
            removed_item = self._first.item
            self._first = self._first.next
        else:
            current = self._first
            for _ in range(index - 1):
                current = current.next
            removed_item = current.next.item
            current.next = current.next.next
        self.size -= 1
        return removed_item


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

    SAVE_GIF = True
    GIF_NAME = 'animation.gif'
    MAX_NUM_PARTICLES = 100

    simulator = Simulator(SCREEN_WIDTH, SCREEN_HEIGHT, MAX_NUM_PARTICLES,
                          SAVE_GIF, GIF_NAME)
    simulator.run()
