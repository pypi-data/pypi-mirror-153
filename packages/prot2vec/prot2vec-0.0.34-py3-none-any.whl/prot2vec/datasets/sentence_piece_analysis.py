import numpy as np
from copy import deepcopy
import json
import datetime as dt
import pickle

from ..analysis.index_accuracy import (
    check_lengths,
    extract_results as extract_results_indexes,
)
from ..analysis.sentencepiece_and_protein_accuracy import (
    extract_results as extract_results_sp_prot,
)


def vectorize_seq(seq, max_len, tokenizer):
    inputs = tokenizer.encode_plus(
        seq,
        add_special_tokens=True,
        max_length=max_len,
        padding="max_length",
        truncation=True,
    )
    input_ids = inputs["input_ids"]
    return input_ids


def vectorize_batch_same_mask_position(batch, mask_position, max_len, tokenizer):
    tokens_in = []

    for (t_in,) in batch:
        t_in = vectorize_seq(t_in, max_len, tokenizer)

        tokens_in.append(t_in)

    tokens_in = np.array(tokens_in, dtype=np.int32)
    mask = np.zeros(tokens_in.shape)

    tokens_masked = deepcopy(tokens_in)

    masked_indexes = [[mask_position] for _ in range(tokens_in.shape[0])]
    masked_coord_y = np.concatenate(masked_indexes)
    masked_coord_x = np.repeat(np.arange(tokens_in.shape[0]), 1)

    tokens_masked[masked_coord_x, masked_coord_y] = tokenizer.mask_token_id

    mask[masked_coord_x, masked_coord_y] = 1

    return tokens_masked, tokens_in, mask


def vectorize_batch_diff_mask_position(batch, masked_positions, max_len, tokenizer):
    tokens_in = []
    domain_linker = list()

    for ((t_in,), dom_lin) in batch:
        t_in = vectorize_seq(t_in, max_len, tokenizer)

        tokens_in.append(t_in)
        domain_linker.append(dom_lin)

    tokens_in = np.array(tokens_in, dtype=np.int32)
    mask = np.zeros(tokens_in.shape)

    tokens_masked = deepcopy(tokens_in)

    masked_indexes = [[masked_positions[i]] for i in range(tokens_in.shape[0])]
    masked_coord_y = np.concatenate(masked_indexes)
    masked_coord_x = np.repeat(np.arange(tokens_in.shape[0]), 1)

    tokens_masked[masked_coord_x, masked_coord_y] = tokenizer.mask_token_id

    mask[masked_coord_x, masked_coord_y] = 1

    return tokens_masked, tokens_in, mask, domain_linker


def get_protein_dom_link_info(key, tokens, seq, domains_info):

    domains = domains_info.get(key)
    if not domains:
        return ["U"] * len(tokens)

    link_dom_sp_vec = ["L"] * len(tokens)
    link_dom_aa_vec = ["L"] * len(seq)

    for domain in domains:
        for i in range(int(domain[1]), int(domain[2]) + 1):
            if i < len(link_dom_aa_vec):
                link_dom_aa_vec[i] = "D"

    actual_index = 0
    for i, token in enumerate(tokens):
        if link_dom_aa_vec[actual_index] == "D":
            link_dom_sp_vec[i] = "D"
        actual_index += len(token)

    return link_dom_sp_vec


