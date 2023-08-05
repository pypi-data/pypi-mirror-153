import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Conv1D, BatchNormalization, Dropout, Input, Activation, Conv1DTranspose, Dense, \
    Concatenate
from tensorflow.keras.models import Model

from prot2vec.layers.skip_block_conv1d import conv1D_conv_block, conv1D_deconv_block, conv1D_identity_block


def get_smallworld_cnn(seq_len, seq_depth, kernel_size, dropout, n_of_kernels=128, n_of_layers=1):
    input_layer = Input(shape=(seq_len, seq_depth), name='input_seq')

    x = input_layer

    x = Conv1D(n_of_kernels, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
    x = Dropout(dropout)(x)

    conv_layers = [x]

    permuts = []

    k = 0
    for n in range(1, round(np.log2(n_of_kernels)) + 1):
        this_permut = []
        for j in range(k, k + round(((1 / 2) ** n) * n_of_kernels)):
            this_permut.append(k)
            k += 1

        permuts.append(this_permut)

    for i in range(1000):
        permuts.append([])  # not so elegant :/

    for i_layer in range(n_of_layers - 1):
        to_concatenate = [
            Conv1D(n_of_kernels, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)]

        for i_prev_layer in range(1, len(conv_layers) + 1):
            select_permut = permuts[i_prev_layer-1]
            if len(select_permut) < 1:
                continue
            # select_permut = permut[:round((0.5 ** i_prev_layer) * n_of_kernels)]

            add = tf.gather(conv_layers[-i_prev_layer], select_permut, axis=-1)
            to_concatenate.append(add)

        x = Concatenate(axis=-1)(to_concatenate)

        x = Dropout(dropout)(x)
        conv_layers.append(x)

    output_layer = Dense(seq_depth, activation='softmax')(x)

    model = Model(inputs=[input_layer], outputs=[output_layer], name="primitive_cnn")

    return model


def get_primitive_cnn(seq_len, seq_depth, kernel_size, dropout, n_of_kernels=256, n_of_layers=1):
    input_layer = Input(shape=(seq_len, seq_depth), name='input_seq')

    x = input_layer

    for i_layer in range(n_of_layers):
        x = Conv1D(n_of_kernels, kernel_size, activation='relu', strides=1, padding='same', dilation_rate=1)(x)
        x = Dropout(dropout)(x)
    output_layer = Dense(seq_depth, activation='softmax')(x)

    model = Model(inputs=[input_layer], outputs=[output_layer], name="primitive_cnn")

    return model


def conv1d_model(seq_len, onehot_size, dropout=0.1):
    x_input = Input((seq_len, onehot_size))

    x = Conv1D(128, kernel_size=9, strides=2, padding='same')(x_input)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Dropout(dropout)(x)

    # Define size of sub-blocks and initial filter size
    block_layers = [2, 3, 3, 2]
    kernels = 128
    # Step 3 Add the Resnet Blocks
    for i in range(4):
        if i == 0:
            # For sub-block 1 Residual/Convolutional block not needed
            for j in range(block_layers[i]):
                x = conv1D_identity_block(x, kernels, 5)
        else:
            # One Residual/Convolutional Block followed by Identity blocks
            # The filter size will go on increasing by a factor of 2
            kernels = kernels * 2
            x = conv1D_conv_block(x, kernels, 5)
            for j in range(block_layers[i] - 1):
                x = conv1D_identity_block(x, kernels, 5)

    #############
    # Define size of sub-blocks and initial filter size
    block_layers = [2, 3, 3]
    kernels = 1024
    # Step 3 Add the Resnet Blocks
    for i in range(3):
        kernels = kernels / 2
        x = conv1D_deconv_block(x, kernels, 5)
        for j in range(block_layers[i] - 1):
            x = conv1D_identity_block(x, kernels, 5)

    x = Conv1DTranspose(onehot_size, 9, padding='same', strides=2)(x)
    ae_out = Activation('softmax', name='ae_out')(x)

    model = Model(inputs=x_input, outputs=ae_out, name="conv1d_model")

    return model


if __name__ == '__main__':
    seq_len = 64
    seq_depth = 23
    kernel_size = 11
    dropout = 0.1
    smallworld_cnn = get_smallworld_cnn(seq_len, seq_depth, kernel_size, dropout, n_of_kernels=128, n_of_layers=20)

    print()
