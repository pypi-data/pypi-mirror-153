"""
Neural network optimizers
"""
import numpy as np
from abc import ABC, abstractmethod
from redmind.layers import Layer
from redmind.network import NeuralNetwork

def init_velocity_vector(layers):
    velocity = {}
    # build layers velocity dict with np zeros array for each trainable pram
    for idx, layer in enumerate(layers):
        trainable_params = layer.get_trainable_params()
        velocity[idx] = trainable_params
        for param, grads in trainable_params.items():
            velocity[idx][param] = np.zeros(grads.shape)
    return velocity

class Optimizer(ABC):
    """
    Only one optimizer can be assigned to the entire NN

    The optimizer is in charge of keeping track of optimization
    variable states for all layers. Check Adam optimizer for reference.

    Optimizer workflow
    1. Loop through self.layers (coming from Neural Network)
    2. Fetch all trainable parameters
    3. Optimize those parameters according to strategy
    4. (optional) track optimization
    5. Update layer parameters on learning rate scale
    """
    def __init__(self, network: NeuralNetwork):
        assert isinstance(network, NeuralNetwork), "network should be a NeuralNetwork object"
        self.layers = network.layers
    
    def set_learning_rate(self, learning_rate: float) -> None:
        self.learning_rate = learning_rate

    @abstractmethod
    def __call__(self) -> None:
        """Runs optimizer for all trainable parameters returned by the layer"""
        
class GradientDescent(Optimizer):
    def __call__(self) -> None:
        for layer in self.layers:
            trainable_params = layer.get_trainable_params()
            for param, grads in trainable_params.items():
                trainable_params[param] = grads * self.learning_rate
            layer.update_trainable_params(trainable_params)

class Momentum(Optimizer):
    beta = 0.9

    def __init__(self, network: NeuralNetwork):
        super().__init__(network)
        self.gradients_velocity = init_velocity_vector(self.layers)


    def __call__(self) -> None:
        for idx, layer in enumerate(self.layers):
            trainable_params = layer.get_trainable_params()
            for param, grads in trainable_params.items():
                self.gradients_velocity[idx][param] = self.beta * self.gradients_velocity[idx][param] + (1 - self.beta) * grads
                trainable_params[param] = self.gradients_velocity[idx][param] * self.learning_rate
            layer.update_trainable_params(trainable_params)

class RMSprop(Optimizer):
    beta = 0.9
    epsilon = 1e-7

    def __init__(self, network: NeuralNetwork):
        super().__init__(network)
        self.gradients_velocity = init_velocity_vector(self.layers)

    def __call__(self) -> None:
        for idx, layer in enumerate(self.layers):
            trainable_params = layer.get_trainable_params()
            for param, grads in trainable_params.items():
                self.gradients_velocity[idx][param] = self.beta * self.gradients_velocity[idx][param] + (1 - self.beta) * np.power(grads, 2)
                trainable_params[param] = (grads / np.sqrt(self.gradients_velocity[idx][param] + self.epsilon)) * self.learning_rate
            layer.update_trainable_params(trainable_params)

class Adam(Optimizer):
    """Adam is a combination of momentum and RMSprop, thats why the velocity names"""
    beta1 = 0.9
    beta2 = 0.999
    epsilon = 1e-7

    def __init__(self, network: NeuralNetwork):
        super().__init__(network)
        self.momentum_velocity = init_velocity_vector(self.layers)
        self.rmsprop_velocity = init_velocity_vector(self.layers)

    def __call__(self) -> None:
        for idx, layer in enumerate(self.layers):
            trainable_params = layer.get_trainable_params()
            for param, grads in trainable_params.items():
                self.momentum_velocity[idx][param] = ((self.beta1 * self.momentum_velocity[idx][param]) + ((1 - self.beta1) * grads)) 
                self.rmsprop_velocity[idx][param] = ((self.beta2 * self.rmsprop_velocity[idx][param]) + ((1 - self.beta2) * np.power(grads, 2)))
                trainable_params[param] = (self.momentum_velocity[idx][param] / np.sqrt(self.rmsprop_velocity[idx][param] + self.epsilon)) * self.learning_rate
            layer.update_trainable_params(trainable_params)

