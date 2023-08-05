import numpy as np


def mask_by_helper_tokens(tokens_in, bool_mask, hint_callback, tokenizer):
    to_replace = tokens_in[bool_mask]

    p = hint_callback.get_distribution()
    selected_helps = np.array(['10', '100', '1000', 'none'])[np.random.choice(4, len(to_replace), p=p)]

    replacement = []
    for j in range(len(to_replace)):
        selected_help = selected_helps[j]
        orig_token = to_replace[j]
        mask_token = tokenizer.mask_token_id if selected_help == 'none' else hint_callback.hints[str(orig_token)][
            selected_help]
        replacement.append(mask_token)

    tokens_in[bool_mask] = np.array(replacement)
    return tokens_in


def mask_data(data, mask_prob, hint_callback, tokenizer):
    bool_mask = np.random.rand(data.shape[0] * data.shape[1]) < mask_prob
    bool_mask = bool_mask.reshape(data.shape)
    bool_mask[:, 0] = False
    bool_mask[:, -1] = False

    data = mask_by_helper_tokens(data, bool_mask, hint_callback, tokenizer)
    return data, bool_mask


def vectorize_batch(batch, mask_prob, hint_callback, tokenizer):
    tokens_in = np.concatenate(batch, axis=0)
    tokens_out = tokens_in.copy()
    mask = np.ones(tokens_in.shape)
    if mask_prob > 1e-6:
        tokens_in, mask = mask_data(tokens_in, mask_prob, hint_callback, tokenizer)

    # Make soft zeros mask
    mask = mask.astype('float32') + 1e-5

    return tokens_in, tokens_out, mask


def data_gen_termostat(data_path, tokenizer, batch_size, max_len, hint_callback, mask_prob=0.15):
    while True:
        with open(data_path, "r", encoding="utf-8") as fr:
            batch = []
            for line in fr:
                items = line.strip().split("\t")
                id, seq_id, seq = items

                tokens = tokenizer(seq)['input_ids']
                if len(tokens) < max_len:
                    continue

                offset = np.random.randint(0, len(tokens) - max_len + 1)
                tokens = tokens[offset:offset + max_len]
                tokens[0] = tokenizer.cls_token_id
                tokens[-1] = tokenizer.eos_token_id

                batch.append(np.array(tokens)[None, :])

                if len(batch) >= batch_size:
                    v_batch = vectorize_batch(batch, mask_prob, hint_callback, tokenizer)
                    yield v_batch
                    del batch[:]
