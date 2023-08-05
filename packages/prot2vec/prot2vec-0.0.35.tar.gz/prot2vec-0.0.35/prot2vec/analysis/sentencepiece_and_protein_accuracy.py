from copyreg import pickle
import json
from matplotlib import rcParams, pyplot as plt
import numpy as np
import pickle

from tensorflow.keras import backend as K
from transformers.modeling_tf_outputs import TFMaskedLMOutput


def extract_results(
    model,
    data,
    masked_positions,
    results_sp: dict,
    results_prot: list,
    conf_matrix: dict,
    inverted_vocab: dict,
    matrix_identity=None,
    matrix_similarity=None,
    matrix_set_similarity=None,
    matrix_cosine_similarity=None,
    start_token=5,
):
    predictions = model.predict(data[0])
    if isinstance(predictions, TFMaskedLMOutput):
        predictions = K.softmax(predictions.logits, axis=-1)
    predicted_tokens = K.argmax(predictions, axis=-1)

    for i, prediction in enumerate(predictions):
        dom_lin = data[3][i]

        argmax_token = int(predicted_tokens[i][masked_positions[i]])
        true_token = data[1][i][masked_positions[i]]
        true_token_seq = inverted_vocab[true_token]

        soft_argmax = float(prediction[masked_positions[i]][argmax_token])
        soft_true = float(prediction[masked_positions[i]][true_token])

        ratio = soft_true / soft_argmax
        hit = 1 if ratio > 0.999 else 0

        results_sp[true_token_seq][dom_lin][0] += hit
        results_sp[true_token_seq][dom_lin][1] += soft_true
        results_sp[true_token_seq][dom_lin][2] += soft_argmax
        results_sp[true_token_seq][dom_lin][3] += 1

        results_prot[0].append(round(soft_true, 5))
        results_prot[1].append(round(soft_argmax, 5))

        conf_matrix[true_token_seq][argmax_token - start_token] += 1

        if matrix_identity:
            results_sp[true_token_seq][dom_lin][4] += matrix_identity[true_token_seq][
                argmax_token - start_token
            ]
        if matrix_similarity:
            results_sp[true_token_seq][dom_lin][5] += matrix_similarity[true_token_seq][
                argmax_token - start_token
            ]
        if matrix_set_similarity:
            results_sp[true_token_seq][dom_lin][6] += matrix_set_similarity[
                true_token_seq
            ][argmax_token - start_token]
        if matrix_cosine_similarity:
            results_sp[true_token_seq][dom_lin][7] += matrix_cosine_similarity[
                true_token_seq
            ][argmax_token - start_token]

    return results_sp, results_prot, conf_matrix


def plot_A(x_sets, y_sets, title, legend=[], alpha=0.1):
    rcParams.update({"figure.autolayout": True})
    plt.figure(figsize=(17, 3.5))
    plt.ion()

    for x, y in zip(x_sets, y_sets):
        plt.scatter(x, y, alpha=alpha)

    plt.title(title)
    plt.xlabel("occurence")
    plt.ylabel("accuracy")
    plt.legend(legend)
    plt.grid()
    plt.show()


def plot_B(accuracies, title):
    rcParams.update({"figure.autolayout": True})
    plt.figure(figsize=(17, 3.5))
    plt.ion()

    plt.hist(accuracies, bins=100)

    plt.title(title)
    plt.xlabel("accuracy")
    plt.ylabel("amount of units")
    plt.grid()
    plt.show()


def show_results_sp(
    results_path,
):
    with open(results_path, "r") as rf:
        data = json.load(rf)

    results_structure = {
        "accuracy": 0,
        "identity": 4,
        "similarity": 5,
        "set_similarity": 6,
    }

    metrics = {
        "accuracy": [],
        "identity": [],
        "similarity": [],
        "set_similarity": [],
    }

    combined_sets_values = list()
    combined_sets_occurances = list()

    for mode, index in results_structure.items():
        values_domains = list()
        occurence_domains = list()
        values_linkers = list()
        occurence_linkers = list()
        values_unknown = list()
        occurence_unknown = list()

        values_concatenated = list()
        occurence_concatenated = list()

        for token in data.keys():
            values_sum = 0
            occ_sum = 0
            for type_dom_lin, type_data in data[token].items():
                occ = int(type_data[3])
                index_values = int(type_data[index])
                value = 0 if not occ else index_values / occ
                if type_dom_lin == "D":
                    values_domains.append(value)
                    occurence_domains.append(occ)
                elif type_dom_lin == "L":
                    values_linkers.append(value)
                    occurence_linkers.append(occ)
                elif type_dom_lin == "U":
                    values_unknown.append(value)
                    occurence_unknown.append(occ)

                values_sum += index_values
                occ_sum += occ
            avg_sum = 0 if not occ_sum else values_sum / occ_sum
            values_concatenated.append(avg_sum)
            occurence_concatenated.append(occ_sum)

        res = (
            sum(values_domains) / sum(occurence_domains)
            if sum(occurence_domains)
            else 0
        )
        metrics[mode].append(res)
        print(f"domains {mode}: {res}")
        res = (
            sum(values_linkers) / sum(occurence_linkers)
            if sum(occurence_linkers)
            else 0
        )
        metrics[mode].append(res)
        print(f"linkers {mode}: {res}")
        res = (
            sum(values_unknown) / sum(occurence_unknown)
            if sum(occurence_unknown)
            else 0
        )
        metrics[mode].append(res)
        print(f"unknown {mode}: {res}")

        plot_A(
            [occurence_domains], [values_domains], f"Tokens {mode}-occurence: domains"
        )
        plot_B(values_domains, f"Tokens {mode} histogram: domains")
        plot_A(
            [occurence_linkers], [values_linkers], f"Tokens {mode}-occurence: linkers"
        )
        plot_B(values_linkers, f"Tokens {mode} histogram: linkers")
        plot_A(
            [occurence_unknown], [values_unknown], f"Tokens {mode}-occurence: unknown"
        )
        plot_B(values_unknown, f"Tokens {mode} histogram: unknown")

        plot_A(
            [occurence_domains, occurence_linkers, occurence_unknown],
            [values_domains, values_linkers, values_unknown],
            f"Tokens {mode}-occurence: comparison",
            ["domains", "linkers", "unknown"],
        )
        plot_A(
            [occurence_concatenated],
            [values_concatenated],
            f"Tokens {mode}-occurence: combined",
        )

        combined_sets_occurances.append(occurence_concatenated)
        combined_sets_values.append(values_concatenated)

    plot_A(
        combined_sets_occurances,
        combined_sets_values,
        f"modes comparison",
        list(results_structure.keys()),
    )

    plot_A(
        [range(3) for _ in range(len(metrics))],
        list(metrics.values()),
        f"metrics",
        list(results_structure.keys()),
        alpha=1,
    )


def show_results_proteins(
    results_path,
):
    accuracies = list()
    with open(results_path, "rb") as rf:
        for line in rf.readlines():
            line = line.decode().split(";")

            gt = [(float(val)) for val in line[1].split(",")]
            argmax = [(float(val)) for val in line[2].split(",")]

            hits = [int(t / a) for t, a in zip(gt, argmax)]
            accuracies.append(sum(hits) / len(hits))

        plot_B(accuracies, "Proteins accuracy histogram")

    # for values in data.values():
    #     gt = values[0]
    #     argmax = values[1]

    #     hits = [int(t / a) for t, a in zip(gt, argmax)]

    #     accuracies.append(sum(hits) / len(hits))

    # plot_B(accuracies, "Proteins accuracy histogram")
