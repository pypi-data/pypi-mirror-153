import numpy as np
import pandas as pd
from scipy.stats import kstest
from scipy.stats import boxcox


# тест-кейсы на корректность расчётов
class MetricsEstimationTestCases:

    # дополнительная проверка на отсуствие выбросов после бакетирования
    @staticmethod
    def calc_outliers_limits(bucketed_group: pd.DataFrame):
        quartiles = np.percentile(bucketed_group['mu'], [25, 75])
        interquartile_range = quartiles[1] - quartiles[0]
        low_limit = quartiles[0] - 1.5 * interquartile_range
        high_limit = quartiles[1] + 1.5 * interquartile_range
        return low_limit, high_limit

    @staticmethod
    def smooth_outliers(bucketed_group: pd.DataFrame, low_limit, high_limit):
        np.where(bucketed_group['mu'].values < low_limit, low_limit, bucketed_group['mu'].values)
        np.where(bucketed_group['mu'].values > high_limit, high_limit, bucketed_group['mu'].values)

        return

    # дополнительная проверка на нормальность распределения после бакетирования
    @staticmethod
    def get_normal_distribution_report(bucketed_group: pd.DataFrame) -> float:
        ks, p_value_norm = kstest(bucketed_group['mu'], 'norm')

        return p_value_norm

    # преобразование к нормальному распределению, если p-значение проверки на нормальность меньше трэшхолда
    @staticmethod
    def transform_to_normal_distribution(bucketed_group: pd.DataFrame, p_value_norm: float,
                                         p_value_threshold: float) -> pd.DataFrame:
        if p_value_norm < p_value_threshold:
            bucketed_group['mu'] = boxcox(bucketed_group['mu'])[0]
            return bucketed_group

        return bucketed_group
