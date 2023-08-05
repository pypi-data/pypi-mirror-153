from tensorflow.keras.layers import Conv1D, Dropout, Input, Add, MaxPool1D, Flatten, Dense, Reshape, Conv1DTranspose
from tensorflow.keras.models import Model


def add_block(x, kernel_count, kernel_size, activation, dropout):
    x = Conv1D(kernel_count, kernel_size, activation=activation, padding='same')(x)
    x = Dropout(dropout)(x)
    skip = x
    x = Conv1D(kernel_count, kernel_size, activation=activation, padding='same')(x)
    x = Dropout(dropout)(x)
    x = Add()([x, skip])

    return x


def get_model(bottle_neck=256, seq_len=24, seq_depth=21, dropout=0.1):
    input_layer = Input(shape=(seq_len, seq_depth), name='input_layer')

    # (None, 24, seq_depth)
    x = input_layer

    # (None, 24, 128)
    x = add_block(x, 128, 5, 'relu', dropout)
    # x = add_block(x, 128, 5, 'relu', dropout)

    x = Conv1D(256, 5, activation='relu', padding='same', strides=2)(x)
    x = Dropout(dropout)(x)

    # (None, 12, 256)
    x = add_block(x, 256, 5, 'relu', dropout)
    # x = add_block(x, 256, 5, 'relu', dropout)

    x = Conv1D(512, 3, activation='relu', padding='same', strides=2)(x)
    x = Dropout(dropout)(x)

    # (None, 6, 512)
    x = add_block(x, 512, 3, 'relu', dropout)

    # (None, 3072)
    x = Flatten()(x)

    # (None, 2048)
    x = Dense(2048, activation='relu')(x)
    x = Dropout(dropout)(x)

    # (None, 256)
    embedded = Dense(bottle_neck, activation=None)(x)
    x = embedded
    x = Dropout(dropout)(x)

    # (None, 512)
    x = Dense(2048, activation=None)(x)
    x = Dropout(dropout)(x)

    # (None, 3072)
    x = Dense(3072, activation='relu')(x)
    x = Dropout(dropout)(x)

    # (None, 6, 512)
    x = Reshape((6, 512))(x)

    x = add_block(x, 512, 3, 'relu', dropout)
    # x = add_block(x, 512, 3, 'relu', dropout)

    # (None, 12, 256)
    x = Conv1DTranspose(256, 3, padding='same', strides=2)(x)
    x = Dropout(dropout)(x)

    x = add_block(x, 256, 5, 'relu', dropout)
    # x = add_block(x, 256, 5, 'relu', dropout)

    # (None, 24, 128)
    x = Conv1DTranspose(128, 5, padding='same', strides=2)(x)
    x = Dropout(dropout)(x)

    x = add_block(x, 128, 5, 'relu', dropout)
    # x = add_block(x, 128, 5, 'relu', dropout)

    # (None, 24, seq_depth)
    x = Dense(seq_depth, activation='softmax')(x)

    output_layer = x

    model = Model(inputs=input_layer, outputs=output_layer, name='conv1D_autoencoder')

    return model


if __name__ == '__main__':
    model = get_model()
    print()
