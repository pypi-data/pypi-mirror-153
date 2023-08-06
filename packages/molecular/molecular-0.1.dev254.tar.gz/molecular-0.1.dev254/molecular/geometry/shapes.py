
import numpy as np


class Shape:
    def __init__(self):
        pass


# TODO randomly distributed points?
# coordinates? x, y, z?
# what's the point of this?
class Sphere(Shape):
    def __init__(self, radius):
        self._radius = radius
        super().__init__()

    @property
    def area(self):
        return 4. * np.pi * np.square(self._radius)

    @property
    def radius(self):
        return self._radius

    @property
    def volume(self):
        return 4. / 3. * np.pi * np.power(self._radius, 3)