import pandas as pd
import numpy as np
import logging

from moosir_feature.model_validations.basic_parameter_searcher import ParameterSearcher
from moosir_feature.model_validations.benchmarking import NaiveModel, run_benchmarking
from moosir_feature.model_validations.model_validator import CustomTsCv
from moosir_feature.model_validations.model_cv_runner import predict_on_cv
from moosir_feature.trades.alpha_manager import create_quantile_alphas

from .domains.models import LarryConnarModel

from .domains.features import core_create_features_targets, core_create_features

log = logging.getLogger(__name__)


def create_features_targets(instances: pd.DataFrame,
                            target_ind_params: dict,
                            feature_ind_params: dict,
                            moving_average_dist_params: dict
                            ):
    result = core_create_features_targets(instances=instances,
                                          feature_ind_params=feature_ind_params,
                                          target_ind_params=target_ind_params,
                                          moving_average_dist_params=moving_average_dist_params)

    return result


def run_cross_validation(features: pd.DataFrame,
                         targets: pd.DataFrame,
                         cv_search_params: dict,
                         search_params: dict,
                         metrics: list
                         ):
    log.info("searching parameters and running cross validation")

    searcher = ParameterSearcher()
    estimator = LarryConnarModel(rsi_col="Ind-Rsi-30",
                                 moving_average_cols=["Ind-Sma-200"])

    search_result = searcher.run_parameter_search_multiple_cvs(X=features,
                                                               y=targets,
                                                               estimator=estimator,
                                                               cv_params=cv_search_params,
                                                               param_grid=search_params,
                                                               metrics=metrics,
                                                               )

    return dict(search_result=search_result)


def benchmark_best_model(features: pd.DataFrame,
                         targets: pd.DataFrame,
                         best_params: dict,
                         benchmark_cv_params: dict,
                         metrics: list
                         ):
    best_model = LarryConnarModel(**best_params)

    models = [best_model, NaiveModel(targets=targets.copy(), look_back_len=12)]

    cv = CustomTsCv(train_n=benchmark_cv_params["train_length"],
                    test_n=benchmark_cv_params["test_length"],
                    sample_n=len(features),
                    train_shuffle_block_size=benchmark_cv_params["train_shuffle_block_size"])

    benchmark_result = run_benchmarking(models=models, targets=targets, features=features, cv=cv, metrics=metrics)

    return dict(benchmark_result=benchmark_result)


def train_predict_best_params(instances: pd.DataFrame,
                              target_ind_params: dict,
                              feature_ind_params: dict,
                              moving_average_dist_params: dict,

                              # lag_ind_params: dict,
                              best_params: dict,
                              benchmark_cv_params: dict):
    features_targets = core_create_features_targets(instances=instances,
                                                    feature_ind_params=feature_ind_params,
                                                    target_ind_params=target_ind_params,
                                                    moving_average_dist_params=moving_average_dist_params)

    features = features_targets["features"]
    targets = features_targets["targets"]

    best_model = LarryConnarModel(**best_params)
    cv = CustomTsCv(train_n=benchmark_cv_params["train_length"],
                    test_n=benchmark_cv_params["test_length"],
                    sample_n=len(features),
                    train_shuffle_block_size=None)

    prediction_result = predict_on_cv(model=best_model, features=features, targets=targets, cv=cv)

    return dict(prediction_result=prediction_result)


def create_alpha(instances: pd.DataFrame, prediction_result: pd.DataFrame, alpha_threashold: float):
    # alphas = create_absolute_prediction_alphas(instances=instances, prediction_result=prediction_result)
    alphas = create_quantile_alphas(instances=instances,
                                    quantile_threshold=alpha_threashold,
                                    prediction_result=prediction_result)

    log.info(alphas)
    log.info(alphas.describe())

    return dict(alphas=alphas)


def train_best_model_to_deploy(instances: pd.DataFrame,
                               target_ind_params: dict,
                               feature_ind_params: dict,
                               moving_average_dist_params: dict,
                               best_params,
                               final_train_len: int):
    instances = instances.iloc[-final_train_len:]

    features_targets = core_create_features_targets(instances=instances,
                                                    feature_ind_params=feature_ind_params,
                                                    target_ind_params=target_ind_params,
                                                    moving_average_dist_params=moving_average_dist_params)

    features = features_targets["features"]
    targets = features_targets["targets"]

    best_model = LarryConnarModel(**best_params)

    best_model.fit(features, targets)

    best_model_tensor = best_model.model
    best_model.model = None

    return dict(best_model_tensor=best_model_tensor, best_model=best_model)


def inference_model(instances: pd.DataFrame,
                    best_model: LarryConnarModel,
                    best_model_tensor,
                    feature_ind_params,
                    moving_average_dist_params: dict,
                    ):

    features = core_create_features(instances=instances,
                                    moving_average_dist_params=moving_average_dist_params,
                                    feature_ind_params=feature_ind_params)

    if len(features) == 0:
        log.warning(f"features empty, likely instances too small. instances len: {len(instances)}")
        return []

    best_model.model = best_model_tensor
    preds = best_model.predict(features)

    # prediction_result = pd.DataFrame(data={"preds": preds}, index=features.index)
    prediction_result = preds
    prediction_result.columns = ["preds"]

    return prediction_result
