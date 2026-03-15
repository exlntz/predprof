import os

os.environ["KERAS_BACKEND"] = "jax"

import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io.wavfile
from keras import layers
from scipy.signal import resample

keras.utils.set_random_seed(41)
