import numpy as np
import tensorflow as tf

AA_DICT = {'?': 0, '<': 1, '>': 2,
           'A': 3, 'C': 4, 'D': 5, 'E': 6, 'F': 7,
           'G': 8, 'H': 9, 'I': 10, 'K': 11, 'L': 12,
           'M': 13, 'N': 14, 'P': 15, 'Q': 16, 'R': 17,
           'S': 18, 'T': 19, 'V': 20, 'W': 21, 'Y': 22}

AA_DICT_REV = {AA_DICT[key]: key for key in AA_DICT}


# AA_DISTRIBUTION = np.load('prot2vec/configs/probab_distribution.npy')


def tokenize(seq):
    digit_seq = []
    for aa in seq:
        if aa not in AA_DICT:
            print(f'Unknown amino acid letter \"{aa}\"')
            return None
        digit_seq.append(AA_DICT[aa])

    digit_seq = np.array(digit_seq)

    digit_seq[0] = 1
    digit_seq[-1] = 2

    return digit_seq[None, :]


def mask_data(data, mask_prob, one_in_middle):
    if one_in_middle:
        bool_mask = np.zeros(data.shape, dtype='bool')
        mask_index = bool_mask.shape[1] // 2
        bool_mask[:, mask_index] = True
    else:
        bool_mask = np.random.rand(data.shape[0] * data.shape[1]) < mask_prob
        bool_mask = bool_mask.reshape(data.shape)

    bool_mask[:, 0] = False
    bool_mask[:, -1] = False

    to_replace = data[bool_mask]

    replacement = np.zeros(to_replace.shape, dtype='int32')

    data[bool_mask] = replacement

    return data, bool_mask


def vect_batch(batch, mask_prob, one_in_middle):
    x = np.concatenate(batch, axis=0)
    y = x.copy()

    x, mask = mask_data(x, mask_prob, one_in_middle)

    return tf.one_hot(x, len(AA_DICT)), tf.one_hot(y, len(AA_DICT)), mask


def random_iter(seq_len, masked_size, batch_size, overfit_batch=False):
    while True:
        seq_in_ = np.random.choice(len(AA_DISTRIBUTION), batch_size * seq_len, p=AA_DISTRIBUTION)

        seq_in = np.zeros((batch_size * seq_len, len(AA_DISTRIBUTION)))
        arang = np.arange(0, seq_in.shape[0])

        seq_in[arang, seq_in_] = 1.0
        seq_in = seq_in.reshape((batch_size, seq_len, len(AA_DISTRIBUTION)))

        m_offset = np.random.randint(0, seq_len - masked_size + 1)
        seq_out = seq_in[:, m_offset:m_offset + masked_size, :].copy()
        seq_in[:, m_offset:m_offset + masked_size, :] = 0.0

        if overfit_batch:
            while True:
                yield seq_in, seq_out

        yield seq_in, seq_out


def ds_iter(src_file, seq_len, mask_prob, batch_size, one_in_middle=False):
    batch = []
    while True:
        with open(src_file, "r", encoding="utf-8") as fr:
            fr.readline()
            for line in fr:
                _, _, seq = line[:-1].split('\t')
                prot_len = len(seq[:-1])
                if prot_len <= seq_len:
                    continue

                offset = np.random.randint(0, prot_len - seq_len + 1)
                seq = seq[offset:offset + seq_len]

                seq_in = tokenize(seq)

                if seq_in is None:
                    continue

                batch.append(seq_in)

                if len(batch) >= batch_size:
                    v_batch = vect_batch(batch, mask_prob, one_in_middle)
                    yield v_batch
                    del batch[:]


if __name__ == '__main__':
    from pathlib import Path

    ROOT = Path(r'C:\DATA\ML-Data\BioML\datasets\UniRef90')
    ds_it = ds_iter(ROOT / 'refprot_random_taxfree.tsv', 64, 0.15, 1024, True)
    a = next(ds_it)
    a = next(ds_it)
    a = next(ds_it)
    # start = time.time()
    for i in range(1000):
        a = next(ds_it)
    # print(time.time() - start)
