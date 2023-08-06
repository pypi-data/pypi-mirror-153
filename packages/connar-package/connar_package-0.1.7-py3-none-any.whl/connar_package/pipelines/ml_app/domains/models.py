import numpy as np
import pandas as pd
from moosir_feature.model_validations.metrics import get_any_metric, binary_returns_avg_metric_fn
from sklearn.base import RegressorMixin

import tensorflow as tf
from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras import callbacks

from sklearn.preprocessing import MinMaxScaler

# from keras import backend as K
import tensorflow.keras.backend as K

# todo: not sure, but for debug stuff needed
# tf.config.run_functions_eagerly(True)


# @tf.autograph.experimental.do_not_convert
# def custom_loss(y_true, y_pred):
#     # extract the "next day's price" of tensor
#     y_true_next = y_true[1:]
#     y_pred_next = y_pred[1:]
#
#     # extract the "today's price" of tensor
#     y_true_tdy = y_true[:-1]
#     y_pred_tdy = y_pred[:-1]
#
#     print('Shape of y_pred_back -', y_pred_tdy.get_shape())
#
#     # substract to get up/down movement of the two tensors
#     y_true_diff = tf.subtract(y_true_next, y_true_tdy)
#     y_pred_diff = tf.subtract(y_pred_next, y_pred_tdy)
#
#     # create a standard tensor with zero value for comparison
#     standard = tf.zeros_like(y_pred_diff)
#
#     # compare with the standard; if true, UP; else DOWN
#     y_true_move = tf.greater_equal(y_true_diff, standard)
#     y_pred_move = tf.greater_equal(y_pred_diff, standard)
#     y_true_move = tf.reshape(y_true_move, [-1])
#     y_pred_move = tf.reshape(y_pred_move, [-1])
#
#     # find indices where the directions are not the same
#     condition = tf.not_equal(y_true_move, y_pred_move)
#     indices = tf.where(condition)
#
#     # move one position later
#     ones = tf.ones_like(indices)
#     indices = tf.add(indices, ones)
#     indices = K.cast(indices, dtype='int32')
#
#     # create a tensor to store directional loss and put it into custom loss output
#     direction_loss = tf.Variable(tf.ones_like(y_pred), dtype='float32')
#     updates = K.cast(tf.ones_like(indices), dtype='float32')
#     alpha = 1000
#     direction_loss = tf.tensor_scatter_nd_update(direction_loss, indices, alpha * updates)
#
#     custom_loss = K.mean(tf.multiply(K.square(y_true - y_pred), direction_loss), axis=-1)
#
#     return custom_loss

# def correlation_coefficient_loss(y_true, y_pred):
#     x = y_true
#     y = y_pred
#     mx = K.mean(x)
#     my = K.mean(y)
#     xm, ym = x-mx, y-my
#     r_num = K.sum(tf.multiply(xm,ym))
#     r_den = K.sqrt(tf.multiply(K.sum(K.square(xm)), K.sum(K.square(ym))))
#     r = r_num / r_den
#
#     r = K.maximum(K.minimum(r, 1.0), -1.0)
#     return 1 - K.square(r)

