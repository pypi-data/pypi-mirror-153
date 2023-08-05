import numpy as np
import json


class SentencePieceChangingHints(object):
    def __init__(self, probs_path, vocab_size, hint_size=10):
        with open(probs_path, 'r', encoding='utf-8') as fr:
            sp_probs = json.load(fr)

        sp_probs = sorted([(int(key), sp_probs[key]) for key in sp_probs], key=lambda x: x[0])

        sp_ids = [x[0] for x in sp_probs]
        sp_probs = [x[1] for x in sp_probs]
        sp_probs_cop = sp_probs.copy()
        sp_ids_cop = sp_ids.copy()

        groups = [[]]

        while len(sp_ids) > 0:
            if len(groups[-1]) >= hint_size:
                groups.append([])

            selected = np.random.choice(len(sp_ids), 1, p=sp_probs)
            assert len(selected == 1)
            selected = selected[0]

            groups[-1].append(sp_ids[selected])

            sp_ids.pop(selected)
            sp_probs.pop(selected)
            sp_probs = np.array(sp_probs)
            sp_probs = list(sp_probs / np.sum(sp_probs))

        self.hints = dict()
        for group_i, group in enumerate(groups):
            for tok in group:
                self.hints[tok] = vocab_size + group_i

    def __mask_by_helper_tokens(self, tokens_in, bool_mask, tokenizer):
        to_replace = tokens_in[bool_mask]

        replacement = [self.hints[tok] for tok in to_replace]

        tokens_in[bool_mask] = np.array(replacement)
        return tokens_in

    def __mask_data(self, data, mask_prob, tokenizer):
        bool_mask = np.random.rand(data.shape[0] * data.shape[1]) < mask_prob
        bool_mask = bool_mask.reshape(data.shape)
        bool_mask[:, 0] = False
        bool_mask[:, -1] = False

        data = self.__mask_by_helper_tokens(data, bool_mask, tokenizer)
        return data, bool_mask

    def __vectorize_batch(self, batch, mask_prob, tokenizer):
        tokens_in = np.concatenate(batch, axis=0)
        tokens_out = tokens_in.copy()
        mask = np.ones(tokens_in.shape)
        if mask_prob > 1e-6:
            tokens_in, mask = self.__mask_data(tokens_in, mask_prob, tokenizer)

        # Make soft zeros mask
        mask = mask.astype('float32') + 1e-5

        return tokens_in, tokens_out, mask

    def data_gen(self, data_path, tokenizer, batch_size, max_len, mask_prob=0.15):
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
                        v_batch = self.__vectorize_batch(batch, mask_prob, tokenizer)
                        yield v_batch
                        del batch[:]
