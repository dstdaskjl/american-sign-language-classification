import sys
sys.path.append('..')

import random
import numpy as np
import traceback
import pandas as pd
import constant as const
from tensorflow.keras import models
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from pylib.path import File, Directory

# Overall CNN format
# https://www.tensorflow.org/tutorials/images/cnn

# The difference between training, validation, and test set
# https://stats.stackexchange.com/a/96869

# Save and load model
# https://www.tensorflow.org/guide/keras/save_and_serialize

# Save and load model with checkpoint
# https://keras.io/api/callbacks/model_checkpoint/

DEFAULT_EPOCH = 1000
BATCH_SIZE = 64
file = File()
directory = Directory()


class CNN:
    def test(self, *data) -> None:
        file.delete(directory.join(const.RESULT_DIR, 'result.txt'))
        x, y = data

        names = directory.list_dir(const.MODEL_DIR)
        for name in names:
            try:
                print(name)
                model = self._load_model(filepath=directory.join(const.MODEL_DIR, name))
                prediction = model.predict(x=x)
                accuracy = self._get_accuracy(prediction=prediction, y=y)
                file.write_text(
                    filepath=directory.join(const.RESULT_DIR, 'result.txt'),
                    content=name + ' ' + str(accuracy) + '\n',
                    mode='a'
                )
                print()
            except Exception:
                print(traceback.format_exc())
                print('\n\n')

    def train(self, *data) -> None:
        print('\nStarting training\n')
        x, y, hidden_activations, output_activations, optimizers, loss_functions, drop_rates = data

        for hidden_activation in hidden_activations:
            for output_activation in output_activations:
                for optimizer in optimizers:
                    for loss in loss_functions:
                        for drop_rate in drop_rates:
                            name = hidden_activation + '_' + output_activation + '_' + optimizer + '_' + loss + '_' + str(drop_rate)

                            try:
                                print(name)
                                model = self._create_model(hidden_activation, output_activation, optimizer, loss, drop_rate, x=x)
                                callback = EarlyStopping(monitor='loss', patience=3)
                                self._fit(model=model, callback=callback, name=name, x=x, y=y)
                                print()
                            except Exception:
                                file.write_text(
                                    filepath=directory.join(const.EXCEPTION_DIR, name + '.txt'),
                                    content=traceback.format_exc()
                                )

    def _create_model(self, *func, x: np.array) -> models.Sequential:
        hidden_activation, output_activation, optimizer, loss, drop_rate = func
        model = models.Sequential()

        # first layer
        model.add(Conv2D(16, (3, 3), activation=hidden_activation, input_shape=x.shape[1:]))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(drop_rate))

        # second layer
        model.add(Conv2D(32, (3, 3), activation=hidden_activation))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(drop_rate))

        # third layer
        model.add(Conv2D(64, (3, 3), activation=hidden_activation))
        model.add(Flatten())
        model.add(Dropout(drop_rate))

        # output layer
        model.add(Dense(128, activation=hidden_activation))
        model.add(Dense(26, activation=output_activation))  # 26 letters

        model.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=['accuracy']
        )
        return model

    def _fit(self, model: models.Sequential, callback: EarlyStopping, name: str, x: np.array, y: np.array) -> None:
        history = model.fit(x, y, batch_size=BATCH_SIZE, epochs=DEFAULT_EPOCH, validation_split=.2, callbacks=[callback])
        self._save_history(
            filepath=directory.join(const.HISTORY_DIR, name + '.json'),
            history_df=pd.DataFrame(history.history)
        )
        model.save(directory.join(const.MODEL_DIR, name))

    def _get_accuracy(self, prediction: np.array, y: np.array) -> float:
        count = 0
        for i in range(len(y)):
            if prediction.argmax(axis=-1)[i] == y[i]:
                count += 1
        accuracy = round(count / len(y) * 100, 3)
        return accuracy

    def _load_model(self, filepath: str) -> models.Sequential:
        return models.load_model(filepath=filepath)

    def _save_history(self, filepath: str, history_df: pd.DataFrame) -> None:
        with open(filepath, mode='w') as f:
            history_df.to_json(f)
