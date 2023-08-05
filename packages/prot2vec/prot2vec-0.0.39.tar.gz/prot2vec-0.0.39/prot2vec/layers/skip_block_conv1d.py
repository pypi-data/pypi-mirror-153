from tensorflow.keras.layers import Add, Dropout, BatchNormalization, Activation, Conv1D, Conv1DTranspose


def conv1D_identity_block(x, kernels, kernel_size, dropout=0.1, activation='relu'):
    x_skip = x
    # Layer 1
    x = Conv1D(kernels, kernel_size, padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation(activation)(x)
    if dropout > 0.0001:
        x = Dropout(dropout)(x)
    # Layer 2
    x = Conv1D(kernels, kernel_size, padding='same')(x)
    x = BatchNormalization()(x)
    # Add Residue
    x = Add()([x, x_skip])
    x = Activation(activation)(x)
    if dropout > 0.0001:
        x = Dropout(dropout)(x)
    return x


def conv1D_conv_block(x, kernels, kernel_size, dropout=0.1, activation='relu'):
    x_skip = x
    # Layer 1
    x = Conv1D(kernels, kernel_size, padding='same', strides=2)(x)
    x = BatchNormalization()(x)
    x = Activation(activation)(x)
    if dropout > 0.0001:
        x = Dropout(dropout)(x)
    # Layer 2
    x = Conv1D(kernels, kernel_size, padding='same')(x)
    x = BatchNormalization()(x)

    x_skip = Conv1D(kernels, 1, strides=2)(x_skip)
    # Add Residue
    x = Add()([x, x_skip])
    x = Activation(activation)(x)
    if dropout > 0.0001:
        x = Dropout(dropout)(x)
    return x


def conv1D_deconv_block(x, kernels, kernel_size, dropout=0.1, activation='relu'):
    x_skip = x
    # Layer 1
    x = Conv1DTranspose(kernels, kernel_size, padding='same', strides=2)(x)
    x = BatchNormalization()(x)
    x = Activation(activation)(x)
    if dropout > 0.0001:
        x = Dropout(dropout)(x)
    # Layer 2
    x = Conv1D(kernels, kernel_size, padding='same')(x)
    x = BatchNormalization()(x)

    x_skip = Conv1DTranspose(kernels, 1, strides=2)(x_skip)
    # Add Residue
    x = Add()([x, x_skip])
    x = Activation(activation)(x)
    if dropout > 0.0001:
        x = Dropout(dropout)(x)
    return x
