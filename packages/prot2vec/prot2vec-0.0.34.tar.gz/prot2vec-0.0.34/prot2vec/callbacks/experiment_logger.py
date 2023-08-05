import datetime
import os
import zlib
from pathlib import Path
import os

import pandas as pd
from tensorflow.keras.callbacks import CSVLogger, TensorBoard, Callback, ModelCheckpoint

from ..constants import RESULTS_DIR


def get_logging_callbacks(params, experiment_id, param_id, experiment_name=None, results_path=RESULTS_DIR):
    logger = ExperimentLogger(params, experiment_id, param_id, experiment_name, results_path)
    csv_logger = CSVLogger(logger.path / 'history.tsv', separator='\t', append=True)
    tensorboard = TensorBoard(log_dir=logger.tensorboard_path)

    checkpoint_n = len(os.listdir(logger.checkpoints_path)) + 1
    checkpoint_n = str(checkpoint_n).zfill(5)
    checkpoint_n = f'{checkpoint_n}_checkpoint.h5'

    checkpointer = ModelCheckpoint(
        logger.checkpoints_path / checkpoint_n, monitor='loss', verbose=0, save_best_only=False,
        save_weights_only=True, mode='auto', save_freq='epoch'
    )

    return [logger, csv_logger, tensorboard, checkpointer]


class ExperimentLogger(Callback):
    def __init__(self, params, experiment_id, param_id, experiment_name=None, results_path=RESULTS_DIR):
        super(ExperimentLogger, self).__init__()
        if experiment_name is None:
            raise Exception('Please specify experiment name.')
        results_path = Path(results_path)

        # Attributes init
        self.params = params
        self.experiment_name = experiment_name
        self.params_hash = self.__get_hash_params(params)
        self.history = dict()
        self.time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create directory for the logs
        self.root_path = results_path
        self.path = results_path / '_flat' / experiment_id
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.path = self.path / param_id
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        # self.path = self.path / str(self.params_hash)
        # if not os.path.exists(self.path):
        #     os.makedirs(self.path)
        # self.path = self.path / self.time_stamp
        # if not os.path.exists(self.path):
        #     os.makedirs(self.path)
        if not os.path.exists(self.path / 'models'):
            os.makedirs(self.path / 'models')
        self.model_path = self.path / 'models'
        if not os.path.exists(self.path / 'models' / 'checkpoints'):
            os.makedirs(self.path / 'models' / 'checkpoints')
        self.checkpoints_path = self.path / 'models' / 'checkpoints'
        if not os.path.exists(self.path / 'tensorboard'):
            os.makedirs(self.path / 'tensorboard')
        self.tensorboard_path = self.path / 'tensorboard'
        if not os.path.exists(self.root_path / '_archive'):
            os.makedirs(self.root_path / '_archive')
        self.archive_path = self.root_path / '_archive'

        self.update_result_table()

    def __get_params_string(self, params):
        keys = sorted([str(key) for key in params])
        values = [str(params[key]) for key in keys]
        return ';'.join([':'.join([keys[i], values[i]]) for i in range(len(keys))])

    def __get_hash_params(self, params):
        string_params = self.__get_params_string(params)
        return zlib.adler32(bytes(string_params, 'utf-8'))

    def update_result_table(self):
        results_table = pd.read_csv(self.root_path / 'results.tsv', delimiter='\t', index_col=False)
        results_table.to_csv(self.archive_path / str(self.time_stamp + '_results.tsv.gz'), sep='\t',
                             header=True,
                             index=False, compression='gzip')

        new_row = {
            'Experiment_Name': self.experiment_name,
            'Time_Stamp': self.time_stamp,
            'Params_Hash': self.__get_hash_params(self.params),
            'Params_String': self.__get_params_string(self.params)
        }
        results_table = results_table.append(new_row, ignore_index=True)
        results_table.to_csv(self.root_path / 'results.tsv', sep='\t', header=True, index=False)
