import tensorflow as tf

NUM_INPUTS = 3
NUM_OUTPUTS = 1
HIDDEN1_UNITS = 50
HIDDEN2_UNITS = 50
HIDDEN3_UNITS = 50


# set up weight variable
def weight_variable(shape):
    initializer = tf.contrib.layers.xavier_initializer()
    initial = initializer(shape=shape)
    return tf.Variable(initial)


# set up bias variable
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


# define hidden layer output
def hidden_layer(inputs, weights, name):
    return tf.nn.relu(tf.matmul(inputs, weights), name=name)


class SupervisedModel(object):
    """implements the supervised learning model"""
    def __init__(self, num_inputs=NUM_INPUTS, num_outputs=NUM_OUTPUTS,
                 hidden_1=HIDDEN1_UNITS, hidden_2=HIDDEN2_UNITS, hidden_3=HIDDEN3_UNITS):
        # placeholder inputs and labels
        self.x = tf.placeholder(tf.float32, shape=[None, num_inputs], name='x')
        self.y_ = tf.placeholder(tf.float32, shape=[None, num_outputs], name='labels')

        # fully connected layer 1
        self.W_fc1 = weight_variable([num_inputs, hidden_1])
        self.h_fc1 = hidden_layer(self.x, self.W_fc1, 'fc1')

        # fully connected layer 2
        self.W_fc2 = weight_variable([hidden_1, hidden_2])
        self.h_fc2 = hidden_layer(self.h_fc1, self.W_fc2, 'fc2')

        # fully connected layer 2
        self.W_fc3 = weight_variable([hidden_2, hidden_3])
        self.h_fc3 = hidden_layer(self.h_fc2, self.W_fc3, 'fc3')

        # output layer
        self.W_fc4 = weight_variable([hidden_3, num_outputs])
        self.b_fc4 = bias_variable([num_outputs])
        self.y = tf.tanh(tf.matmul(self.h_fc1, self.W_fc4) + self.b_fc4, name='y')





















