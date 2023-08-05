import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.metrics import Metric


class MeanTopK(Metric):
    def __init__(self, is_weighted=False, name='mean_top_k'):
        super(MeanTopK, self).__init__()
        self.mean_top_k_sum = self.add_weight(name=name, initializer='zeros', dtype='float64')
        self.ticks = self.add_weight(name='tics', initializer='zeros', dtype='float64')
        self.is_weighted = is_weighted

    def update_state(self, y_true, y_pred, sample_weight=None, crop_edges=False):
        if crop_edges:
            y_true = y_true[:, 1:-1]
            y_pred = y_pred[:, 1:-1]

        y_top = tf.gather(y_pred, y_true, batch_dims=2)
        y_top_rep = tf.repeat(y_top[:, :, None], y_pred.shape[2], axis=-1)

        higher_than_tru = K.cast(y_pred > y_top_rep, dtype='float64')

        top_k = tf.reduce_sum(higher_than_tru, axis=-1)

        if self.is_weighted:
            top_k = top_k * K.cast(sample_weight, 'float64')
            top_k_mean = K.sum(top_k) / K.cast(K.sum(sample_weight), 'float64')
        else:
            top_k_mean = K.mean(top_k)

        self.mean_top_k_sum.assign_add(top_k_mean)
        self.ticks.assign_add(1.)

    def result(self):
        return self.mean_top_k_sum / self.ticks

    def reset(self):
        self.accuracy.assign(0.)
        self.tics.assign(0.)
