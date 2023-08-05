import numpy as np
import tensorflow as tf

from .sentence_piece import data_gen, random_iter
from .sentence_piece_termostat import data_gen_termostat


def data_gen_svec(data_path, tokenizer, batch_size, max_len, mask_prob=0.15, overfit_batch=False, helper_mode='none',
                  once=False, session_steps=-1, skip_shorter_than=None):
    gen = data_gen(data_path, tokenizer, batch_size, max_len, mask_prob, overfit_batch, helper_mode, once,
                   session_steps, skip_shorter_than)

    while True:
        tokens_in, tokens_out, mask = next(gen)

        yield ({"tokens": tokens_in, "mask": mask},
               {"deemb": tokens_out, "emb": tokens_out},
               )


def data_gen_termostat_svec(data_path, tokenizer, batch_size, max_len, hint_callback, mask_prob=0.15):
    gen = data_gen_termostat(data_path, tokenizer, batch_size, max_len, hint_callback, mask_prob)

    while True:
        tokens_in, tokens_out, mask = next(gen)

        yield ({"tokens": tokens_in, "mask": mask},
               {"deemb": tokens_out, "emb": tokens_out},
               mask
               )


def random_iter_svec(batch_size, max_len, mask_prob, helper_mode='none', session_steps=-1):
    gen = random_iter(batch_size, max_len, mask_prob, helper_mode, session_steps)

    while True:
        tokens_in, tokens_out = next(gen)

        bert_mask = tf.logical_or(tokens_in == TOKENIZER.mask_token_id, tokens_in > len(TOKENIZER.vocab))

        yield ({"tokens": tokens_in, "mask": bert_mask},
               {"deemb": tokens_out, "emb": tokens_out},
               )
