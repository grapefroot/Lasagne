"""
The `layers` module provides various classes representing the layers of a
neural network. All of them are subclasses of the `Layer` base class.

Creating a layer
----------------

A layer can be created as an instance of a `Layer` subclass. For example, a
dense layer can be created as follows:

>>> import lasagne
>>> l = lasagne.layers.DenseLayer(l_in, num_units=100) # doctest: +SKIP

This will create a dense layer with 100 units, connected to another layer
`l_in`.

Creating a network
------------------

Note that for almost all types of layers, you will have to specify one or more
other layers that the layer you are creating gets its input from. The main
exception is :class:`InputLayer`, which can be used to represent the input of
a network.

Chaining layer instances together like this will allow you to specify your
desired network structure. Note that the same layer can be used as input to
multiple other layers, allowing for arbitrary tree and directed acyclic graph
(DAG) structures.

Here is an example of an MLP with a single hidden layer:

>>> import theano.tensor as T
>>> l_in = lasagne.layers.InputLayer((100, 50))
>>> l_hidden = lasagne.layers.DenseLayer(l_in, num_units=200)
>>> l_out = lasagne.layers.DenseLayer(l_hidden, num_units=10,
...                                   nonlinearity=T.nnet.softmax)

The first layer of the network is an `InputLayer`, which represents the input.
When creating an input layer, you should specify the shape of the input data.
In this example, the input is a matrix with shape (100, 50), representing a
batch of 100 data points, where each data point is a vector of length 50.
the first dimension of a tensor is usually the batch dimension, following the
established Theano and scikit-learn conventions.

The hidden layer of the network is a dense layer with 200 units, taking its
input from the input layer. Note that we did not specify the nonlinearity of
the hidden layer. A layer with rectified linear units will be created by
default.

The output layer of the network is a dense layer with 10 units and a softmax
nonlinearity, allowing for 10-way classification of the input vectors.

Note also that we did not create any object representing the entire network.
Instead, the output layer instance `l_out` is also used to refer to the entire
network in Lasagne.

Naming layers
-------------

For convenience, you can name a layer by specifying the `name` keyword
argument:

>>> l_hidden = lasagne.layers.DenseLayer(l_in, num_units=200,
...                                      name="hidden_layer")

Initializing parameters
-----------------------

Many types of layers, such as :class:`DenseLayer`, have trainable parameters.
These are referred to by short names that match the conventions used in modern
deep learning literature. For example, a weight matrix will usually be called
`W`, and a bias vector will usually be `b`.

When creating a layer with trainable parameters, Theano shared variables will
be created for them and initialized automatically. You can optionally specify
your own initialization strategy by using keyword arguments that match the
parameter variable names. For example:

>>> l = lasagne.layers.DenseLayer(l_in, num_units=100,
...                               W=lasagne.init.Normal(0.01))

The weight matrix `W` of this dense layer will be initialized using samples
from a normal distribution with standard deviation 0.01 (see `lasagne.init`
for more information).

There are several ways to manually initialize parameters:

- Theano shared variable
    If a shared variable instance is provided, this is used unchanged as the
    parameter variable. For example:

    >>> import theano
    >>> import numpy as np
    >>> W = theano.shared(np.random.normal(0, 0.01, (50, 100)))
    >>> l = lasagne.layers.DenseLayer(l_in, num_units=100, W=W)

- numpy array
    If a numpy array is provided, a shared variable is created and initialized
    using the array. For example:

    >>> W_init = np.random.normal(0, 0.01, (50, 100))
    >>> l = lasagne.layers.DenseLayer(l_in, num_units=100, W=W_init)

- callable
    If a callable is provided (e.g. a function or a
    :class:`lasagne.init.Initializer` instance), a shared variable is created
    and the callable is called with the desired shape to generate suitable
    initial parameter values. The variable is then initialized with those
    values. For example:

    >>> l = lasagne.layers.DenseLayer(l_in, num_units=100,
    ...                               W=lasagne.init.Normal(0.01))

    Or, using a custom initialization function:

    >>> def init_W(shape):
    ...     return np.random.normal(0, 0.01, shape)
    >>> l = lasagne.layers.DenseLayer(l_in, num_units=100, W=init_W)

Some types of parameter variables can also be set to ``None`` at initialization
(e.g. biases). In that case, the parameter variable will be omitted.
For example, creating a dense layer without biases is done as follows:

>>> l = lasagne.layers.DenseLayer(l_in, num_units=100, b=None)

Parameter sharing
-----------------

Parameter sharing between multiple layers can be achieved by using the
same Theano shared variable instance for their parameters. For example:

>>> l1 = lasagne.layers.DenseLayer(l_in, num_units=100)
>>> l2 = lasagne.layers.DenseLayer(l_in, num_units=100, W=l1.W)

These two layers will now share weights (but have separate biases).

Propagating data through layers
-------------------------------

To compute the output of a single layer given its input, the `get_output_for()`
method can be used. To compute the output of a network, you should instead call
`get_output()`. This will traverse the network graph.

Any keyword arguments passed to `get_output()` are propagated to all layers.
This makes it possible to control the behaviour of the entire network. The
main use case for this is the `deterministic` keyword argument, which disables
stochastic behaviour such as dropout when set to ``True``. This is useful
because a deterministic output is desirable at evaluation time.

Creating a custom layer class
-----------------------------

To implement a custom layer class, you should subclass :class:`Layer` and
implement at least one method: `get_output_for()`. This method computes the
output of the layer given its input. Note that both the output and the input
are Theano expressions, so they are symbolic.

If the layer does not change the shape of the data (for example because it
applies an elementwise operation), then implementing this one method is
sufficient. Otherwise, you should also implement `get_output_shape_for()`,
which computes the shape of the layer output given the shape of its input.
Note that this shape computation should result in a tuple of integers, so it
is *not* symbolic.

If the layer has trainable parameters, these should be initialized in the
constructor using the `create_param()` method. When overriding the constructor,
it is also important to call the base class constructor as the first statement,
passing ``kwargs`` as well.

A layer should declare its trainable parameters by implementing a
`get_params()` method, which returns a list of Theano shared variables
representing the trainable parameters.

TODO: flesh out this section, update it once the API is frozen.
"""


from .base import *
from .helper import *
from .input import *
from .dense import *
from .noise import *
from .conv import *
from .pool import *
from .shape import *
from .merge import *
from .normalization import *
