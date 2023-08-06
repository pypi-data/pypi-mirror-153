
import molecular.flags as flags

from molecular.energy import Bond, LennardJones
from molecular.geometry import distance
from molecular.misc import experimental

import numpy as np
import pygame
from scipy.optimize import minimize as _minimize
import sys


@experimental(allow=flags.use_experimental)
class Random2D:
    def __init__(self, n_particles=100, box=(800, 600), draw=True):
        # Initialize game
        self.screen = _initialize_pygame(box)

        # Generate initial coordinates
        self.xyz = np.random.rand(n_particles, 2) * np.array(box)[None, :]

    def draw(self):
        self.screen.fill((255, 255, 255))
        for xyz in self.xyz:
            pygame.draw.circle(self.screen, (0, 0, 0), (int(xyz[0]), int(xyz[1])), 10)
        pygame.display.update()
        pygame.time.wait(100)

    def minimize(self):
        def f(xyz, screen):
            xyz = xyz.reshape(-1, 2)

            energy = 0.
            for i in range(xyz.shape[0] - 1):
                for j in range(i, xyz.shape[0]):
                    lj = LennardJones(xyz[i, :], xyz[j, :], sigma=50.)
                    energy += lj.energy

            screen.fill((255, 255, 255))
            for xyz in xyz:
                pygame.draw.circle(screen, (0, 0, 0), (int(xyz[0]), int(xyz[1])), 10)
            pygame.display.update()
            pygame.time.wait(100)

            print(energy)

            return energy

        _minimize(f, x0=self.xyz, args=self.screen)

    def molecular_dynamics(self, n_steps=1000, timestep=1e-2):
        # Run through all steps
        for step in range(n_steps):
            bond = Bond(self.xyz[0, :], self.xyz[1, :], ideal_value=0., force_constant=20.)
            force = bond.force.ravel()

            lj = LennardJones(self.xyz[0, :], self.xyz[1, :], sigma=10/np.power(2, 1/6), epsilon=500.)
            force += lj.force.ravel()
            print(bond.energy, lj.energy)

            self.xyz[0, :] -= timestep * force
            self.xyz[1, :] += timestep * force

            self.screen.fill((255, 255, 255))
            pygame.draw.circle(self.screen, (0, 0, 0), (int(self.xyz[0, 0]), int(self.xyz[0, 1])), 10)
            pygame.draw.circle(self.screen, (255, 0, 0), (int(self.xyz[1, 0]), int(self.xyz[1, 1])), 10)
            pygame.display.update()
            pygame.time.wait(100)


def _initialize_pygame(box):
    pygame.init()
    screen = pygame.display.set_mode(box)
    screen.fill((255, 255, 255))
    pygame.display.update()
    return screen


simulation = Random2D()
# simulation.draw()
# simulation.minimize()
simulation.molecular_dynamics(timestep=1e-3)
