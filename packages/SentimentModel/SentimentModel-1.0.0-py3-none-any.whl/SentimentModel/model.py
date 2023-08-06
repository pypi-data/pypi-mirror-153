import os

from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint,
                                        ReduceLROnPlateau)
from tensorflow.keras.layers import (LSTM, Bidirectional, Conv1D, Dense,
                                     Embedding, GlobalMaxPool1D)
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier

from SentimentModel.Config.core import config

os.environ['PYTHONHASHSEED']=str(config.app.SEED)
 
# 2. Set `python` built-in pseudo-random generator at a fixed value
import random

random.seed(config.app.SEED)
 
# 3. Set `numpy` pseudo-random generator at a fixed value
import numpy as np

np.random.seed(config.app.SEED)
 
# 4. Set `tensorflow` pseudo-random generator at a fixed value
import tensorflow as tf

tf.random.set_seed(config.app.SEED)


def make_model():
    embedding_layer = Embedding(input_dim=config.model.VOCAB_LEN,
                                output_dim=config.model.EMBEDDING_DIMENSIONS,
                                # weights=[],
                                input_length=config.model.INPUT_LEN,
                                trainable=True)

    model = Sequential([
        embedding_layer,
        Bidirectional(LSTM(100, dropout=0.3, return_sequences=True)),
        Bidirectional(LSTM(100, dropout=0.3, return_sequences=True)),
        Conv1D(100, 5, activation='relu'),
        GlobalMaxPool1D(),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid'),
    ],
        name="SentimentModel")

    model.compile(loss='binary_crossentropy',
                  optimizer='adam', metrics=['accuracy'])

    return model


callbacks = [ReduceLROnPlateau(monitor='val_loss', patience=5, cooldown=0),
             EarlyStopping(monitor='val_accuracy', min_delta=1e-4, patience=5),
             ModelCheckpoint(filepath=config.app.MODELS_PATH + config.app.MODEL_NAME, monitor='val_accuracy', verbose=0, save_best_only=True)]


lstm_clf = KerasClassifier(build_fn=make_model,
                           batch_size=config.model.BATCH_SIZE,
                           validation_split=0.1,
                           epochs=config.model.EPOCHS,
                           verbose=1,  # progress bar - required for CI job
                           callbacks=callbacks,
                        #    embedding_matrix=None
                           )

if __name__ == '__main__':
    model = make_model()
    model.summary()
