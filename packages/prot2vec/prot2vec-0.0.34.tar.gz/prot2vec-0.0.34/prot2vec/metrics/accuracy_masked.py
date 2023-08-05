import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.metrics import Metric

from ..constants import TOKENIZER


class AccuracyMasked(Metric):
    def __init__(self, name="accuracy_masked"):
        super(AccuracyMasked, self).__init__()
        self.accuracy = self.add_weight(name=name, initializer="zeros")
        self.tics = self.add_weight(name='tics', initializer="zeros")

    def update_state(self, y_true, y_pred, sample_weight=None):
        x = K.cast(y_pred[:, :, 0], 'int64')
        y_pred = y_pred[:, :, 1:]

        y_true = K.cast(y_true, "int64")
        y_pred = K.argmax(y_pred, axis=-1)
        eq_out = K.equal(y_true[:, 1:-1], y_pred[:, 1:-1])
        eq_masked = K.equal(x[:, 1:-1], TOKENIZER.mask_token_id)

        logic_and = tf.logical_and(eq_out, eq_masked)
        acc_of_masked = K.sum(K.cast(logic_and, "int32")) / K.sum(K.cast(eq_masked, "int32"))
        acc_of_masked = K.cast(acc_of_masked, "float32")
        self.accuracy.assign_add(acc_of_masked)
        self.tics.assign_add(1.)

    def result(self):
        return self.accuracy / self.tics

    def reset(self):
        self.accuracy.assign(0.)
        self.tics.assign(0.)
