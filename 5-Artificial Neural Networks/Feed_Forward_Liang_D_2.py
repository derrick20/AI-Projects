import sys, math

LINEAR, RAMP, LOGISTIC, SIGMOID = "T1", "T2", "T3", "T4"

class NeuralNetwork:
    def __init__(self, inputs, layers):
        # Initialize the input cell values
        self.values = inputs
        self.layers = len(layers)
        #self.NN = self.make_neural_network(layers)


    def display_neural_network(self):
        for layer in self.NN.keys():
            for post in self.NN[layer].keys():
                for pre, weight in self.NN[layer][post].items():
                    print("Layer:", layer, "From:", pre, "To:", post, "Weight:", weight)


    def output(self, type, layers):
        curr_size = len(self.values)
        output = []

        for line in range(len(layers)):  # A layer is a whole line
            layer = layers[line]
            prev_size = curr_size
            curr_size = len(layer) // prev_size
            start = len(self.values) - prev_size  # Start from the beginning of the previous layer
            if line == len(layers) - 1:
                curr_size = len(layer)
                for i in range(curr_size):  # For last layer, curr_size = prev_zsize
                    output.append(self.values[start + i] * layer[i])
            else:
                for i in range(curr_size):
                    weight = sum([self.values[start + j] * layer[prev_size * i + j] for j in range(prev_size)])
                    # Take from the previous layer, go through how many cells there are, and step up by i * size
                    # to get to the current group of weights
                    value = self.transfer_function(type, weight)
                    self.values.append(value)
        '''output = []
        for layer in self.NN.keys():
            for post in self.NN[layer].keys():
                dot_product = 0
                for pre, weight in self.NN[layer][post].items():  # We build up our
                    dot_product += self.values[pre] * weight
                if layer == self.layers - 1:  # Directly apply the weights!
                    self.values[post] = dot_product
                    output.append(dot_product)
                else:
                    self.values[post] = self.transfer_function(type, dot_product)
        return output'''
        return output

    def transfer_function(self, type, x):
        if type == LINEAR:
            return x
        elif type == RAMP:
            return x if x > 0 else 0
        elif type == LOGISTIC:
            return 1 / (1 + math.exp(-x))
        elif type == SIGMOID:
            return -1 + 2 / (1 + math.exp(-x))

    def make_neural_network(self, layers):
        num_curr_cells = len(self.values)
        current_cell = 1
        neural_network = {}  # [layer][to/postsynaptic][from/presynaptic] -> weight for that connection

        for layer in range(len(layers)):
            line = layers[layer]
            num_prev_cells = num_curr_cells
            num_curr_cells = len(line) // num_prev_cells

            neural_network[layer] = {}
            if layer == len(layers) - 1:
                num_curr_cells = len(line)
                for incr in range(num_curr_cells):
                    post = current_cell + num_prev_cells + incr
                    neural_network[layer][post] = {
                        incr + current_cell: line[incr]
                    }
            else:
                # Bottom-up style; build from the first layers, using previous information to form new
                # layers of different sizes, which depend on the previous layer size
                for incr in range(num_curr_cells):
                    post = current_cell + num_prev_cells + incr  # Start from the last cell seen (previous layer).
                    # However, we are mapping to one layer further, so post is actually the prev layer count further!
                    neural_network[layer][post] = {
                        pre + current_cell: line[num_prev_cells * incr + pre] for pre in range(num_prev_cells)
                        # Within the line, move forward however many inputs go to a specific post cell,
                        # then increment through to get all of the input cells from previous layer
                    }
                current_cell += num_prev_cells
                # We have finished, and our current cell has progressed forward, and we need to keep track of this
                # reference frame shifting. We only have relative location information from the inputs

        return neural_network #'''
        #eturn 0


def main():
    args = sys.argv
    #args = ['ff.py', 'weights.txt', 'T2', 1, -0.8]

    lines = []
    file = open(args[1], "r")
    for line in file.readlines():
        lines.append([float(x) for x in line.split(" ")])
    file.close()

    inputs = [float(args[i]) for i in range(3, len(args))]

    NN = NeuralNetwork(inputs, lines)

    #NN.display_neural_network()

    type = args[2]
    print(NN.output(type, lines))



if __name__ == '__main__':
    main()