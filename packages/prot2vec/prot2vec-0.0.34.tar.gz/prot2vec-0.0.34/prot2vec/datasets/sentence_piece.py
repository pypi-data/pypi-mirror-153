import json

import numpy as np


# GROUPS_REVERSE = json.load(open('prot2vec/configs/helper_groups_reverse.json', 'r', encoding='utf-8'))
# GROUPS_REVERSE = json.load(open('../configs/helper_groups_reverse.json', 'r', encoding='utf-8'))


def mask_by_helper_tokens(tokens_in, bool_mask, help_distrib, tokenizer):
    to_replace = tokens_in[bool_mask]

    help_distrib = np.array([help_distrib['10'], help_distrib['100'], help_distrib['1000'], help_distrib['none']])
    selected_helps = np.array(['10', '100', '1000', 'none'])[np.random.choice(4, len(to_replace), p=help_distrib)]

    replacement = []
    for j in range(len(to_replace)):
        selected_help = selected_helps[j]
        orig_token = to_replace[j]
        mask_token = tokenizer.mask_token_id if selected_help == 'none' else GROUPS_REVERSE[str(orig_token)][
            selected_help]
        replacement.append(mask_token)

    tokens_in[bool_mask] = np.array(replacement)
    return tokens_in


def mask_data(data, mask_prob, help_distrib, tokenizer):
    bool_mask = np.random.rand(data.shape[0] * data.shape[1]) < mask_prob
    bool_mask = bool_mask.reshape(data.shape)
    bool_mask[:, 0] = False
    bool_mask[:, -1] = False

    data = mask_by_helper_tokens(data, bool_mask, help_distrib, tokenizer)
    return data, bool_mask


def vectorize_batch(batch, mask_prob, help_distrib, tokenizer):
    tokens_in = np.concatenate(batch, axis=0)
    tokens_out = tokens_in.copy()
    if mask_prob > 1e-6:
        tokens_in, mask = mask_data(tokens_in, mask_prob, help_distrib, tokenizer)

    return tokens_in, tokens_out, mask


def get_help_scheduler(helper_mode):
    if helper_mode == '10':
        help_sched = lambda x: {'10': 1., '100': 0., '1000': 0., 'none': 0.}
    elif helper_mode == '100':
        help_sched = lambda x: {'10': 0., '100': 1., '1000': 0., 'none': 0.}
    elif helper_mode == '1000':
        help_sched = lambda x: {'10': 0., '100': 0., '1000': 1., 'none': 0.}
    elif helper_mode == 'none':
        help_sched = lambda x: {'10': 0., '100': 0., '1000': 0., 'none': 1.}
    elif helper_mode == 'continuous':
        help_sched = lambda x: {'10': (x < 1 / 3) * (1 - 3 * x),
                                '100': (x < 1 / 3) * (3 * x) + (1 / 3 <= x < 2 / 3) * (2 - 3 * x),
                                '1000': (1 / 3 <= x < 2 / 3) * (3 * x - 1) + (2 / 3 <= x) * (3 - 3 * x),
                                'none': (2 / 3 <= x) * (3 * x - 2)}
    else:
        raise Exception(f'helper_mode \"{helper_mode}\" is not supported.')

    return help_sched


def data_gen(data_path, tokenizer, batch_size, max_len, mask_prob=0.15, overfit_batch=False, helper_mode='none',
             once=False, session_steps=-1, skip_shorter_than=None):
    if skip_shorter_than is None:
        skip_shorter_than = max_len
    # Setup helper scheduler
    help_sched = get_help_scheduler(helper_mode)
    step = 0

    if helper_mode == 'continuous':
        assert session_steps > 0

    while True:
        batch = []
        with open(data_path, "r", encoding="utf-8") as fr:
            fr.readline()
            for line in fr:
                items = line.strip().split("\t")
                id, seq_id, seq = items

                tokens = tokenizer(seq)['input_ids']
                if len(tokens) < skip_shorter_than:
                    continue

                offset = np.random.randint(0, len(tokens) - max_len + 1)
                tokens = tokens[offset:offset + max_len]
                tokens[0] = tokenizer.cls_token_id
                tokens[-1] = tokenizer.eos_token_id

                batch.append(np.array(tokens)[None, :])

                if len(batch) >= batch_size:
                    v_batch = vectorize_batch(batch, mask_prob, help_sched(min(step / session_steps, 1.)), tokenizer)
                    if overfit_batch:
                        while True:
                            yield v_batch
                    yield v_batch
                    step += 1
                    del batch[:]

        if once:
            v_batch = vectorize_batch(batch, mask_prob, help_sched(min(step / session_steps, 1.)), tokenizer)
            yield v_batch
            break


def random_iter(tokenizer, batch_size, max_len, mask_prob, helper_mode='none', session_steps=-1):
    with open('prot2vec/configs/1st_order_random_dict.json', 'r', encoding='utf-8') as fr:
        sp_probs = json.load(fr)
    sp_probs = sorted([(int(k), v) for k, v in sp_probs.items()], key=lambda x: x[1])
    sp_ids = np.array([k for k, v in sp_probs])
    probs = [v for k, v in sp_probs]

    help_sched = get_help_scheduler(helper_mode)
    if helper_mode == 'continuous':
        assert session_steps > 0
    step = 1

    while True:
        selected_indexes = np.random.choice(len(sp_ids), max_len * batch_size, p=probs)
        tokens_in = sp_ids[selected_indexes]
        tokens_in = tokens_in.reshape((batch_size, max_len))
        tokens_in[:, 0] = 0
        tokens_in[:, -1] = 2

        tokens_out = tokens_in.copy()

        if mask_prob > 1e-6:
            tokens_in = mask_data(tokens_in, mask_prob, help_sched(min(step / session_steps, 1.)), tokenizer)

        yield tokens_in, tokens_out
        step += 1
