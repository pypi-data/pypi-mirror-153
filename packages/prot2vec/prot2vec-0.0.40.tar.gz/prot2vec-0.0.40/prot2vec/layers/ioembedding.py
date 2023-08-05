from tensorflow import keras
import tensorflow.keras.backend as K
import tensorflow as tf


class IOEmbedding(keras.layers.Embedding):
    def __init__(self,
                 initializer='zeros',
                 regularizer=None,
                 constraint=None,
                 **kwargs):
        super(IOEmbedding, self).__init__(**kwargs)
        self.supports_masking = True
        self.initializer = keras.initializers.get(initializer)
        self.regularizer = keras.regularizers.get(regularizer)
        self.constraint = keras.constraints.get(constraint)
        self.bias = None

    def get_config(self):
        config = {
            'initializer': keras.initializers.serialize(self.initializer),
            'regularizer': keras.regularizers.serialize(self.regularizer),
            'constraint': keras.constraints.serialize(self.constraint),
        }
        base_config = super(IOEmbedding, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def build(self, input_shape):
        self.bias = self.add_weight(
            shape=(self.input_dim,),
            initializer=self.initializer,
            regularizer=self.regularizer,
            constraint=self.constraint,
            name='bias',
        )
        super(IOEmbedding, self).build(input_shape)

    def compute_mask(self, inputs, inverse=False, mask=None):
        if not isinstance(inputs, list) or len(inputs) != 2:
            return super(IOEmbedding, self).compute_mask(inputs, mask)
        else:
            token_mask = K.not_equal(inputs[1], 0)
            return token_mask

    def call(self, inputs, mask=None, inverse=False, **kwargs):
        if not inverse:
            return super(IOEmbedding, self).call(inputs)
        else:
            if not isinstance(inputs, list):
                inputs = [inputs]
            
            return tf.tensordot(inputs[0], self.embeddings, [[2], [1]])+self.bias
