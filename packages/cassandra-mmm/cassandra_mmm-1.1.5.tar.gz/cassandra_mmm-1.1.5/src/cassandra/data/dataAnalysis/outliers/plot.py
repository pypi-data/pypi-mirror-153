import plotly.figure_factory as ff
import plotly.graph_objects as go


def show_distplot(df, name_target_column, bin_size=500):
    hist_data = [list(df[name_target_column])]
    group_labels = ['distplot']  # name of the dataset

    fig = ff.create_distplot(hist_data, group_labels, bin_size=bin_size)
    fig.show()


def show_boxplot(df, name_target_column):
    fig = go.Figure()
    fig.add_trace(go.Box(
        x=df[name_target_column],
        name="Suspected Outliers",
        boxpoints='suspectedoutliers',  # only suspected outliers
        marker=dict(
            color='rgb(8,81,156)',
            outliercolor='rgba(219, 64, 82, 0.6)',
            line=dict(
                outliercolor='rgba(219, 64, 82, 0.6)',
                outlierwidth=2)),
        line_color='rgb(8,81,156)'
    ))
    fig.show()