class LarryConnarModel(RegressorMixin):
    def __init__(self, rsi_col: str, moving_average_cols: list, ):
        self.moving_average_cols = moving_average_cols
        self.rsi_col = rsi_col
        self.model = None
        self.scaler = MinMaxScaler()

    def _get_features(self, data):
        feature_cols = self.moving_average_cols + [self.rsi_col]
        features = data.filter(feature_cols, axis=1)
        assert features.shape[1] == len(feature_cols), f"input data missing some columns:  {set(feature_cols) - set(data.columns)} "
        return features

    def fit(self, X=None, y=None):
        features = self._get_features(data=X)
        feature_n = features.shape[1]
        sample_n = features.shape[0]

        model = Sequential(name="LarryConnarModel")  # Model
        # model.add(InputLayer(input_shape=(feature_n,)))  # Input Layer - need to speicfy the shape of inputs
        model.add(Dense(10 * feature_n, input_shape=(feature_n,), activation='relu'))  # Hidden Layer, softplus(x) = log(exp(x) + 1)
        # model.add(Dense(5 * feature_n, activation='relu'))  # Hidden Layer, softplus(x) = log(exp(x) + 1)
        model.add(Dense(feature_n, activation='relu'))  # Hidden Layer, softplus(x) = log(exp(x) + 1)
        model.add(Dense(1, activation='linear'))  # Output Layer, sigmoid(x) = 1 / (1 + exp(-x))

        earlystopping = callbacks.EarlyStopping(monitor="val_loss",
                                                mode="min",
                                                min_delta=0.00001,
                                                patience=5,
                                                restore_best_weights=True)

        ##### Step 4 - Compile keras model
        model.compile(optimizer='adam',  # default='rmsprop', an algorithm to be used in backpropagation
                      loss='mean_squared_error'
                      # custom_loss #correlation_coefficient_loss #'mean_squared_error', #  ‘mean_squared_logarithmic_error‘
                      # Loss function to be optimized. A string (name of loss function), or a tf.keras.losses.Loss instance.
                      # metrics=['Accuracy', 'Precision', 'Recall'],
                      # # List of metrics to be evaluated by the model during training and testing. Each of this can be a string (name of a built-in function), function or a tf.keras.metrics.Metric instance.
                      # loss_weights=None,
                      # # default=None, Optional list or dictionary specifying scalar coefficients (Python floats) to weight the loss contributions of different model outputs.
                      # weighted_metrics=None,
                      # # default=None, List of metrics to be evaluated and weighted by sample_weight or class_weight during training and testing.
                      # run_eagerly=None,
                      # # Defaults to False. If True, this Model's logic will not be wrapped in a tf.function. Recommended to leave this as None unless your Model cannot be run inside a tf.function.
                      # steps_per_execution=None
                      # # Defaults to 1. The number of batches to run during each tf.function call. Running multiple batches inside a single tf.function call can greatly improve performance on TPUs or small models with a large Python overhead.
                      )

        X_raw = np.array(features)
        X_tf = self.scaler.fit_transform(X=X_raw)

        history = model.fit(X_tf,  # input data
                            y,  # target data
                            batch_size=int(sample_n * 0.05),
                            # Number of samples per gradient update. If unspecified, batch_size will default to 32.
                            epochs=100,

                            callbacks=[earlystopping],

                            # default=1, Number of epochs to train the model. An epoch is an iteration over the entire x and y data provided
                            # verbose='auto',
                            # default='auto', ('auto', 0, 1, or 2). Verbosity mode. 0 = silent, 1 = progress bar, 2 = one line per epoch. 'auto' defaults to 1 for most cases, but 2 when used with ParameterServerStrategy.
                            # callbacks=None,  # default=None, list of callbacks to apply during training. See tf.keras.callbacks
                            validation_split=0.2,
                            # default=0.0, Fraction of the training data to be used as validation data. The model will set apart this fraction of the training data, will not train on it, and will evaluate the loss and any model metrics on this data at the end of each epoch.
                            # validation_data=(X_test, y_test), # default=None, Data on which to evaluate the loss and any model metrics at the end of each epoch.
                            shuffle=True,
                            # default=True, Boolean (whether to shuffle the training data before each epoch) or str (for 'batch').
                            # class_weight={0: 0.3, 1: 0.7},
                            # default=None, Optional dictionary mapping class indices (integers) to a weight (float) value, used for weighting the loss function (during training only). This can be useful to tell the model to "pay more attention" to samples from an under-represented class.
                            # sample_weight=None,
                            # default=None, Optional Numpy array of weights for the training samples, used for weighting the loss function (during training only).
                            # initial_epoch=0,
                            # Integer, default=0, Epoch at which to start training (useful for resuming a previous training run).
                            # steps_per_epoch=None,
                            # Integer or None, default=None, Total number of steps (batches of samples) before declaring one epoch finished and starting the next epoch. When training with input tensors such as TensorFlow data tensors, the default None is equal to the number of samples in your dataset divided by the batch size, or 1 if that cannot be determined.
                            # validation_steps=None,
                            # Only relevant if validation_data is provided and is a tf.data dataset. Total number of steps (batches of samples) to draw before stopping when performing validation at the end of every epoch.
                            # validation_batch_size=None,
                            # Integer or None, default=None, Number of samples per validation batch. If unspecified, will default to batch_size.
                            # validation_freq=3,
                            # default=1, Only relevant if validation data is provided. If an integer, specifies how many training epochs to run before a new validation run is performed, e.g. validation_freq=2 runs validation every 2 epochs.
                            # max_queue_size=10,
                            # default=10, Used for generator or keras.utils.Sequence input only. Maximum size for the generator queue. If unspecified, max_queue_size will default to 10.
                            # workers=1,
                            # default=1, Used for generator or keras.utils.Sequence input only. Maximum number of processes to spin up when using process-based threading. If unspecified, workers will default to 1.
                            # use_multiprocessing=False,
                            # default=False, Used for generator or keras.utils.Sequence input only. If True, use process-based threading. If unspecified, use_multiprocessing will default to False.
                            )

        # print(model.summary())
        # result = model.predict(X_tf)
        # hist = pd.DataFrame(history.history)
        # print("End ------")
        self.model = model

    def predict(self, X: pd.DataFrame):
        features = self._get_features(data=X)
        X_tf = self.scaler.transform(np.array(features))
        K.clear_session()
        preds = self.model.predict(X_tf)
        result = pd.DataFrame(data=preds, index=X.index)

        return result

    def get_params(self, deep=False):
        return {'rsi_col': self.rsi_col,
                'moving_average_cols': self.moving_average_cols,
                }

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self


