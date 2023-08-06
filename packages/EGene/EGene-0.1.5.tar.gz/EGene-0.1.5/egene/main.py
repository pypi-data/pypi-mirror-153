import copy
import random
import math
import egene.pygameTools as pgt
import pkg_resources
from multiprocessing import Pool

import pygame
from pygame import gfxdraw

icon = pkg_resources.resource_stream(__name__, 'images/Icon.png')

pygame.init()

pygame.display.set_caption("Network Viewer")
pygame.display.set_icon(pygame.image.load(icon))

black = (0, 0, 0)
white = (255, 255, 255)

colors = {"input": (37, 37, 125),
          "hidden": (100, 0, 0),
          "output": (0, 150, 0),
          "bias": (200, 0, 200)}


def sigmoid(x):
    """
    Uses the sigmoid function on x. High values become close to 1 while low/negative values become close to 0
    :return: The sigmoid of x, always between 0 and 1
    """
    try:
        y = 1 / (1 + math.e ** (-1 * x))
    except OverflowError:
        y = 0
    return y


def donata(x):
    """
    A function that does nothing. For nodes without an activation function
    :return: x
    """
    return x


def square(x):
    return x ** 2


class CustomError(Exception):
    pass


def duplicate_checker(x):
    """
    Checks if a list contains duplicates
    :param x: A list
    :return: True or False
    """
    uniquevalues = []

    for v in x:
        if v not in uniquevalues:
            uniquevalues.append(v)
        else:
            return True
    return False


def custom_eval(t):
    loss_function, network = t
    return loss_function(network)


