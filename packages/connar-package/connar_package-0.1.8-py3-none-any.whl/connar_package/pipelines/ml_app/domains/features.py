import pandas as pd
import numpy as np
import moosir_feature.transformers.indicators.contexts as ind_cntx

import moosir_feature.transformers.tsfresh_features.feature_manager as tsfresh_fm
from moosir_feature.transformers.indicators.tech_indicators import SmaOperator
from moosir_feature.transformers.managers.feature_manager import FeatureCreatorManager
import moosir_feature.transformers.features_common.calculator as f_common

from moosir_feature.transformers.managers.settings import IndicatorTargetSettings, IndicatorFeatureSettings, \
    TargetSettings

OHLC_COLS = ["Open", "High", "Low", "Close"]


def core_create_features(instances: pd.DataFrame,
                         feature_ind_params: dict,
                         moving_average_dist_params: dict
                                 ):

    target_settings = TargetSettings()
    feature_ind_settings = [IndicatorFeatureSettings(**feature_ind_params)]
    lag_ind_settings = []

    fc_mgr = FeatureCreatorManager(target_settings=target_settings,
                                   feature_settings_list=feature_ind_settings,
                                   lag_settings_list=lag_ind_settings)

    features, _ = fc_mgr.create_features(instances=instances)
    features = _create_additional_features(features=features, moving_average_dist_params=moving_average_dist_params)
    return features


def _create_additional_features(features: pd.DataFrame, moving_average_dist_params: dict):
    moving_average_dist_settings = MovingAverageDistSettings(**moving_average_dist_params)
    # todo: hard coded ma_period, win_len hard coded
    result = create_moving_average_dist_feature(features=features,
                                                ma_period=moving_average_dist_settings.ma_period,
                                                win_len=moving_average_dist_settings.win_len)

    features = f_common.combine_features([features, result])
    features = np.log10(1 + features).fillna(0)
    return features


def core_create_features_targets(instances: pd.DataFrame,
                                 target_ind_params: dict,
                                 feature_ind_params: dict,
                                 moving_average_dist_params: dict
                                 ):
    target_settings = IndicatorTargetSettings(**target_ind_params)
    feature_ind_settings = [IndicatorFeatureSettings(**feature_ind_params)]

    fc_mgr = FeatureCreatorManager(target_settings=target_settings,
                                   feature_settings_list=feature_ind_settings,
                                   lag_settings_list=[])
    features, targets, _ = fc_mgr.create_features_and_targets(instances=instances)

    features = _create_additional_features(features=features,
                                           moving_average_dist_params=moving_average_dist_params)

    targets = targets + 1
    features, targets, _ = f_common.align_features_and_targets(features=features, targets=targets)

    return dict(features=features, targets=targets)


class MovingAverageDistSettings:
    def __init__(self,
                 ma_period: int,
                 win_len: int):
        self.win_len = win_len
        self.ma_period = ma_period


def create_moving_average_dist_feature(features: pd.DataFrame,
                                       ma_period: int,
                                       win_len: int,
                                       ):
    ohlc = features[OHLC_COLS]

    # result = ind_fm.calculate_lags(ohlc=ohlc, win_lens=[win_len], lag_lens=lags, feature_names=[SmaOperator.__name__])

    context = ind_cntx.Context()
    ma_cols = context.get_column_names(
        period=ma_period,
        operator=SmaOperator,
    )
    result_ma = features[ma_cols]

    ma_col = result_ma.columns[0]
    assert len(result_ma.columns) == 1, "multiple moving average result"

    # todo: memory exception if not doing it
    result_ma = result_ma.astype("float32")

    result_ts = tsfresh_fm.calculate_features(ohlc=result_ma,
                                              feature_names=["linear_trend_timewise"],
                                              win_lens=[win_len],
                                              apply_col_name=ma_col)

    # todo: shame
    # result = result.filter(like="Sma").dropna()
    result_ts = pd.concat([result_ts.filter(like="Trend-Slope"), result_ts.filter(like="Trend-Stderr")], axis=1)
    assert len(result_ts.columns) == 2, "Cant have more than two cols"
    result_ts.columns = [f"{ma_col}_{c}" for c in result_ts.columns]
    # result_ts = result_ts[["Trend-Slope", "Trend-Stderr"]].dropna()

    aligned = result_ma.join(ohlc[["Close"]], how='inner')
    distances = (aligned[ma_col] - aligned["Close"])
    aligned[f"{ma_col}_Dist-Mean-{win_len}"] = distances.rolling(win_len).mean()
    aligned[f"{ma_col}_Dist-Var-{win_len}"] = distances.rolling(win_len).std()
    aligned[f"{ma_col}_Dist-Sum-{win_len}"] = distances.rolling(win_len).sum()

    result = f_common.combine_features([aligned, result_ma, result_ts])

    _ = result.pop(ma_col)
    _ = result.pop("Close")
    result = result.dropna()

    # todo: not sure why weights in tensor model becomes float32!!
    result = result.astype("float32")

    return result
