import json
import os

from keras_pos_embd import PositionEmbedding, TrigPosEmbedding
from tensorflow.keras.layers import Input, Lambda, GaussianNoise, RepeatVector, LayerNormalization, Activation, Dense, \
    Embedding
from tensorflow.keras.models import Model, load_model
from transformers.optimization_tf import WarmUp

from ..layers.ioembedding import IOEmbedding
from ..layers.transformer_block import TransformerBlock


def get_model(max_len, dim, num_layers, num_heads, ff_dim, vocab_siz, model_dir=None, train_from_scratch=True,
              short_circuit_reduction=False, gaussian_std=None, with_hints=True):
    input_in = Input(shape=(max_len, dim), dtype='float32')

    # interim = TrigPosEmbedding(mode=TrigPosEmbedding.MODE_ADD)(input_in)
    interim = PositionEmbedding(input_dim=max_len, output_dim=dim, mode=PositionEmbedding.MODE_ADD)(input_in)

    for i in range(num_layers):
        interim = TransformerBlock(embed_dim=dim, num_heads=num_heads, ff_dim=ff_dim)(interim)
    encoded_full = interim

    encoded_input = Input(shape=(dim,), dtype='float32')
    encoded_unrolled = RepeatVector(max_len)(encoded_input)

    interim = PositionEmbedding(input_dim=max_len, output_dim=dim, mode=PositionEmbedding.MODE_ADD)(encoded_unrolled)
    interim = LayerNormalization(epsilon=1e-6)(interim)

    for i in range(num_layers):
        interim = TransformerBlock(embed_dim=dim, num_heads=num_heads, ff_dim=ff_dim)(interim)
    decoded_output = interim

    if model_dir is not None and os.path.isdir(model_dir) and not train_from_scratch:
        print("Loading model from", model_dir)
        model = load_model(os.path.join(model_dir, "model"),
                           custom_objects={"WarmUp": WarmUp, "TransformerBlock": TransformerBlock,
                                           "IOEmbedding": IOEmbedding})

        with open(f"{model_dir}/config.json", "r", encoding="utf-8") as fr:
            TRAIN_STATE = json.load(fr)
            INITIAL_EPOCH = TRAIN_STATE["INITIAL_EPOCH"]
        print(f"Training will start from state: {TRAIN_STATE}")
    else:
        print("Initializing a new model from scratch")

        if with_hints:
            vocab_siz = int(vocab_siz * 1.2)

        emb_layer = IOEmbedding(input_dim=vocab_siz, output_dim=dim, name="ioembedding")
        emb_layer_2 = Embedding(input_dim=vocab_siz, output_dim=dim)

        embedder = Model(input_in, encoded_full, name="embedder")

        # reduction = Model(ae_input, encoded_reduced, name="reduction")
        # expansion = Model(ae_reduced, encoded_expanded, name="expansion")
        deembedder = Model(encoded_input, decoded_output, name="deembedder")
        TRAIN_STATE = {}

        model_in = Input(shape=(max_len,), dtype='int32', name="input_tokens")
        model_mask = Input(shape=(max_len,), dtype='int32', name="input_mask")

        x = emb_layer_2(model_in)
        x = embedder(x)

        # masked_out = emb_layer([x, model_mask], inverse=True)
        masked_out = Dense(vocab_siz, 'softmax')(x)

        x = Lambda((lambda i: i[:, 0]), name="bos_vector")(x)

        if not short_circuit_reduction:
            x = reduction(x)
        if gaussian_std is not None:
            x = GaussianNoise(gaussian_std)(x)
        if not short_circuit_reduction:
            x = expansion(x)
        x = deembedder(x)

        out = emb_layer(x, inverse=True)
        out = Activation('softmax')(out)
        model = Model(inputs={"tokens": model_in, "mask": model_mask}, outputs={"deemb": out, "emb": masked_out})

    return model


def get_model_2(max_len, dim, num_layers, num_heads, ff_dim, vocab_siz):
    model_mask = Input(shape=(max_len,), dtype='int32', name="input_mask")
    input_in = Input(shape=(max_len, dim), dtype='float32')

    # interim = TrigPosEmbedding(mode=TrigPosEmbedding.MODE_ADD)(input_in)
    interim = PositionEmbedding(input_dim=max_len, output_dim=dim, mode=PositionEmbedding.MODE_ADD)(input_in)

    for i in range(num_layers):
        interim = TransformerBlock(embed_dim=dim, num_heads=num_heads, ff_dim=ff_dim)(interim)
    encoded_full = interim

    vocab_siz = int(vocab_siz * 1.2)

    # emb_layer = IOEmbedding(input_dim=vocab_siz, output_dim=dim, name="ioembedding")
    emb_layer_2 = Embedding(input_dim=vocab_siz, output_dim=dim)

    embedder = Model(input_in, encoded_full, name="embedder")

    model_in = Input(shape=(max_len,), dtype='int32', name="input_tokens")

    x = emb_layer_2(model_in)
    x = embedder(x)

    masked_out = Dense(vocab_siz, 'softmax')(x)

    model = Model(inputs={"tokens": model_in, "mask": model_mask}, outputs={"deemb": masked_out, "emb": masked_out})

    return model


def get_model_3(max_len, dim, num_layers, num_heads, ff_dim, vocab_siz):
    vocab_siz = int(vocab_siz * 1.2)

    ### Embedder
    input_in = Input(shape=(max_len, dim), dtype='float32')
    interim = PositionEmbedding(input_dim=max_len, output_dim=dim, mode=PositionEmbedding.MODE_ADD)(input_in)
    for i in range(num_layers):
        interim = TransformerBlock(embed_dim=dim, num_heads=num_heads, ff_dim=ff_dim)(interim)
    encoded_full = interim
    embedder = Model(input_in, encoded_full, name="embedder")
    ###

    model_in = Input(shape=(max_len,), dtype='int32', name="input_tokens")
    x = Embedding(input_dim=vocab_siz, output_dim=dim)(model_in)
    x = embedder(x)
    masked_out = Dense(vocab_siz, 'softmax')(x)

    model = Model(inputs=[model_in], outputs=[masked_out])

    return model


if __name__ == '__main__':
    test_obj = get_model(24, 256, 4, 4, 1024, 8000)
    print()
