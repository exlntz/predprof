# Требуемые пакеты:
# pip install tensorflow numpy

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks, optimizers
import json
import re

# Параметры
SAMPLE_RATE = 16000          # замените, если у вас другая частота
N_MELS = 64
FRAME_LENGTH = 1024
FRAME_STEP = 512
FFT_LENGTH = 1024
BATCH_SIZE = 32
EPOCHS = 30

# 1) Загрузка
data = np.load("Data.npz", allow_pickle=True)
X_train = data["train_x"]    # shape (1200, 80000, 1)
y_train = data["train_y"]
X_valid = data["valid_x"]
y_valid = data["valid_y"]

# Уберём последний размер канала -> (N, samples)
X_train = np.squeeze(X_train, axis=-1)
X_valid = np.squeeze(X_valid, axis=-1)
print("X_train shape:", X_train.shape, "y_train shape:", y_train.shape)
print("X_valid shape:", X_valid.shape, "y_valid shape:", y_valid.shape)


# 2) Нормализация (peak-normalize каждый пример)
def normalize_waveforms(arr):
    out = np.empty_like(arr, dtype=np.float32)
    for i, w in enumerate(arr):
        w = w.astype(np.float32)
        max_abs = np.max(np.abs(w))
        if max_abs == 0:
            out[i] = w
        else:
            out[i] = w / max_abs
    return out

X_train = normalize_waveforms(X_train)
X_valid = normalize_waveforms(X_valid)

# 3) Функция: waveform -> log-mel (используем tf.signal, возвращаем numpy)
def waveform_to_log_mel_np(waveform, sample_rate=SAMPLE_RATE,
                           n_mels=N_MELS, frame_length=FRAME_LENGTH,
                           frame_step=FRAME_STEP, fft_length=FFT_LENGTH):
    # waveform: 1D numpy float32
    w = tf.convert_to_tensor(waveform, dtype=tf.float32)
    stft = tf.signal.stft(w,
                          frame_length=frame_length,
                          frame_step=frame_step,
                          fft_length=fft_length,
                          window_fn=tf.signal.hann_window)
    magnitude = tf.abs(stft)  # [frames, fft_bins]
    num_spectrogram_bins = magnitude.shape[-1]
    linear_to_mel = tf.signal.linear_to_mel_weight_matrix(
        num_mel_bins=n_mels,
        num_spectrogram_bins=num_spectrogram_bins,
        sample_rate=sample_rate,
        lower_edge_hertz=0.0,
        upper_edge_hertz=sample_rate / 2.0)
    mel_spectrogram = tf.tensordot(magnitude, linear_to_mel, axes=1)  # [frames, n_mels]
    mel_spectrogram.set_shape([None, n_mels])
    log_mel = tf.math.log(mel_spectrogram + 1e-6)  # [frames, n_mels]
    log_mel = tf.transpose(log_mel)  # [n_mels, time_frames]
    log_mel = tf.expand_dims(log_mel, axis=-1)   # [n_mels, time_frames, 1]
    return log_mel.numpy()

# 4) Преобразуем весь датасет (можно сделать батчами, но тут N невелик)
def build_log_mel_dataset(X):
    specs = []
    for i in range(X.shape[0]):
        spec = waveform_to_log_mel_np(X[i])
        specs.append(spec)
    specs = np.stack(specs, axis=0)  # shape: (N, n_mels, time, 1)
    return specs

print("Computing log-mel for train...")
X_train_spec = build_log_mel_dataset(X_train)
print("Computing log-mel for valid...")
X_valid_spec = build_log_mel_dataset(X_valid)

print("X_train_spec shape:", X_train_spec.shape)   # (N, n_mels, time, 1)
print("X_valid_spec shape:", X_valid_spec.shape)

# 5) Метки: убедимся, что это целые числа 0..C-1
y_train = y_train.astype(np.int32)
y_valid = y_valid.astype(np.int32)
num_classes = int(np.max(y_train) + 1)
print("num_classes:", num_classes)

# 6) Модель: простой 2D-CNN
input_shape = X_train_spec.shape[1:]  # (n_mels, time, 1)
def make_model(input_shape, num_classes):
    inp = layers.Input(shape=input_shape)
    x = layers.Conv2D(32, (3,3), padding="same", activation=None)(inp)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPool2D((2,2))(x)

    x = layers.Conv2D(64, (3,3), padding="same", activation=None)(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPool2D((2,2))(x)

    x = layers.Conv2D(128, (3,3), padding="same", activation=None)(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.GlobalAveragePooling2D()(x)

    x = layers.Dropout(0.3)(x)
    out = layers.Dense(num_classes, activation="softmax")(x)
    return models.Model(inputs=inp, outputs=out)

model = make_model(input_shape, num_classes)
model.compile(optimizer=optimizers.Adam(1e-3),
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
model.summary()

# 7) Коллбэки и обучение
cb = [
    callbacks.ModelCheckpoint("best_model.h5", monitor="val_accuracy", save_best_only=True),
    callbacks.EarlyStopping(monitor="val_accuracy", patience=6, restore_best_weights=True),
    callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3)
]

history = model.fit(
    X_train_spec, y_train,
    validation_data=(X_valid_spec, y_valid),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=cb,
    shuffle=True
)

# 8) Оценка
eval_res = model.evaluate(X_valid_spec, y_valid, verbose=1)
print("Validation eval:", eval_res)

# Сохранение финальной модели
model.save("final_model_tf")