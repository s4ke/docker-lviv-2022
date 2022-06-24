from datetime import datetime
from os import path
from ai.model import *

# seed the random generator, for reproducible results
from numpy import random
random.seed(1337)

import numpy
from PIL import Image
from sklearn import datasets


# directory of this file
module_dir = path.dirname(path.realpath(__file__))

# load prepared data set containing 1797 digits as 8x8 images
digit_features, digit_classes = datasets.load_digits(n_class=NUM_DIGITS, return_X_y=True)
num_samples = digit_classes.shape[0]

# normalize features, see documentation of sklearn.datasets.load_digits!
# neural networks work best with normalized data
digit_features /= MAX_FEATURE

# we need so called "one-hot" vectors
# one-hots are vectors, where all entries are 0 except the target class, which is 1
digit_labels = numpy.zeros(shape=(num_samples, NUM_DIGITS))
for index, digit_class in enumerate(digit_classes):
    digit_labels[index][digit_class] = 1.

# get a neural net, that can fit our problem
model = get_model()

# prints a human readable summary of the model to the out-stream
model.summary()

# training the model
model.fit(digit_features, digit_labels, batch_size=32, epochs=30, validation_split=.2, callbacks=[])

# finally save the model's weights
# for compatibility reasons we don't save the entire model
# instead save only the weights, on load build the same model and load them
model.save_weights(path.join(module_dir, 'weights', 'trained'))
