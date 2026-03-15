import os

os.environ["KERAS_BACKEND"] = "jax"

import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.io.wavfile
from keras import layers
from scipy.signal import resample
SAMPLE_RATE=1
keras.utils.set_random_seed(41)
print('loading')
data = np.load("Data.npz")
#valid_x  - WAV файлы
#valid_y  - номера цивилизаций
#train_x  - WAV файлы
#train_y  - поврежденые номера
train_x = data["train_x"]
train_y = data["train_y"]

valid_x = data["valid_x"]
valid_y = data["valid_y"]

def read_wav_file(path, target_sr=SAMPLE_RATE):
    sr, wav = scipy.io.wavfile.read(os.path.join(BASE_DATA_DIR, "audio", path))
    wav = wav.astype(np.float32) / 32768.0  # normalize to [-1, 1]
    num_samples = int(len(wav) * target_sr / sr)  # resample to 16 kHz
    wav = resample(wav, num_samples)
    return wav[:, None]  # Add a channel dimension (of size 1)