##########################################
#
#########################################
algorithm_parameters = {'max_num_iteration': None,
                        'population_size': 100,
                        'mutation_probability': 0.1,
                        'elit_ratio': 0.01,
                        'crossover_probability': 0.5,
                        'parents_portion': 0.3,
                        'crossover_type': 'uniform',
                        'max_iteration_without_improv': None}
convergence_curve = True


class LarryConnarModel2(RegressorMixin):
    def __init__(self, rsi_col: str, moving_average_col: str, ):
        self.moving_average_col = moving_average_col
        self.rsi_col = rsi_col
        self.rsi_threshold = 40.0
        self.ma_threshold = 0.0

    def fit(self, X=None, y=None):
        def f(X_params):
            # print(X)
            rsi_threshold = X_params[0]
            ma_threshold = X_params[1]

            # predict X,
            X_temp = X.copy()
            X_temp["_pred"] = 0
            X_temp.loc[(X_temp[self.moving_average_col] > X_temp["Close"] + ma_threshold) & (
                    X_temp[self.rsi_col] < rsi_threshold), "_pred"] = 1

            # score
            score = binary_returns_avg_metric_fn(y_true=y, y_pred=X_temp["_pred"].values.reshape(-1))
            # print(score)

            loss = -1 * score

            # by default the package minimize
            return loss

        rsi_boundary = [40, 50]
        ma_boundary = [0, 200]

        varbound = np.array([rsi_boundary, ma_boundary])

        model = ga(function=f,
                   dimension=2,
                   variable_type='real',
                   variable_boundaries=varbound,
                   algorithm_parameters=algorithm_parameters,
                   convergence_curve=convergence_curve)
        model.run()
        # convergence = model.report
        solution = model.output_dict
        best_vars = solution["variable"]

        self.rsi_threshold = best_vars[0]
        self.ma_threshold = best_vars[1]

        print(solution)
        pass

    def predict(self, X: pd.DataFrame):
        X["_temp"] = 0
        X.loc[(X[self.moving_average_col] > X["Close"] + self.ma_threshold) & (
                X[self.rsi_col] < self.rsi_threshold), "_temp"] = 1

        vals = X["_temp"].values.reshape(-1)
        return vals

    def get_params(self, deep=False):
        return {'rsi_col': self.rsi_col,
                'moving_average_col': self.moving_average_col,
                }

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self
