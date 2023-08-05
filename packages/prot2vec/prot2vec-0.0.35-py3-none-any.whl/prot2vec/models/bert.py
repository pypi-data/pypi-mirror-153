import math

from keras_pos_embd import PositionEmbedding
from tensorflow.keras.layers import Input, Dense, Embedding
from tensorflow.keras.models import Model

from prot2vec.layers.transformer_block import TransformerBlock


def bert_model(seq_len, embedding_size, vocab_size, n_layers, n_heads, ff_dim, with_hints=True):
    if with_hints:
        vocab_size = math.ceil(vocab_size * 1.11111111)

    input_layer = Input(shape=(seq_len,), dtype='int32', name='input_tokens')

    x = Embedding(vocab_size, embedding_size)(input_layer)
    x = PositionEmbedding(input_dim=seq_len, output_dim=embedding_size, mode=PositionEmbedding.MODE_ADD)(x)
    # x = TrigPosEmbedding(input_dim=seq_len, output_dim=embedding_size, mode=TrigPosEmbedding.MODE_ADD)(x)

    for i in range(n_layers):
        x = TransformerBlock(embed_dim=embedding_size, num_heads=n_heads, ff_dim=ff_dim)(x)

    output_layer = Dense(vocab_size, activation='softmax')(x)
    model = Model(inputs=[input_layer], outputs=[output_layer], name="prot_bert")

    return model


if __name__ == '__main__':
    b = bert_model(24, 256, 8000, 4, 4, 1024)
    print()