def process_all_data(
    model,
    dataset_path,
    tokenizer,
    max_len,
    dev_size,
    results_path_sp,
    results_path_proteins,
    results_path_confusion,
    domains_info,
    save_every_nth=1000,
    print_every_nth=100,
    to_process=None,
    min_mask_index=4,
    matrix_identity=None,
    matrix_similarity=None,
    matrix_set_similarity=None,
    matrix_cosine_similarity=None,
):
    results_sp = dict()
    conf_matrix = dict()
    start_token = 5
    for i, key in enumerate(
        {k: v for k, v in sorted(tokenizer.vocab.items(), key=lambda item: item[1])}
    ):
        if i >= start_token:
            results_sp[key] = {
                "D": [0, 0, 0, 0, 0, 0, 0, 0],
                "L": [0, 0, 0, 0, 0, 0, 0, 0],
                "U": [0, 0, 0, 0, 0, 0, 0, 0],
            }
            conf_matrix[key] = [0] * (len(tokenizer.vocab) - start_token)
    inverted_vocab = {v: k for k, v in tokenizer.vocab.items()}

    max_len1 = max_len - 2
    processed = 0
    middle = max_len // 2
    max_mask_index = max_len - min_mask_index

    with open(dataset_path, "r", encoding="utf-8") as fr:

        batch = []
        masked_positions = []
        for line in fr:
            items = line.strip().split("\t")
            id, seq_id, seqF = items
            if id.endswith(";"):
                id = id[:-1]

            key = f"{id}-{seq_id}"

            tokens = tokenizer.tokenize(seqF)

            if len(tokens) < max_len1:
                continue

            dom_link_info = get_protein_dom_link_info(key, tokens, seqF, domains_info)
            results_protein = [list(), list()]

            offset = 0
            mask_index = min_mask_index
            while True:

                tokens1 = tokens[offset : offset + max_len1]
                seq1 = "".join(tokens1)

                batch.append(((seq1,), dom_link_info[offset + mask_index - 1]))
                masked_positions.append(mask_index)
                if len(batch) >= dev_size:
                    results_sp, results_protein, conf_matrix = extract_results_sp_prot(
                        model,
                        vectorize_batch_diff_mask_position(
                            batch, masked_positions, max_len, tokenizer
                        ),
                        masked_positions,
                        results_sp,
                        results_protein,
                        conf_matrix,
                        inverted_vocab,
                        matrix_identity,
                        matrix_similarity,
                        matrix_set_similarity,
                        matrix_cosine_similarity,
                        start_token,
                    )
                    del batch[:]
                    del masked_positions[:]

                if mask_index < middle:
                    mask_index += 1
                elif offset + max_len1 == len(tokens):
                    if mask_index < max_mask_index:
                        mask_index += 1
                    else:
                        break
                else:
                    offset += 1
            if batch:
                results_sp, results_protein, conf_matrix = extract_results_sp_prot(
                    model,
                    vectorize_batch_diff_mask_position(
                        batch, masked_positions, max_len, tokenizer
                    ),
                    masked_positions,
                    results_sp,
                    results_protein,
                    conf_matrix,
                    inverted_vocab,
                    matrix_identity,
                    matrix_similarity,
                    matrix_set_similarity,
                    matrix_cosine_similarity,
                    start_token,
                )
                del batch[:]
                del masked_positions[:]

            processed += 1

            with open(results_path_proteins, "ab") as af:
                prot_data = f"{key};{','.join(map(str, results_protein[0]))};{','.join(map(str, results_protein[1]))}\n"
                af.write(str.encode(prot_data))

            if processed % print_every_nth == 0:
                print(processed, end=", ")

            if processed % save_every_nth == 0:

                print(f"\nprocessed: {processed}, {dt.datetime.now()}", end=", ")
                with open(results_path_sp, "w") as wf:
                    json.dump(results_sp, wf)
                print(dt.datetime.now(), end=", ")
                with open(results_path_confusion, "wb") as wf:
                    pickle.dump(conf_matrix, wf)
                print(dt.datetime.now())

            if to_process and processed == to_process:
                break


def process_data_indexes(
    model,
    dataset_path,
    tokenizer,
    max_len,
    dev_size,
    results_path,
    save_every_nth=10,
    to_process=1000,
):
    mask_positions = range(1, max_len - 1)

    results = dict()
    for index in mask_positions:
        results[index] = (list(), list())

    max_len1 = max_len - 2
    processed = 0

    with open(dataset_path, "r", encoding="utf-8") as fr:

        batch = []
        for line in fr:
            items = line.strip().split("\t")
            _, _, seqF = items

            tokens = tokenizer.tokenize(seqF)

            if len(tokens) < max_len1 * 2 + 1:
                continue

            for mask_position in mask_positions:
                offset = max_len1 - mask_position
                border = len(tokens) - max_len1 + offset
                while True:

                    if offset + max_len1 >= border:
                        break

                    tokens1 = tokens[offset : offset + max_len1]
                    assert len(tokens1) == max_len1
                    seq1 = "".join(tokens1)

                    batch.append((seq1,))
                    if len(batch) >= dev_size:
                        results = extract_results_indexes(
                            model,
                            vectorize_batch_same_mask_position(
                                batch, mask_position, max_len, tokenizer
                            ),
                            mask_position,
                            results,
                        )
                        del batch[:]
                    offset += 1
                if batch:
                    results = extract_results_indexes(
                        model,
                        vectorize_batch_same_mask_position(
                            batch, mask_position, max_len, tokenizer
                        ),
                        mask_position,
                        results,
                    )
                    del batch[:]

            processed += 1

            print(processed, end=", ")

            if processed % save_every_nth == 0:
                check_lengths(results)
                print(f"\nprocessed: {processed}")
                with open(results_path, "w") as wf:
                    json.dump(results, wf)

            if to_process and processed == to_process:
                break


def read_architectures(datapath):
    # protein-id: [(domain name, start, end), ...]

    # read architectures
    ret = {}
    with open(datapath, "r", encoding="utf-8") as rf:
        for line in rf:
            items = line.strip().split("\t")
            # print(items)
            key = f"{items[0]}-{items[1]}"
            arch = [tuple(items[i : i + 3]) for i in range(2, len(items), 3)]
            ret[key] = arch
    return ret
