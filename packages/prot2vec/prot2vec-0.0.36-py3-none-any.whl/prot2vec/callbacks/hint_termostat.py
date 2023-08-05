import json
from pathlib import Path

import numpy as np
from tensorflow.keras.callbacks import Callback


class HintTermostat(Callback):
    def __init__(self, tokenizer_path, target_value, log_path, init_step=0, verbose=False, target_variable='loss',
                 is_min_problem=True):
        super(HintTermostat, self).__init__()
        self.levels = np.abs(np.load(Path(tokenizer_path) / 'termostat.npy'))
        with open(Path(tokenizer_path) / 'hints.json', 'r', encoding='utf-8') as fr:
            self.hints = json.load(fr)
        self.level_num = init_step
        self.target_value = target_value
        self.log_path = Path(log_path)
        self.verbose = verbose
        self.target_variable = target_variable

        # True if the objective is minimizing the target value, False if objective is maximizing the target value
        self.is_min_problem = is_min_problem
        if is_min_problem:
            self.target_value *= -1

    def get_distribution(self):
        return self.levels[self.level_num]

    def on_epoch_end(self, epoch, logs=None):
        actual_value = logs[self.target_variable]
        if not self.is_min_problem:
            actual_value *= -1
        if actual_value < self.target_value:
            self.level_num += 1
        else:
            self.level_num -= 1

        # Saturate by range of values
        self.level_num = max(self.level_num, 0)
        self.level_num = min(self.level_num, self.levels.shape[0])
        if self.verbose:
            print(f'Level: {self.level_num}/{self.levels.shape[0]}')
        with open(self.log_path / 'levels.txt', 'a', encoding='utf-8') as fw:
            print(f'{self.level_num}', file=fw)
