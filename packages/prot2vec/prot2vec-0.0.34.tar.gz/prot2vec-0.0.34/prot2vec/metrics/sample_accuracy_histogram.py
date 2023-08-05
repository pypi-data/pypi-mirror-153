import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.metrics import Metric


def update_metric(x_prev, x_now, i):
    return (1 / (i + 1)) * (i * x_prev + x_now)


class SampleAccHist(Metric):
    def __init__(self, name='sample_accuracy_histogram'):
        super(SampleAccHist, self).__init__()
        self.metric_name = name
        self.metric = []
        self.tics = self.add_weight('tics', initializer="zeros")

    def update_state(self, y_true, y_pred, x=None, sample_weight=None):
        y_pred = tf.argmax(y_pred, axis=-1, output_type=tf.int32)
        equals = tf.cast(y_pred == y_true, tf.int32)

        linspac = tf.range(y_pred.shape[1] + 1)

        eq_sum = K.sum(equals, axis=1)

        eq_sum = tf.repeat(eq_sum[:, None], linspac.shape[0], axis=1)
        linspac = tf.repeat(linspac[None, :], eq_sum.shape[0], axis=0)

        hits_count_histogram = K.cast(eq_sum == linspac, 'float32')
        hits_count_histogram = K.sum(hits_count_histogram, axis=0)
        hits_count_histogram = hits_count_histogram / K.sum(hits_count_histogram)

        for i in range(hits_count_histogram.shape[0]):
            if i >= len(self.metric):
                self.metric.append(self.add_weight(name=self.metric_name + str(i), initializer="zeros"))
            self.metric[i].assign(update_metric(self.metric[i], hits_count_histogram[i], self.tics))

        self.tics.assign_add(1.)

    def result(self):
        return self.metric

    def reset(self):
        for i in range(len(self.metric)):
            self.metric[i].assign(0.)
        self.tics.assign(0.)
