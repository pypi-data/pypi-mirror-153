import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.metrics import Metric
from tensorflow.keras.losses import SparseCategoricalCrossentropy

from ..constants import TOKENIZER

CE = SparseCategoricalCrossentropy()


class CrossEntropyMasked(Metric):
    def __init__(self, name="accuracy_masked"):
        super(CrossEntropyMasked, self).__init__()
        self.accuracy = self.add_weight(name=name, initializer="zeros")
        self.tics = self.add_weight(name=name, initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):
        x = K.cast(y_pred[:, :, 0], 'int64')
        y_pred = y_pred[:, :, 1:]
        y_true = K.cast(y_true, "int64")

        is_masked = K.equal(x, TOKENIZER.mask_token_id)

        y_true = tf.boolean_mask(y_true, is_masked)
        y_pred = tf.boolean_mask(y_pred, is_masked)

        loss = CE(y_true, y_pred)

        self.accuracy.assign_add(loss)
        self.tics.assign_add(1.)

    def result(self):
        return self.accuracy / self.tics

    def reset(self):
        self.accuracy.assign(0.)
        self.tics.assign(0.)
