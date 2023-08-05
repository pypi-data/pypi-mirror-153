from tensorflow.keras.layers import Input, Dense, Conv1D, MaxPool1D, Dropout, Conv1DTranspose
from tensorflow.keras.models import Model

from prot2vec.layers.transformer_block import TransformerBlock


def get_convtransformer_full_len(seq_len, seq_depth, kernel_size, dropout, n_layers, n_heads, ff_dim):
    input_layer = Input(shape=(seq_len, seq_depth), name='input_seq')

    x = Conv1D(256, kernel_size * 2 + 1, activation='relu', strides=1, padding='same', dilation_rate=1)(input_layer)
    x = Dropout(dropout)(x)

    for i in range(n_layers):
        x = TransformerBlock(embed_dim=256, num_heads=n_heads, ff_dim=ff_dim, dropout=dropout, ff_activation='relu')(x)

    output_layer = Dense(seq_depth, activation='softmax')(x)

    model = Model(inputs=[input_layer], outputs=[output_layer], name="convtransformer_full_len")

    return model


def get_convtransformer(seq_len, seq_depth, kernel_size, dropout, n_layers, n_heads, ff_dim):
    input_layer = Input(shape=(seq_len, seq_depth), name='input_seq')

    x = Conv1D(64, kernel_size * 2 + 1, activation='relu', strides=1, padding='same', dilation_rate=1)(input_layer)
    x = Dropout(dropout)(x)
    # x = Conv1D(64, kernel_size * 2 + 1, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    # x = Dropout(dropout)(x)

    x = MaxPool1D(2)(x)  # seq_len / 2

    x = Conv1D(128, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    # x = Conv1D(128, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    # x = Dropout(dropout)(x)

    x = MaxPool1D(2)(x)  # seq_len / 4

    x = Conv1D(256, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    # x = Conv1D(256, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    # x = Dropout(dropout)(x)

    for i in range(n_layers):
        x = TransformerBlock(embed_dim=256, num_heads=n_heads, ff_dim=ff_dim, dropout=dropout, ff_activation='relu')(x)

    x = Conv1DTranspose(128, kernel_size, activation='relu', padding='same', strides=2, dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    x = Conv1DTranspose(64, kernel_size, activation='relu', padding='same', strides=2, dilation_rate=1)(x)
    x = Dropout(dropout)(x)

    output_layer = Dense(seq_depth, activation='softmax')(x)

    model = Model(inputs=[input_layer], outputs=[output_layer], name="convtransformer")

    return model


def get_convtransformer_deep(seq_len, seq_depth, kernel_size, dropout, n_layers, n_heads, ff_dim):
    input_layer = Input(shape=(seq_len, seq_depth), name='input_seq')

    x = Conv1D(64, kernel_size * 2 + 1, activation='relu', strides=1, padding='same', dilation_rate=1)(input_layer)
    x = Dropout(dropout)(x)
    x = Conv1D(64, kernel_size * 2 + 1, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    x = Conv1D(64, kernel_size * 2 + 1, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)

    x = MaxPool1D(2)(x)  # seq_len / 2

    x = Conv1D(128, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    x = Conv1D(128, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    x = Conv1D(128, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)

    x = MaxPool1D(2)(x)  # seq_len / 4

    x = Conv1D(256, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    # x = Conv1D(256, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    # x = Dropout(dropout)(x)

    for i in range(n_layers):
        x = TransformerBlock(embed_dim=256, num_heads=n_heads, ff_dim=ff_dim, dropout=dropout, ff_activation='relu')(x)

    x = Conv1D(256, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    x = Conv1D(256, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    x = Conv1DTranspose(128, kernel_size, activation='relu', padding='same', strides=2, dilation_rate=1)(x)
    x = Dropout(dropout)(x)

    x = Conv1D(128, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    x = Conv1D(128, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)

    x = Conv1D(64, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    x = Conv1D(64, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)
    x = Conv1DTranspose(64, kernel_size, activation='relu', padding='same', strides=2, dilation_rate=1)(x)
    x = Dropout(dropout)(x)

    output_layer = Dense(seq_depth, activation='softmax')(x)

    model = Model(inputs=[input_layer], outputs=[output_layer], name="convtransformer")

    return model


if __name__ == '__main__':
    seq_len = 64
    seq_depth = 21
    kernel_size = 5
    dropout = 0.1
    n_layers = 4
    n_heads = 4
    ff_dim = 1024

    convtransformer_full_len = get_convtransformer_full_len(seq_len, seq_depth, kernel_size, dropout, n_layers, n_heads,
                                                            ff_dim)
    convtransformer = get_convtransformer(seq_len, seq_depth, kernel_size, dropout, n_layers, n_heads, ff_dim)

    print()
