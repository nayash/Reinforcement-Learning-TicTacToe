#
# Dataset = GE Stock
# Grid search

import numpy as np
import pandas as pd
import os
import sys
import time
import pandas as pd
from tqdm import tqdm
import pickle
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
import keras
from keras.callbacks import Callback
from keras import optimizers
from keras.wrappers.scikit_learn import KerasClassifier
from keras.callbacks import CSVLogger
from sklearn.model_selection import GridSearchCV
# import psutil
from sklearn.preprocessing import MinMaxScaler, normalize
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

import logging
import itertools as it

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
logging.getLogger("tensorflow").setLevel(logging.ERROR)

from keras import backend as K

print("checking if GPU available", K.tensorflow_backend._get_available_gpus())

LOG_PATH = "./outputs"
LOG_FILE_NAME_PREFIX = "stock_pred_lstm_"
LOG_FILE_NAME_SUFFIX = ".log"

TIME_STEPS = 90  # 3 months
BATCH_SIZE = 20
stime = time.time()


def print_time(text, stime):
    seconds = (time.time() - stime)
    print(text + " " + str(seconds // 60) + " minutes : " + str(np.round(seconds % 60)) + " seconds")


def get_readable_ctime():
    return time.strftime("%d-%m-%Y %H_%M_%S")


def init_logging():
    logging.basicConfig(level=logging.INFO)
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    root_logger = logging.getLogger()

    file_handler = logging.FileHandler("{0}/{1}.log".format(LOG_PATH, LOG_FILE_NAME_PREFIX + get_readable_ctime()))
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)


def trim_dataset(mat, batch_size):
    """
    trims dataset to a size that's divisible by BATCH_SIZE
    """
    no_of_rows_drop = mat.shape[0] % batch_size
    if no_of_rows_drop > 0:
        return mat[:-no_of_rows_drop]
    else:
        return mat


def process_dataframe(df):
    df["change_value"] = df["Close"] - df["Close"].shift(-1)
    df["change_class"] = df["change_value"] < 0  # means price increased
    df.replace(True, 1, inplace=True)
    df.replace(False, 0, inplace=True)
    df["change_class"] = df["change_class"].astype(int)
    # print("processed0 {}",str(df_msft.isnull().sum()))
    df["change_value"] = df["change_value"].dropna()
    # print("processed1",str(df_msft.isnull().sum()))
    return df


def build_timeseries(mat, y_col_index, time_steps):
    # total number of time-series samples would be len(mat) - TIME_STEPS

    dim_0 = mat.shape[0] - time_steps
    dim_1 = mat.shape[1]
    x = np.zeros((dim_0, time_steps, dim_1))
    y = np.zeros((x.shape[0],))

    for i in tqdm(range(dim_0)):
        x[i] = mat[i:time_steps + i]
        y[i] = mat[time_steps + i, y_col_index]
    print("length of time-series i/o {} {}".format(x.shape, y.shape))
    return x, y


stime = time.time()
init_logging()
print(str(os.listdir("./")))  # ge.us.txt
df_ge = pd.read_csv("./ge.us.txt", engine='python')
print(str(df_ge.shape))
print(str(df_ge.columns))

train_cols = ["Open", "High", "Low", "Close", "Volume"]
df_train, df_test = train_test_split(df_ge, train_size=0.8, test_size=0.2, shuffle=False)
print("Train--Test size {} {}".format(len(df_train), len(df_test)))

# scale the feature MinMax, build array
mat = df_ge.loc[:, train_cols].values

# y = df_train.loc[:,"Close"].values
# min_max_scaler = MinMaxScaler()
# x_train = min_max_scaler.fit_transform(x)
# x_test = min_max_scaler.transform(df_test.loc[:,train_cols])

print("Deleting unused dataframes of total size(KB) {}"
      .format((sys.getsizeof(df_ge) + sys.getsizeof(df_train) + sys.getsizeof(df_test)) // 1024))

del df_ge
del df_test
del df_train

csv_logger = CSVLogger('./outputs/training_' + 'log_' + get_readable_ctime() + '.log', append=True)


class LogMetrics(Callback):

    def __init__(self, search_params, param, comb_no):
        self.param = param
        self.self_params = search_params
        self.comb_no = comb_no

    def on_epoch_end(self, epoch, logs):
        for i, key in enumerate(self.self_params.keys()):
            logs[key] = self.param[i]
        logs["combination_number"] = self.comb_no


search_params = {
    "batch_size": [20, 30, 40],
    "time_steps": [30, 60, 90],
    "lr": [0.01, 0.001, 0.0001],
    "epochs": [30, 50, 70]
    # "optimizer": ["SGD", "RMSProp"]
}


# search_params = {
#     "batch_size": [10],
#     "time_steps": [30],
#     "lr": [0.01],
#     "epochs": [50]
#     # "optimizer": ["SGD", "RMSProp"]
# }

def eval_model(mat, params, comb_no):
    global search_params

    BATCH_SIZE = params[0]
    TIME_STEPS = params[1]

    x_train, x_test = train_test_split(mat, train_size=0.8, test_size=0.2, shuffle=False)

    # scale the train and test dataset
    min_max_scaler = MinMaxScaler()
    x_train = min_max_scaler.fit_transform(x_train)
    x_test = min_max_scaler.transform(x_test)

    x_train_ts, y_train_ts = build_timeseries(x_train, 3, TIME_STEPS)
    x_test_ts, y_test_ts = build_timeseries(x_test, 3, TIME_STEPS)
    x_train_ts = trim_dataset(x_train_ts, BATCH_SIZE)
    y_train_ts = trim_dataset(y_train_ts, BATCH_SIZE)
    print("Train size(trimmed) {}, {}".format(x_train_ts.shape, y_train_ts.shape))
    print("{},{}".format(x_train[TIME_STEPS - 1, 3], y_train_ts[0]))
    print(str(x_train[TIME_STEPS, 3]), str(y_train_ts[1]))
    print(str(x_train[TIME_STEPS + 1, 3]), str(y_train_ts[2]))
    print(str(x_train[TIME_STEPS + 2, 3]), str(y_train_ts[3]))
    print(str(x_train[TIME_STEPS + 3, 3]), str(y_train_ts[4]))
    print(str(x_train[TIME_STEPS + 4, 3]), str(y_train_ts[5]))
    print(str(x_train[TIME_STEPS + 5, 3]), str(y_train_ts[6]))
    x_test_ts = trim_dataset(x_test_ts, BATCH_SIZE)
    y_test_ts = trim_dataset(y_test_ts, BATCH_SIZE)
    print("Test size(trimmed) {}, {}".format(x_test_ts.shape, y_test_ts.shape))

    print("Are any NaNs present in train/test matrices?{0},{1}".format(str(np.isnan(x_train).any()),
                                                                       str(np.isnan(x_test).any())))

    lstm_model = Sequential()
    # (batch_size, timesteps, data_dim)
    lstm_model.add(LSTM(100, batch_input_shape=(BATCH_SIZE, TIME_STEPS, x_train_ts.shape[2]), dropout=0.2,
                        recurrent_dropout=0.2, stateful=True, return_sequences=True,
                        kernel_initializer='random_uniform'))
    # ,return_sequences=True #LSTM params => dropout=0.2, recurrent_dropout=0.2
    lstm_model.add(LSTM(60, dropout=0.2))
    lstm_model.add(Dense(20, activation='relu'))
    lstm_model.add(Dense(1, activation='sigmoid'))
    optimizer = optimizers.RMSprop(lr=params[2])
    # optimizer = optimizers.SGD(lr=params[2], decay=1e-6, momentum=0.9, nesterov=True)
    lstm_model.compile(loss='mean_squared_error', optimizer=optimizer)  # binary_crossentropy
    history = lstm_model.fit(x_train_ts, y_train_ts, epochs=params[3], verbose=2, batch_size=BATCH_SIZE,
                             validation_data=[x_test_ts, y_test_ts],
                             callbacks=[LogMetrics(search_params, params, comb_no), csv_logger])
    # for key in history.history.keys():
    #     print(key, "--",history.history[key])
    return history, lstm_model


def get_all_combinations(params):
    all_names = params.keys()
    combinations = it.product(*(params[Name] for Name in all_names))
    return list(combinations)


def run_search(mat, params):
    param_combs = get_all_combinations(params)  # list of tuples
    logging.info("Total combinations to try = {}".format(len(param_combs)))
    for i, combination in enumerate(param_combs):
        logging.info("Trying combo no. {} {}".format(i, combination))
        eval_model(mat, combination, i)


run_search(mat, search_params)

print_time("program completed in", stime)

