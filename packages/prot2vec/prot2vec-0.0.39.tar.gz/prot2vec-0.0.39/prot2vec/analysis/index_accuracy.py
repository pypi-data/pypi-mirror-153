import json
from matplotlib import pyplot as plt
import numpy as np

from tensorflow.keras import backend as K
from transformers.modeling_tf_outputs import TFMaskedLMOutput


def extract_results(model, data, mask_position, results: dict):

    predictions = model.predict(data[0])
    if isinstance(predictions, TFMaskedLMOutput):
        predictions = K.softmax(predictions.logits, axis=-1)
    predicted_tokens = K.argmax(predictions, axis=-1)

    for i, prediction in enumerate(predictions):
        predicted_token = int(predicted_tokens[i][mask_position])
        true_token = data[1][i][mask_position]
        soft_predicted = float(
            prediction[mask_position][predicted_token]
        )  # softmax_out
        soft_true = float(prediction[mask_position][true_token])  # softmax_out
        results[mask_position][0].append(soft_predicted)
        results[mask_position][1].append(soft_true)
    return results


def check_lengths(data):
    lengths = list()
    for vec1, _ in data.values():
        lengths.append(len(vec1))
    len_0 = lengths[0]
    for length in lengths:
        if length != len_0:
            raise ValueError("Lengths mismatch")


