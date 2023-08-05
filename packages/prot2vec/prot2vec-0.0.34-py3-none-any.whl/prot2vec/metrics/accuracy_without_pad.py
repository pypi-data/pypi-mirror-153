from tensorflow.keras import backend as K
from tensorflow.keras.metrics import Metric, sparse_categorical_accuracy


class AccuracyWithoutPad(Metric):
    def __init__(self, name='accuracy_without_pad'):
        super(AccuracyWithoutPad, self).__init__()
        self.accuracy = self.add_weight(name=name, initializer='zeros')
        self.tics = self.add_weight(name='tics', initializer='zeros')

    def update_state(self, y_true, y_pred, x=None, sample_weight=None):
        y_true = y_true[:, 1:-1]
        y_pred = y_pred[:, 1:-1]
        acc = sparse_categorical_accuracy(y_true, y_pred)
        acc = K.mean(acc)

        self.accuracy.assign_add(acc)
        self.tics.assign_add(1.)

    def result(self):
        return self.accuracy / self.tics

    def reset(self):
        self.accuracy.assign(0.)
        self.tics.assign(0.)