class Species:
    def __init__(self, shape, initial_change_rate=1, pop_size=32, train_inputs=None, train_outputs=None, loss_function=None,
                 initial_weights=None, data_per_gen=None, use_sigmoid=True, can_change_change_rate=True,
                 use_multiprocessing=True, set_all_zero=False, add_bias_nodes=True, native_window_size=500):
        self.use_multiprocessing = use_multiprocessing
        self.use_sigmoid = use_sigmoid
        self.can_change_change_rate = can_change_change_rate
        self.set_all_zero = set_all_zero
        self.add_bias_nodes = add_bias_nodes
        self.window_size = native_window_size

        self.epochs = 0  # Count of all epochs every trained on this species
        self.all_lowest_losses = []  # All the lowest losses for each epoch

        if loss_function is None and train_inputs is None:
            raise CustomError("Species needs either a list of inputs and outputs or a loss_function")
        if loss_function is None:
            self.n_inputs = len(train_inputs[0])
            self.n_outputs = len(train_outputs[0])
            self.loss_function = self._evaluate
            self.using_custom_loss_function = False

        else:
            self.loss_function = loss_function
            self.using_custom_loss_function = True

        self.shape = shape  # This does not include the bias nodes which are added to every non-output layer

        if not self.using_custom_loss_function:
            if self.shape[0] != self.n_inputs:
                raise CustomError("First layer node count does not equal inputs number from training data which is:",
                                  self.n_inputs)
            if self.shape[-1] != self.n_outputs:
                raise CustomError("Last layer node count does not equal outputs number from training data which is:",
                                  self.n_outputs)
            if duplicate_checker(train_inputs):
                print("--Duplicate Inputs Found--")
            if data_per_gen is None:
                data_per_gen = len(train_inputs)
            self.data_per_gen = min(len(train_inputs), data_per_gen)
        else:
            self.data_per_gen = None

        self.initial_weights = initial_weights
        self.train_inputs = train_inputs
        self.train_outputs = train_outputs
        self.pop_size = pop_size
        self.change_rate = initial_change_rate

        self.networks = []

        for p in range(pop_size):  # Creating first generation of networks
            self.networks.append(Network(self.shape, self.use_sigmoid, self.add_bias_nodes, self.window_size, self.set_all_zero))
        # Giving the first network the initial weights
        if self.initial_weights is not None and self.set_all_zero is False:
            for v in range(len(self.networks[0].w)):
                self.networks[0].w[v].value = self.initial_weights[v]

    @staticmethod
    def _evaluate(p, inputs, output):  # Calculates the loss of a network based on a given input and output set
        loss = 0

        for active_input_index in range(len(inputs)):

            gen_output = p.calico(inputs[active_input_index])
            desired_output = output[active_input_index]
            for o in range(len(gen_output)):  # for handling networks with multiple outputs
                loss += abs(gen_output[o] - desired_output[o])

        loss /= len(inputs)  # division for average loss, to account for network with many outputs
        return loss

    def _score_all(self, loss_function):  # Evaluates all the networks and puts them in order from best to worst

        if self.using_custom_loss_function:  # if a custom function is being use
            if self.use_multiprocessing:
                data = []
                p = Pool()
                for a in self.networks:
                    data.append((self.loss_function, a))

                results = p.map(custom_eval, data)

                for a in range(len(self.networks)):
                    self.networks[a].loss = results[a]
            else:
                for a in range(len(self.networks)):
                    self.networks[a].loss = self.loss_function(self.networks[a])
        else:  # If a list of inputs and outputs are being used for training
            inout = []  # List of tuples with each tuple having input, output
            for i in range(len(self.train_inputs)):
                inout.append((self.train_inputs[i], self.train_outputs[i]))
            random.shuffle(inout)
            ins = []
            outs = []
            for i in range(self.data_per_gen):
                ins.append(inout[i][0])
                outs.append(inout[i][1])
            for p in self.networks:
                p.loss = loss_function(p, ins, outs)

        self.networks.sort(key=lambda x: x.loss)

    def _crossover(self, p1, p2):  # Crosses the weights of two parents to get a new child
        child = Network(self.shape, self.use_sigmoid, self.add_bias_nodes, self.window_size)
        num_weights = len(p1.w)
        cross_point = random.randint(0, num_weights - 1)
        orientation = random.choice([(p1, p2), (p2, p1)])  # Determines which parent is first

        for v in range(len(child.w)):  # Changes every weight
            if v < cross_point:
                child.w[v].value = orientation[0].w[v].value
            else:
                child.w[v].value = orientation[1].w[v].value

        return child

    def _mutate(self, network):  # Adds some random variation to some weights
        for w in network.w:
            w.value += random.random() * random.choice([-1, 0, 0, 0, 1]) * self.change_rate
        return network

    def _nextgen(self):  # Crosses over and mutates certain networks
        n = 0
        max_index = max(4, int(self.pop_size / 16))  # The worst network index that can still be a parent

        for p in range(len(self.networks) // 16, len(self.networks)):  # Only the worst 15/16 are changed

            n += 1
            while True:  # Choosing the two parents
                p1 = self.networks[random.randint(0, max_index)]
                p2 = self.networks[random.randint(0, max_index)]

                if p1 != p2:
                    break

            self.networks[p] = self._crossover(p1, p2)  # Crosses the parents to produce a child
            self.networks[p] = self._mutate(self.networks[p])  # Mutates the child based on the change rate

        for p in range(int(len(self.networks) * (15 / 16)),
                       len(self.networks)):  # Last 16th are just asexual mutants of the best 16th only one weight is changed
            p1 = self.networks[random.randint(0, max_index)]
            w_index = random.randint(0, len(self.networks[0].w) - 1)
            self.networks[p].w = copy.deepcopy(p1.w)
            self.networks[p].w[w_index].value = random.choice([-1, 1]) * random.random() * self.change_rate + p1.w[
                w_index].value

    def train(self, epochs, print_progress=True, print_population_losses=False):

        for v in range(epochs):

            self._score_all(self.loss_function)

            self.all_lowest_losses.append(self.networks[0].loss)
            if print_progress:
                print("\n", self.epochs, ":", "loss:", self.networks[0].loss, "Weights:", self.networks[0].show())
            if len(self.all_lowest_losses) > 4 and self.can_change_change_rate:  # We must be at least 4 generations in
                if self.all_lowest_losses[self.epochs - 4] == self.all_lowest_losses[self.epochs]:  # No change
                    self.change_rate /= 2
                    if print_progress:
                        print("--\nNo change from 4 gens ago so change_rate is being lowered to", self.change_rate, "\n--")

            if print_population_losses:
                all_losses = [a.loss for a in self.networks]
                print("Avg Loss:", sum(all_losses) / len(all_losses), "Losses:", all_losses)
            self.epochs += 1
            self._nextgen()

    def get_best_network(self):
        return self.networks[0]


class Network:
    def __init__(self, shape, use_sigmoid, add_bias_nodes, window_size, set_all_zero=False):
        self.loss = 0
        self.use_sigmoid = use_sigmoid
        self.set_all_zero = set_all_zero
        self.shape = shape
        self.window_size = window_size

        # Initiate nodes ------------
        self.nodes = []
        x_scale = self.window_size / len(self.shape)
        x_start = x_scale / 2
        layer_starts = []  # Keeps track of where each layer starts so weights are created faster

        # Determining the radius of the nodes when drawn, so they all fit
        self.node_draw_size = min(int((self.window_size - 50) / max(self.shape) / 2.2), int(x_scale / 5))

        # Node Creation
        for active_layer in range(len(self.shape)):  # Each layer
            layer_starts.append(len(self.nodes))
            x = int(active_layer * x_scale + x_start)

            if add_bias_nodes and active_layer != len(self.shape) - 1:  # Prevents bias on output layer
                layer_size = self.shape[active_layer] + 1  # +1 for bias
            else:
                layer_size = self.shape[active_layer]
            for n in range(layer_size):  # Each node in the layer +1 for bias:
                if not (n == self.shape[active_layer] and active_layer == len(self.shape) - 1):  # Prevents bias on output layer
                    y_scale = (self.window_size - 50) / layer_size
                    y = int(n * y_scale + (y_scale/2) + 25)
                    if active_layer == 0:
                        node_type = "input"
                    elif active_layer == len(self.shape) - 1:
                        node_type = "output"
                    else:
                        node_type = "hidden"

                    if n == self.shape[active_layer]:
                        node_type = "bias"  # Overrides other types
                    self.nodes.append(Network.Node(node_type, (x, y), active_layer, n, self.use_sigmoid, self.node_draw_size))

        layer_starts.append(len(self.nodes))
        things_checked = 0
        self.w = []
        for n in self.nodes:
            if n.layer != len(layer_starts) - 2:
                for target_index in range(layer_starts[n.layer + 1],
                                          layer_starts[n.layer + 2]):  # All nodes ahead in index are checked
                    things_checked += 1
                    t = self.nodes[target_index]

                    if t.layer == n.layer + 1:  # If the target node is one layer ahead of the current node
                        if t.node < self.shape[t.layer]:  # Stops weights from connecting to the bias node,
                            # weights can only connect from the bias node, not to bias node.

                            if self.set_all_zero is False:
                                self.w.append(Network.Edge(random.choice([-1, 1]) * random.random(), n, t))
                            else:
                                self.w.append(Network.Edge(0, n, t))
                        else:
                            pass
        self.w.sort(key=lambda x: x.pnode.layer)

    def set_weights(self, weights):
        for v in range(len(self.w)):
            self.w[v].value = weights[v]

    def _set_layer_values(self, layer, values):  # Sets the nodes of a layer to specific values. Used by calico
        for n in self.nodes:
            n.value = 0

            if n.layer == layer:  # If it is on the selected layer
                if n.node == self.shape[layer]:  # Checks if the node is the bias node
                    n.value = 1
                else:
                    n.value = values[n.node]  # Sets the input nodes to their corresponding input

    def _feedforward_calculate(self):  # Starts at input layer and calculates forward
        for active_layer in range(len(self.shape) + 1):
            for n in self.nodes:
                if n.layer == active_layer:
                    n.value = n.activation_function(n.value)
                if n.type == "bias":
                    n.value = 1
            for v in self.w:
                if v.pnode.layer == active_layer:
                    v.tnode.value += v.pnode.value * v.value

    def _collect_output_layer(self):  # Takes values of all output nodes and returns it as a list
        outputs = []
        for n in self.nodes:
            if n.layer == len(self.shape) - 1:  # If it is on the output layer
                outputs.append(n.value)
        return outputs

    def list_internal_values(self):  # Prints the value of every node and edge
        for n in self.nodes:
            print("Layer: ", n.layer, "| Node: ", n.node, "| Value: ", n.value)
        for we in self.w:
            print("PNode:", (we.pnode.layer, we.pnode.node), "| TNode:", (we.tnode.layer, we.tnode.node),
                  "| Value:", we.value)

    def calico(self, inputs, show_internals=False):  # Using an input and its weights the network returns an output

        self._set_layer_values(0, inputs)  # Sets the input layer to the input values

        self._feedforward_calculate()

        if show_internals:
            self.list_internal_values()

        return self._collect_output_layer()

    def calico_from_hidden_layer(self, layer, values, show_internals=False):  # Starts the feedforward at a different layer
        self._set_layer_values(layer, values)  # Sets the selected layer to the given values

        for active_layer in range(len(self.shape) + 1):  # Only feed forwards from the starting layer
            if active_layer >= layer:
                for n in self.nodes:
                    if n.layer == active_layer:
                        n.value = n.activation_function(n.value)
                for v in self.w:
                    if v.pnode.layer == active_layer:
                        v.tnode.value += v.pnode.value * v.value

        if show_internals:
            self.list_internal_values()
        return self._collect_output_layer()

    class Node:
        def __init__(self, node_type, location, layer, node, use_sigmoid, draw_size):
            self.type = node_type
            self.color = colors[self.type]
            self.location = location
            self.layer = layer
            self.node = node
            self.value = 0
            self.draw_size = draw_size

            if self.type == "hidden":
                if not use_sigmoid:

                    self.activation_function = donata
                    self.color = (255, 128, 0)
                else:

                    self.activation_function = sigmoid
                    self.color = (12, 122, 67)
            else:
                self.activation_function = donata

        def draw(self, display):

            gfxdraw.aacircle(display, self.location[0], self.location[1], self.draw_size + 1, white)
            gfxdraw.filled_circle(display, self.location[0], self.location[1], self.draw_size + 1, white)
            gfxdraw.aacircle(display, self.location[0], self.location[1], self.draw_size, self.color)
            gfxdraw.filled_circle(display, self.location[0], self.location[1], self.draw_size, self.color)
            if self.type == "bias":
                pygame.draw.rect(display, white,
                                 [self.location[0] - self.draw_size - 1, self.location[1] - self.draw_size - 1,
                                  self.draw_size, self.draw_size * 2 + 3])
                pygame.draw.rect(display, self.color,
                                 [self.location[0] - self.draw_size, self.location[1] - self.draw_size, self.draw_size,
                                  self.draw_size * 2 + 1])

    class Edge:  # The connection between nodes with weights
        def __init__(self, value, pnode, tnode):  # Each weight has a value and connects the pnode to the tnode
            self.value = value
            self.pnode = pnode
            self.tnode = tnode  # The tnode must be one layer ahead of the pnode

        def draw(self, width, display, node_radius):
            if width > 0:
                if self.value > 0:
                    c = (0, 100, 0)
                elif self.value < 0:
                    c = (100, 0, 0)
                else:
                    c = (255, 255, 255)
                start_loc = (self.pnode.location[0] + node_radius - width, self.pnode.location[1])
                end_loc = (self.tnode.location[0] - node_radius + width, self.tnode.location[1])
                # yf.draw_line_as_polygon(display, (self.pnode.location[0] + node_radius, self.pnode.location[1]), (self.tnode.location[0] - node_radius, self.tnode.location[1]), width, (100, 100, 100))
                pgt.draw_line_as_polygon(display, start_loc, end_loc, width, c)
            # pygame.draw.line(display, black, self.pnode.location, self.tnode.location, width + 2)
            # pygame.draw.line(display, c, self.pnode.location, self.tnode.location, width)

    def show(self):  # A list of all weights
        a = []
        for v in self.w:
            a.append(v.value)
        return a

    def draw(self, show_internals=False, independent=False):
        display = None  # If independent, this becomes a pygame window
        if independent:
            display = pygame.display.set_mode((self.window_size, self.window_size))


        surface = pygame.Surface((self.window_size, self.window_size))
        largest_weight = max([abs(v.value) for v in self.w])

        for p in self.w:
            p.draw(round((abs(p.value) / largest_weight) * self.node_draw_size * .3, 0), surface, self.node_draw_size)
        if show_internals:
            for p in self.w:  # Again so the text is not covered by any edges
                pgt.text(surface, ((p.tnode.location[0] + p.pnode.location[0] * 1.5) / 2.5,
                                   (p.tnode.location[1] + p.pnode.location[1] * 1.5) / 2.5), str(round(p.value, 2)), white, 20)
        for n in self.nodes:
            n.draw(surface)
            if show_internals:
                pgt.text(surface, n.location, str(round(n.value, 2)), white, 20)

        while independent:
            display.blit(surface, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    independent = False
                    pygame.quit()

        return surface
