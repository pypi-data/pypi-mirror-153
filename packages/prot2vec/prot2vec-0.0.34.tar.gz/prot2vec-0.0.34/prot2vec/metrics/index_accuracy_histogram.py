import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.metrics import Metric


def update_metric(x_prev, x_now, i):
    return (1 / (i + 1)) * (i * x_prev + x_now)


class IndexAccHist(Metric):
    def __init__(self, name='index_accuracy_histogram'):
        super(IndexAccHist, self).__init__()
        self.metric_name = name
        self.metric = []
        self.tics = self.add_weight(name='tics', initializer="zeros")

    def update_state(self, y_true, y_pred, x=None, sample_weight=None):
        y_pred = tf.argmax(y_pred, axis=-1, output_type=tf.int32)
        equals = tf.cast(y_pred == y_true, tf.float32)
        new_index_accs = K.sum(equals, axis=0) / equals.shape[0]
        for i in range(new_index_accs.shape[0]):
            if i >= len(self.metric):
                self.metric.append(self.add_weight(name=self.metric_name + str(i), initializer="zeros"))
            self.metric[i].assign(update_metric(self.metric[i], new_index_accs[i], self.tics))

        self.tics.assign_add(1.)

    def result(self):
        return self.metric

    def reset(self):
        for i in range(len(self.metric)):
            self.metric[i].assign(0.)

        self.tics.assign(0.)
