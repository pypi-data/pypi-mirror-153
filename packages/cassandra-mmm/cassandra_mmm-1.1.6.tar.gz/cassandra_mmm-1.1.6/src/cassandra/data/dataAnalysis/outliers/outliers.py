from cassandra.data.dataAnalysis.outliers.plot import show_distplot, show_boxplot
import warnings
import numpy as np
from scipy.stats import iqr
from IPython.display import Markdown, display


def detect_and_remove_normally_distribution(df, name_target_column, show_plot=True, bin_size=500):
    df_normally_distribution = df.copy()
    upper_limit = df_normally_distribution[name_target_column].mean() + 3 * df_normally_distribution[
        name_target_column].std()
    lower_limit = df_normally_distribution[name_target_column].mean() - 3 * df_normally_distribution[
        name_target_column].std()

    new_df = df_normally_distribution[(df_normally_distribution[name_target_column] > upper_limit) | (
            df_normally_distribution[name_target_column] < lower_limit)]

    if show_plot:
        display(Markdown(f"### Dataset with highest and lowest outliers"))
        display(new_df)

    df_normally_distribution[name_target_column] = np.where(
        df_normally_distribution[name_target_column] > upper_limit,
        upper_limit,
        np.where(
            df_normally_distribution[name_target_column] < lower_limit,
            lower_limit,
            df_normally_distribution[name_target_column])
    )

    if show_plot:
        display(Markdown(f"### Distplot after capping"))
        show_distplot(df_normally_distribution, name_target_column, bin_size=bin_size)

    if show_plot:
        display(Markdown(f"### Descriptive statistics of the dataset"))
        display(df_normally_distribution[name_target_column].describe())

    return df_normally_distribution


def detect_and_remove_skewed_distribution(df, name_target_column, show_plot=True, bin_size=500):
    df_skewed_distribution = df.copy()

    if show_plot:
        show_boxplot(df_skewed_distribution, name_target_column)

    percentile25 = df_skewed_distribution[name_target_column].quantile(0.25)
    percentile75 = df_skewed_distribution[name_target_column].quantile(0.75)

    upper_limit = percentile75 + 1.5 * iqr(df_skewed_distribution[name_target_column])
    lower_limit = percentile25 - 1.5 * iqr(df_skewed_distribution[name_target_column])

    new_df = df_skewed_distribution[df_skewed_distribution[name_target_column] < upper_limit]

    if show_plot:
        display(Markdown(f"### Distplot and boxplot after trimming"))
        show_distplot(new_df, name_target_column, bin_size=bin_size)
        show_boxplot(new_df, name_target_column)

    new_df_cap = df_skewed_distribution.copy()
    new_df_cap['revenue_online'] = np.where(
        new_df_cap['revenue_online'] > upper_limit,
        upper_limit,
        np.where(
            new_df_cap['revenue_online'] < lower_limit,
            lower_limit,
            new_df_cap['revenue_online']
        )
    )

    if show_plot:
        display(Markdown(f"### Distplot and boxplot after capping"))
        show_distplot(new_df_cap, name_target_column, bin_size=bin_size)
        show_boxplot(new_df_cap, name_target_column)

    return new_df_cap


def detect_and_remove_winsorization(df, name_target_column, show_plot=True, bin_size=500, min_quantile=0.01,
                                    max_quantile=0.99):
    df_winsorization = df.copy()

    if show_plot:
        display(Markdown(
            f"#### This technique works by setting a particular threshold value, which decides based on our problem statement."))
        display(Markdown(
            f"#### While we remove the outliers using capping, then that particular method is known as Winsorization."))
        display(Markdown(
            f"#### Here we always maintain symmetry on both sides means if remove 1% from the right then in the left we also drop by 1%."))

    upper_limit = df_winsorization[name_target_column].quantile(max_quantile)
    lower_limit = df_winsorization[name_target_column].quantile(min_quantile)

    new_df = df_winsorization[
        (df_winsorization[name_target_column] <= upper_limit) & (df_winsorization[name_target_column] >= lower_limit)]

    if show_plot:
        display(Markdown(f"### Distplot and boxplot after trimming"))
        show_distplot(new_df, name_target_column, bin_size=bin_size)
        show_boxplot(new_df, name_target_column)

    df_winsorization[name_target_column] = np.where(df_winsorization[name_target_column] >= upper_limit,
                                                    upper_limit,
                                                    np.where(df_winsorization[name_target_column] <= lower_limit,
                                                             lower_limit,
                                                             df_winsorization[name_target_column]))

    if show_plot:
        display(Markdown(f"### Distplot and boxplot after capping"))
        show_distplot(df_winsorization, name_target_column, bin_size=bin_size)
        show_boxplot(df_winsorization, name_target_column)

    return df_winsorization


def detect_and_remove_outliers(df, name_target_column, show_plot=True, bin_size=500, min_quantile=0.01,
                               max_quantile=0.99):
    warnings.filterwarnings('ignore')

    if show_plot:
        display(Markdown(f"# Detect and remove the outliers"))
        display(Markdown(
            f"### The distplot  displays a combination of statistical representations of numerical data, such as histogram, kernel density estimation and normal curve, and rug plot."))
        show_distplot(df, name_target_column, bin_size=500)

    if show_plot:
        display(Markdown(f"## 1) Detect and remove the outliers from normally distribution"))
    df_normally_distribution = detect_and_remove_normally_distribution(df, name_target_column, show_plot=show_plot,
                                                                       bin_size=bin_size)

    if show_plot:
        display(Markdown(f"## 2) Detect and remove the outliers from skewed distribution"))
    df_skewed_distribution = detect_and_remove_skewed_distribution(df, name_target_column, show_plot=show_plot,
                                                                   bin_size=bin_size)

    if show_plot:
        display(Markdown(f"## 3) Detect and remove the outliers with Winsorization"))
    df_winsorization = detect_and_remove_winsorization(df, name_target_column, show_plot=show_plot, bin_size=bin_size,
                                                       min_quantile=min_quantile, max_quantile=max_quantile)

    return df_normally_distribution, df_skewed_distribution, df_winsorization
