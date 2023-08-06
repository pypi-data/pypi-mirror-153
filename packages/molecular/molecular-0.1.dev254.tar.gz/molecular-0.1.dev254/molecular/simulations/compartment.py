
class CompartmentalModel:
    def __init__(self, compartments, parameters):
        self._compartments = {}

    def __add__(self, other):
        self.add_compartment(other)

    def __getitem__(self, item):
        return self._compartments[item]

    def __setitem__(self, key, value):
        self._compartments[key] = value

    def add_compartment(self, compartment):
        if not isinstance(compartment, Compartment):
            raise AttributeError('must be Compartment')
        label = compartment.label
        if label in self._compartments:
            raise AttributeError('Compartment label already used')
        self._compartments[label] = compartment


class Compartment:
    def __init__(self, initial_value):
        self._initial_value = initial_value
        self._derivative = None

    def __sub__(self, other):
        pass

    @property
    def derivative(self):
        return self._derivative

    @derivative.setter
    def derivative(self, value):
        self._derivative = value

    @property
    def label(self):
        return self._label


class Parameter:
    def __init__(self, value):
        self._value = value

    @property
    def inverse(self):
        return -self._value


model = CompartmentalModel(
    compartments={
        'S': 1,
        'I': 1.27e-6,
        'R': 0,
    },
    parameters={
        'b': 0.5,
        'k': 0.33,
    }
)

# S, I, R = model.compartments
# b, k = model.parameters

S, I, R = Compartment(initial_value=1.), Compartment(initial_value=1.27e-6), Compartment(initial_value=0.)
b, k = Parameter(0.5), Parameter(0.33)

S.derivative = b.inverse * S * I
I.derivative = b * S * I - k * I
R.derivative = k * I



#
# model.add_equation('S = S - b * S * I')
# model.add_equation('I = I + b * S * I - k * I')
# model.add_equation('R = R + k * I')

model.integrate(500)