def show_results(
    results_path,
    show_confidences: bool = True,
    show_norm_confidences: bool = True,
    show_accuracies: bool = True,
    show_diff_from_mean: bool = True,
    show_diff_on_indexes: bool = True,
):
    with open(results_path, "r") as rf:
        results = json.load(rf)

    pred_avgs = list()
    true_avgs = list()

    for i in range(len(list(results.values())[0][0])):
        i_val_pred = [val[0][i] for val in results.values()]
        i_val_true = [val[1][i] for val in results.values()]

        pred_avgs.append(sum(i_val_pred) / len(i_val_pred))
        true_avgs.append(sum(i_val_true) / len(i_val_true))

    ratios_mean = list()
    trues_mean = list()
    preds_mean = list()

    ratios_var = list()
    trues_var = list()
    preds_var = list()

    hits = list()

    trues_diff_avg = list()
    preds_diff_avg = list()

    for _, values in results.items():
        vec_preds, vec_trues = values
        vec_ratios = [v_t / v_p for v_p, v_t in zip(vec_preds, vec_trues)]
        mean_ratio = sum(vec_ratios) / len(vec_ratios)
        mean_true = sum(vec_trues) / len(vec_trues)
        mean_pred = sum(vec_preds) / len(vec_preds)

        ratios_mean.append(mean_ratio)
        trues_mean.append(mean_true)
        preds_mean.append(mean_pred)

        ratios_var.append(
            sum([(v_r - mean_ratio) ** 2 for v_r in vec_ratios]) / len(vec_ratios)
        )
        trues_var.append(
            sum([(v_t - mean_true) ** 2 for v_t in vec_trues]) / len(vec_trues)
        )
        preds_var.append(
            sum([(v_p - mean_pred) ** 2 for v_p in vec_preds]) / len(vec_preds)
        )

        vec_hits = [int(v) for v in vec_ratios]
        hits.append(sum(vec_hits) / len(vec_hits))

        trues_diff = [abs(m - v) for m, v in zip(true_avgs, vec_trues)]
        preds_diff = [abs(m - v) for m, v in zip(pred_avgs, vec_preds)]

        trues_diff_avg.append(sum(trues_diff) / len(trues_diff))
        preds_diff_avg.append(sum(preds_diff) / len(preds_diff))

    if show_confidences:
        plt.rcParams["figure.figsize"] = (30, 5)

        plt.plot(
            np.arange(0, len(ratios_mean)), ratios_mean, color="black", linewidth=2
        )
        plt.plot(np.arange(0, len(preds_mean)), preds_mean, color="blue", linewidth=2)
        plt.plot(np.arange(0, len(trues_mean)), trues_mean, color="red", linewidth=2)

        plt.fill_between(
            np.arange(0, len(ratios_mean)),
            [m - v for m, v in zip(ratios_mean, ratios_var)],
            [m + v for m, v in zip(ratios_mean, ratios_var)],
            color="yellow",
        )
        plt.fill_between(
            np.arange(0, len(preds_mean)),
            [m - v for m, v in zip(preds_mean, preds_var)],
            [m + v for m, v in zip(preds_mean, preds_var)],
            color="orange",
        )
        plt.fill_between(
            np.arange(0, len(trues_mean)),
            [m - v for m, v in zip(trues_mean, trues_var)],
            [m + v for m, v in zip(trues_mean, trues_var)],
            color="green",
        )

        plt.title("averages on indexes")
        plt.xlabel("position in window")
        plt.legend(["ratio", "pred", "true", "var", "var", "var"])
        plt.xticks(np.arange(0, len(ratios_mean), 1))
        plt.grid()
        plt.show()

    norm_true = list()
    norm_pred = list()
    max_true = max(trues_mean)
    max_pred = max(preds_mean)

    if show_norm_confidences:
        for v_t, v_p in zip(trues_mean, preds_mean):
            norm_true.append(v_t / max_true)
            norm_pred.append(v_p / max_pred)

        plt.rcParams["figure.figsize"] = (30, 5)

        plt.plot(np.arange(0, len(norm_pred)), norm_pred, color="blue", linewidth=2)
        plt.plot(np.arange(0, len(norm_true)), norm_true, color="red", linewidth=2)

        plt.title("norm averages on indexes")
        plt.xlabel("position in window")
        plt.legend(["pred", "true"])
        plt.xticks(np.arange(0, len(norm_pred), 1))
        plt.grid()
        plt.show()

    if show_accuracies:
        plt.rcParams["figure.figsize"] = (30, 5)
        plt.bar(np.arange(0, len(hits)), hits, color="black", linewidth=2)
        plt.title("acurracy on indexes")
        plt.xlabel("position in window")
        plt.legend(["accuracy"])
        plt.xticks(np.arange(0, len(hits), 1))
        plt.grid()
        plt.show()

    if show_diff_from_mean:
        plt.rcParams["figure.figsize"] = (30, 5)

        plt.plot(
            np.arange(0, len(preds_diff_avg)), preds_diff_avg, color="blue", linewidth=2
        )
        plt.plot(
            np.arange(0, len(trues_diff_avg)), trues_diff_avg, color="red", linewidth=2
        )

        plt.title(f"differences from mean values")
        plt.xlabel("position in window")
        plt.legend(["pred", "true"])
        plt.xticks(np.arange(0, len(trues_diff_avg), 1))
        plt.grid()
        plt.show()

    if show_diff_on_indexes:
        for key_ref, values_ref in results.items():

            trues_diffs = list()
            pred_diffs = list()
            ratios_diffs = list()

            ref_true = values_ref[1]
            ref_pred = values_ref[0]
            ref_ratio = [t / p for p, t in zip(ref_pred, ref_true)]

            for key, values in results.items():
                vec_preds, vec_trues = values
                vec_ratios = [v_t / v_p for v_p, v_t in zip(vec_preds, vec_trues)]

                # differences
                diff_true_vec = [abs(m - v) for m, v in zip(ref_true, vec_trues)]
                diff_pred_vec = [abs(m - v) for m, v in zip(ref_pred, vec_preds)]
                diff_ratio_vec = [abs(m - v) for m, v in zip(ref_ratio, vec_ratios)]

                trues_diffs.append(sum(diff_true_vec) / len(diff_true_vec))
                pred_diffs.append(sum(diff_pred_vec) / len(diff_pred_vec))
                ratios_diffs.append(sum(diff_ratio_vec) / len(diff_ratio_vec))

            plt.rcParams["figure.figsize"] = (30, 5)

            plt.plot(
                np.arange(0, len(ratios_diffs)),
                ratios_diffs,
                color="black",
                linewidth=2,
            )
            plt.plot(
                np.arange(0, len(pred_diffs)), pred_diffs, color="blue", linewidth=2
            )
            plt.plot(
                np.arange(0, len(trues_diffs)), trues_diffs, color="red", linewidth=2
            )

            plt.title(f"averages absolute differences on indexes - {key_ref}")
            plt.xlabel("position in window")
            plt.legend(["ratio", "pred", "true"])
            plt.xticks(np.arange(0, len(norm_pred), 1))
            plt.grid()
            plt.show()
