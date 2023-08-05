import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind
from mlxtend.evaluate import mcnemar
from scipy.stats import chi2
from statsmodels.sandbox.stats.multicomp import multipletests
from typing import List
import os
import json
from .unit_tests import MetricsEstimationTestCases
from .datamart_models import MetricsHandbook


# калькулятор аб теста для независимых и зависимых выборок
# для зависимых выборок не предусмотрена возможность множественных сравнений (более 2-х временных периодов)
# нужен ли effect size для зависимых выборок
class MetricEstimation:

    def __init__(self, data: pd.DataFrame, product_metrics: List[str], ab_test: str, experiment_variant: str,
                 p_value_threshold: float, bucket_size: int, cat_threshold: int,
                 metrics_handbook_path: str, report_name: str):

        self.product_metrics = product_metrics
        self.ab_test = ab_test
        self.experiment_variant = experiment_variant
        self.p_value_threshold = p_value_threshold
        self.n_buckets = int(data.shape[0] / bucket_size)
        self.cat_threshold = cat_threshold
        self.metrics_handbook_path = metrics_handbook_path

        with open(self.metrics_handbook_path) as infile:
            self.handbook = json.load(infile)

        # определение стат.типа метрик
        self._check_new_metrics()
        self._check_old_metrics_in_handbook()

        # рабочий запуск
        control_groups = list(data[self.experiment_variant].unique())

        for group in control_groups[:]:
            if group[0] != 'c':
                control_groups.remove(group)

        n_control_groups = len(control_groups)

        if not os.path.exists('./assets/{ab_test}'.format(ab_test=self.ab_test)):
            os.mkdir('./assets/{ab_test}'.format(ab_test=self.ab_test))

        try:
            assert n_control_groups == 1
            self.data = data
            self._get_independent_ab_test_report().to_csv(
                './assets/{ab_test}/{ab_test}_{report_name}.csv'.format(ab_test=self.ab_test, report_name=report_name),
                encoding='utf-8')
        except AssertionError:
            # считаем только между контролем
            self.data = data.loc[data[self.experiment_variant].isin(control_groups)]
            self._get_independent_ab_test_report().to_csv(
                './assets/{ab_test}/{ab_test}_{report_name}_control_report.csv'.format(ab_test=self.ab_test,
                                                                                       report_name=report_name),
                encoding='utf-8')
            # схлопываем контроль
            mapping_dict = dict(zip(control_groups, ['control' for _ in range(n_control_groups)]))
            self.data[self.experiment_variant].replace(mapping_dict, inplace=True)
            # считаем на всех данных
            test_groups = data.loc[~data[self.experiment_variant].isin(control_groups)]
            self.data = pd.concat([self.data, test_groups], axis=0)
            self._get_independent_ab_test_report().to_csv(
                './assets/{ab_test}/{ab_test}_{report_name}.csv'.format(ab_test=self.ab_test, report_name=report_name),
                encoding='utf-8')

    # отчёт по результатам ab теста и входным данным для независимых выборок
    # отчёт по входным данным нужен для понимания исходных условий, на которых запускается ab тест
    def _get_independent_ab_test_report(self) -> pd.DataFrame:
        test_groups = []
        metrics = self.handbook[MetricsHandbook.numerical] + self.handbook[MetricsHandbook.categorical] + \
                  self.handbook[MetricsHandbook.binary]
        p_values_answers = []
        p_values_answers_corrected = []
        final_answers = []
        lift = []
        effect_size = []

        # итерируемся по группам эксперемента и метрикам, применяя к каждой метрике соотвествующий стат.тест
        groups = list(self.data[self.experiment_variant].unique())
        groups.remove('control')
        group_a = self.data.loc[self.data[self.experiment_variant] == 'control']

        for group in groups:
            group_b = self.data.loc[self.data[self.experiment_variant] == group]
            test_groups.append('control' + '_' + group)

            if len(self.handbook[MetricsHandbook.numerical]) != 0:
                numerical_test_answers = []
                for metric in self.handbook[MetricsHandbook.numerical]:
                    np.random.shuffle(group_a[metric].values)
                    np.random.shuffle(group_b[metric].values)

                    numerical_test_answers.append(
                        self._mean_estimation(group_a=group_a[metric], group_b=group_b[metric]))

                    group_a_mean, group_b_mean, group_a_std, group_b_std = self._calc_numerical_statistics(
                        group_a=group_a[metric], group_b=group_b[metric])
                    lift.append(self._calc_lift(group_a_mean=group_a_mean, group_b_mean=group_b_mean))
                    effect_size.append(self._calc_numerical_binomial_effect_size(group_a_mean=group_a_mean,
                                                                                 group_b_mean=group_b_mean,
                                                                                 group_a_std=group_a_std,
                                                                                 group_b_std=group_b_std))

                p_values_answers.extend(numerical_test_answers)

            if len(self.handbook[MetricsHandbook.categorical]) != 0:
                categorical_test_answers = []
                for metric in self.handbook[MetricsHandbook.categorical]:
                    np.random.shuffle(group_a[metric].values)
                    np.random.shuffle(group_b[metric].values)

                    categorical_test_answers.append(
                        self._chi_square_test(group_a=group_a, group_b=group_b, metric=metric))

                    rank_a_sum, rank_b_sum, group_a_dim, group_b_dim, group_a_mean, group_b_mean = \
                        self._calc_categorical_statistics(group_a=group_a, group_b=group_b)
                    lift.append(self._calc_lift(group_a_mean=group_a_mean, group_b_mean=group_b_mean))
                    effect_size.append(self._calc_categorical_effect_size(rank_a_sum=rank_a_sum, rank_b_sum=rank_b_sum,
                                                                          group_a_dim=group_a_dim,
                                                                          group_b_dim=group_b_dim))

                p_values_answers.extend(categorical_test_answers)

            if len(self.handbook[MetricsHandbook.binary]) != 0:
                binary_test_answers = []
                for metric in self.handbook[MetricsHandbook.binary]:
                    np.random.shuffle(group_a[metric].values)
                    np.random.shuffle(group_b[metric].values)

                    binary_test_answers.append(self._chi_square_test(group_a=group_a, group_b=group_b, metric=metric))

                    group_a_mean, group_b_mean, group_a_std, group_b_std = self._calc_binary_statistics(group_a=group_a,
                                                                                                        group_b=group_b)
                    lift.append(self._calc_lift(group_a_mean=group_a_mean, group_b_mean=group_b_mean))
                    effect_size.append(self._calc_numerical_binomial_effect_size(group_a_mean=group_a_mean,
                                                                                 group_b_mean=group_b_mean,
                                                                                 group_a_std=group_a_std,
                                                                                 group_b_std=group_b_std))
                p_values_answers.extend(binary_test_answers)

        # делаем итоговый отчёт
        p_values_answers_corrected.extend(self._get_multiple_comparisons_correction(n_groups=len(groups),
                                                                                    p_value_answers=p_values_answers))
        final_answers.extend(self._get_stat_significance_answers(p_value_answers=p_values_answers_corrected))

        independent_stat_significance_report = self._make_frame_report(groups=test_groups,
                                                                       p_values_answers=p_values_answers_corrected,
                                                                       answers=final_answers,
                                                                       metrics=metrics, lift=lift,
                                                                       effect_size=effect_size)

        return independent_stat_significance_report

    # тест для сравнения пропорций в группах
    def _chi_square_test(self, group_a: pd.DataFrame, group_b: pd.DataFrame, metric: str):
        table = pd.concat([group_a[[self.experiment_variant, metric]],
                           group_b[[self.experiment_variant, metric]]], axis=0)
        contingency_table = pd.crosstab(table[self.experiment_variant], table[metric], normalize='index')
        chi2, p_value, dof, ex = chi2_contingency(contingency_table)

        return p_value

    # оценка вещественной фичи
    def _mean_estimation(self, group_a: pd.DataFrame, group_b: pd.DataFrame) -> float:
        group_a_bucketed, group_b_bucketed = self._get_buckets(group_a, group_b)
        # доп. проверка на выбросы - если они остались, то сглаживаем
        low_limit_a, high_limit_a = MetricsEstimationTestCases.calc_outliers_limits(bucketed_group=group_a_bucketed)
        low_limit_b, high_limit_b = MetricsEstimationTestCases.calc_outliers_limits(bucketed_group=group_b_bucketed)
        MetricsEstimationTestCases.smooth_outliers(bucketed_group=group_a_bucketed, low_limit=low_limit_a,
                                                   high_limit=high_limit_a)
        MetricsEstimationTestCases.smooth_outliers(bucketed_group=group_b_bucketed, low_limit=low_limit_b,
                                                   high_limit=high_limit_b)
        # доп. проверка на нормальность - если всё таки нет, то сглаживаем
        p_value_norm_a = MetricsEstimationTestCases.get_normal_distribution_report(bucketed_group=group_a_bucketed)
        group_a_bucketed = MetricsEstimationTestCases.transform_to_normal_distribution(bucketed_group=group_a_bucketed,
                                                                                       p_value_norm=p_value_norm_a,
                                                                                       p_value_threshold=self.p_value_threshold)
        p_value_norm_b = MetricsEstimationTestCases.get_normal_distribution_report(bucketed_group=group_b_bucketed)
        group_b_bucketed = MetricsEstimationTestCases.transform_to_normal_distribution(bucketed_group=group_b_bucketed,
                                                                                       p_value_norm=p_value_norm_b,
                                                                                       p_value_threshold=self.p_value_threshold)

        stat, p_value = ttest_ind(group_a_bucketed['mu'], group_b_bucketed['mu'])

        return p_value

    # оценка биномиальной фичи на зависимой выборке
    @staticmethod
    def _mcnemar_test(group_a: pd.DataFrame, group_b: pd.DataFrame):
        table = pd.concat([group_a, group_b], axis=1)
        contingency_table = pd.crosstab(table['before'], table['after'])
        stat, p_value = mcnemar(ary=contingency_table, corrected=True)

        return p_value

    # оценка категориальной фичи на зависимой выборке
    @staticmethod
    def _bowker_test(group_a: pd.DataFrame, group_b: pd.DataFrame):
        table = pd.concat([group_a, group_b], axis=1)
        contingency_table = pd.crosstab(table['before'], table['after'])

        k = contingency_table.shape[0]
        upp_idx = np.triu_indices(k, 1)

        tril = contingency_table.T[upp_idx]
        triu = contingency_table[upp_idx]

        stat = ((tril - triu) ** 2 / (tril + triu + 1e-20)).sum()
        ddof = k * (k - 1) / 2.
        p_value = chi2.sf(stat, ddof)

        return p_value

    # бакетирование для приведения распределения к нормальному
    # количество наблюдений кратно количеству бакетов для минимизации риска выбросов
    def _get_buckets(self, group_a: pd.DataFrame, group_b: pd.DataFrame):
        group_a_dimension = (group_a.shape[0] // self.n_buckets) * self.n_buckets
        group_b_dimension = (group_b.shape[0] // self.n_buckets) * self.n_buckets

        group_a = group_a.head(group_a_dimension)
        group_b = group_b.head(group_b_dimension)

        size_a = group_a.shape[0]
        size_b = group_b.shape[0]

        group_a_bucketed = pd.DataFrame({'values': group_a.values,
                                         'bucket_a': [i for i in range(self.n_buckets)] * int(size_a / self.n_buckets)}) \
            .groupby('bucket_a')['values'].agg(mu=np.mean).reset_index()

        group_b_bucketed = pd.DataFrame({'values': group_b.values,
                                         'bucket_b': [i for i in range(self.n_buckets)] * int(size_b / self.n_buckets)}) \
            .groupby('bucket_b')['values'].agg(mu=np.mean).reset_index()

        return group_a_bucketed, group_b_bucketed

    # получение ответов по статзначимости с проверкой p-значения и необходимости применения множественных сравнений
    def _get_multiple_comparisons_correction(self, n_groups: int, p_value_answers: list) -> list:
        if n_groups > 2:
            return self._apply_multiple_comparisons(p_value_answers=p_value_answers)

        return p_value_answers

    # ответы по p-значениям
    def _get_stat_significance_answers(self, p_value_answers: list) -> List[str]:
        for p_value in range(len(p_value_answers)):
            if p_value_answers[p_value] <= self.p_value_threshold:
                p_value_answers[p_value] = 'Статзначимо'
            else:
                p_value_answers[p_value] = 'Не статзначимо'

        return p_value_answers

    # ответы по множественным сравнениям
    @staticmethod
    def _apply_multiple_comparisons(p_value_answers: list) -> list:
        _, bh_p, _, _ = multipletests(p_value_answers, method='fdr_bh')

        return list(bh_p)

    # расчёт прироста метрики (различия значений метрики между группами в процентах)
    @staticmethod
    def _calc_lift(group_a_mean: float, group_b_mean: float) -> float:
        lift = ((group_a_mean - group_b_mean) / group_b_mean) * 100

        return lift

    # расчёт размера эффекта c учётом дисперсии метрики между группами для вещественной и бинарной фичи
    @staticmethod
    def _calc_numerical_binomial_effect_size(group_a_mean: float, group_b_mean: float,
                                             group_a_std: float, group_b_std: float) -> float:
        effect_size = (group_a_mean - group_b_mean) / ((group_a_std + group_b_std) / 2)

        return effect_size

    @staticmethod
    def _calc_categorical_effect_size(rank_a_sum, rank_b_sum, group_a_dim, group_b_dim) -> float:
        z_score = ((rank_a_sum + 0.5) - ((rank_a_sum + rank_b_sum) / 2)) / np.sqrt(
            (group_a_dim * group_b_dim * (group_a_dim + group_b_dim + 1) / 12))
        effect_size = z_score / np.sqrt(group_a_dim + group_b_dim)

        return effect_size

    # подсчёт средней и std по вещественной метрике
    @staticmethod
    def _calc_numerical_statistics(group_a: pd.DataFrame, group_b: pd.DataFrame):
        group_a_mean = group_a.values.mean()
        group_b_mean = group_b.values.mean()

        group_a_std = group_a.values.std()
        group_b_std = group_b.values.std()

        return group_a_mean, group_b_mean, group_a_std, group_b_std

    # подсчёт средней и дисперсии по бинарной метрике
    @staticmethod
    def _calc_binary_statistics(group_a: pd.DataFrame, group_b: pd.DataFrame):
        size_a = group_a.shape[0]
        size_b = group_b.shape[0]
        proba_a = (group_a.values == 1).sum() / size_a
        proba_b = (group_b.values == 1).sum() / size_b

        group_a_mean = size_a * proba_a
        group_b_mean = size_b * proba_b

        group_a_std = np.sqrt(proba_a * (1 - proba_a))
        group_b_std = np.sqrt(proba_b * (1 - proba_b))

        return group_a_mean, group_b_mean, group_a_std, group_b_std

    @staticmethod
    def _calc_categorical_statistics(group_a: pd.DataFrame, group_b: pd.DataFrame):
        rank_a_sum = np.sum(group_a.values)
        rank_b_sum = np.sum(group_b.values)

        group_a_dim = group_a.shape[0]
        group_b_dim = group_b.shape[0]

        group_a_mean = group_a.values.mean()
        group_b_mean = group_b.values.mean()

        return rank_a_sum, rank_b_sum, group_a_dim, group_b_dim, group_a_mean, group_b_mean

    # формирование итогового отчёта в виде датафрейма
    def _make_frame_report(self, groups: List[str], p_values_answers: list, answers: List[str], metrics: List[str],
                           lift: list, effect_size: list) -> pd.DataFrame:

        grs = []
        for i in range(len(groups)):
            for _ in range(len(metrics)):
                grs.append(groups[i])
        metrics *= len(groups)

        frames = [pd.DataFrame([self.ab_test for _ in range(len(metrics))], columns=['ab_test']),
                  pd.DataFrame(grs, columns=['experiment_variant']),
                  pd.DataFrame(p_values_answers, columns=['p_value']),
                  pd.DataFrame(answers, columns=['answers']),
                  pd.DataFrame(lift, columns=['lift']),
                  pd.DataFrame(effect_size, columns=['effect_size']),
                  pd.DataFrame(metrics, columns=['metrics']),
                  ]

        stat_significance_report = pd.pivot_table(pd.concat(frames, axis=1),
                                                  index=['ab_test', 'experiment_variant', 'metrics', 'answers'],
                                                  values=['p_value', 'lift', 'effect_size'])

        return stat_significance_report

    # вспомогательные методы
    # проверка на наличие новых продуктовых метрик для расчёта - если есть, то добавляем в справочник
    def _check_new_metrics(self):
        for metric in self.product_metrics:
            if metric not in self.handbook[MetricsHandbook.binary] or metric not in self.handbook[
                MetricsHandbook.categorical] \
                    or metric not in self.handbook[MetricsHandbook.numerical]:
                unique_values_number = self.data[metric].nunique()

                if unique_values_number == 2:
                    self.handbook[MetricsHandbook.binary].append(metric)
                elif 2 < unique_values_number <= self.cat_threshold:
                    self.handbook[MetricsHandbook.categorical].append(metric)
                else:
                    self.handbook[MetricsHandbook.numerical].append(metric)

        with open(self.metrics_handbook_path, 'w') as outfile:
            json.dump(self.handbook, outfile)

        return

    # проверка на наличие старых продуктовых метрик, которых нет в витрине abfinal daily, но есть в справочнике
    def _check_old_metrics_in_handbook(self):
        for key in self.handbook.keys():
            handbook_metrics = self.handbook.get(key)

            for metric in handbook_metrics:
                if metric not in self.product_metrics:
                    handbook_metrics.remove(metric)

        with open(self.metrics_handbook_path, 'w') as outfile:
            json.dump(self.handbook, outfile)

        return
