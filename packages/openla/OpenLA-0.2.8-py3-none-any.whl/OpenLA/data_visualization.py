import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from matplotlib.colors import cnames
from matplotlib import ticker as tick
from pandas.plotting import register_matplotlib_converters
import numpy as np

from .data_extraction import *
from .check import _is_str, _is_str_list
from .data_classes.event_stream import EventStream
from .data_classes.operation_count import OperationCount
from .data_classes.time_range_aggregation import TimeRangeAggregation
from .data_classes.pagewise_aggregation import PageWiseAggregation, PageTransition


def _set_ax(ax, figsize):
    """
    Create new axes if it is None.

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes

    :param figsize: Figure size
    :type figsize: tuple(float, float)

    :return: The axes to plot the figure on
    """
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=figsize)

    return ax


def _stacked_bar(x, top, bottom, width, ax, label, color=None):
    if color is not None:
        ax.bar(x, top, bottom=bottom, width=width, label=label, color=color)
    else:
        ax.bar(x, top, bottom=bottom, width=width, label=label)

    next_bottom = bottom + top
    return next_bottom


def visualize_grade_distribution(course_info, plot_proportion=False, xlabel=None, ylabel=None, ax=None,
                                 figsize=None, fontsize=None, save_file=None):
    """
    Drow a bar graph of grade distribution in the course.

    :param course_info: Instance of CourseInformation class
    :type course_info: CourseInformation

    :param plot_proportion: If False, the number of users in each grade is used for Y-axis.
                            If True, the proportion of each grade is used for Y-axis.
    :type plot_proportion: bool

    :param xlabel: The label name of x-axis
    :type xlabel: str

    :param ylabel: The label name of y-axis
    :type ylabel: str

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes or None

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :return: Bar graph of grade distribution.
    :rtype: matplotlib.axes.Axes
    """
    grade_distribution = course_info.grade_distribution()

    ax = _set_ax(ax, figsize)

    if plot_proportion:
        plot_column = "proportion"
    else:
        plot_column = "count"

    ax.bar(grade_distribution.index, grade_distribution[plot_column])

    if fontsize is not None:
        plt.rcParams["font.size"] = fontsize

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if save_file is not None:
        plt.savefig(save_file)
    return ax

def visualize_time_series_graph(event_stream, column, graph_type='line', time_format='%Y/%m/%d %H:%M:%S', xlabel=None, ylabel=None,
                               start_time=None, end_time=None, ax=None, figsize=None, fontsize=None, save_file=None):
    """
    Draw a time series graph of indicated “column”. If the “save_file” is indicated, the graph is saved.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param column: Column to make Y-axis of time series graph
    :type colmn: str

    :param graph_type: The graph type selected from 'line', 'step', 'plot', or 'bar'
    :type graph_type: str

    :param time_format: The time format in x axis.
                   For example, default format '%Y/%m/%d %H:%M:%S' converts "December 10, 2019 at 10:30 p.m." to "2019/12/10 22:30:00".
                   The meaning of directive such as '%Y' is in https://docs.python.org/3/library/time.html.
    :type time_format: str

    :param xlabel: The label name of x-axis
    :type xlabel: str

    :param ylabel: The label name of y-axis
    :type ylabel: str

    :param start_time: The start time of time series
    :type start_time: pandas.Timestamp or datetime.datetime or None

    :param end_time: The end time of time series
    :type end_time: pandas.Timestamp or datetime.datetime or NOne

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes or None

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :return: The time series graph of selected type
    :rtype: matplotlib.axes.Axes
    """
    df = event_stream.df
    df["eventtime"] = pd.to_datetime(df["eventtime"])

    # time range
    if (start_time is None) and (end_time is None):
        df = df
    elif start_time is None:
        df = df[df["eventtime"] < end_time]
    elif end_time is None:
        df = df[start_time <= df["eventtime"]]
    else:
        df = df[(start_time <= df["eventtime"]) & (df["eventtime"] < end_time)]

    ax = _set_ax(ax, figsize)
    register_matplotlib_converters()
    # graph type
    if graph_type == "line":
        ax.plot(df["eventtime"], df[column])
    elif graph_type == "step":
        ax.step(df["eventtime"], df[column])
    elif graph_type == "plot":
        ax.plot(df["eventtime"], df[column], marker="s", linestyle='None')
    elif graph_type == "bar":
        ax.bar(df["eventtime"], df[column], linestyle='None')

    if fontsize is not None:
        plt.rcParams["font.size"] = fontsize

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    ax.xaxis.set_major_formatter(mdates.DateFormatter(time_format))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid(True)
    if save_file is not None:
        plt.savefig(save_file)
    return ax


def visualize_operation_count_bar(operation_count, user_id=None, contents_id=None, operation_name=None,
                                  calculate_type="total", xlabel=None, ylabel=None, ax=None, figsize=None, fontsize=None,
                                  save_file=None):
    """
    Draw a bar graph which represents each operation used by a specific learner.

    :param operation_count: OperationCount instance
    :type operation_count: OperationCount

    :param user_id: The user id to make graph. If it is None, the graph is made from all users data.
    :type user_id: str, List[str], or None

    :param contents_id: The contents id to make graph. If it is None, the graph is made from all contents data.
    :type contents_id: str, List[str], or None

    :param operation_name: The operation name to count. If it is None, the graph is made for all operations.
    :type operation_name: str, List[str], or None

    :param calculate_type: 'total' or 'average'. How a multiple values integrate.
    :type calculate_type: str

    :param xlabel: The label name of x-axis
    :type xlabel: str

    :param ylabel: The label name of y-axis
    :type ylabel: str

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes or None

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :return: The bar graph
    :rtype: matplotlib.axes.Axes
    """
    if user_id is not None:
        operation_count = select_user(operation_count, user_id)
    if contents_id is not None:
        operation_count = select_contents(operation_count, contents_id)

    count_df = operation_count.df
    count_df = count_df.drop(['userid', 'contentsid'], axis=1)

    if operation_name is None:
        operation_name = operation_count.operation_name()
    elif _is_str(operation_name):
        operation_name = [operation_name]
    else:
        operation_name = operation_name

    if calculate_type == "total":
        count_df = count_df.sum(axis=0)
    elif calculate_type == "average":
        count_df = count_df.mean(axis=0)

    ax = _set_ax(ax, figsize)
    register_matplotlib_converters()
    ax.bar(operation_name, count_df.loc[operation_name])

    plt.xticks(rotation=90)
    plt.tight_layout()

    if fontsize is not None:
        plt.rcParams["font.size"] = fontsize

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    if save_file is not None:
        plt.savefig(save_file)
    return ax


def visualize_behavior_in_pages(pagewise_aggregation, contents_id, user_id=None,
                               is_plot_operation=True, is_plot_reading_time=True, operation_name=None,
                               reading_time_basis="minutes", calculate_type="total", operation_bar_colors=None,
                               reading_time_color="brown", figsize=None, fontsize=None, save_file=None):
    """
    Draw a bar graph which represents page-wise counting result of each operation and reading time.

    :param pagewise_aggregation: The instance of PageWiseAggregation
    :type pagewise_aggregation: PageWiseAggregation

    :param contents_id: The contents id to make graph. If it is None, the graph is made from all contents data.
    :type contents_id: str

    :param user_id: The user id to make graph. If it is None, the graph is made from all users data.
    :type user_id: str, List[str], or None

    :param is_plot_operation: Whether make a bar plot of operation count
    :type is_plot_operation: bool

    :param is_plot_reading_time: Whether make a bar plot of reading time
    :type is_plot_reading_time: bool

    :param operation_name: The operation name to make a bar graph. Default 'None' makes a bar graph for all operations.
    :type operation_name: str, List[str], or None

    :param reading_time_basis: 'seconds', 'minutes', or 'hours'.
    :type reading_time_basis: str

    :param calculate_type: 'total' or 'average'. How a multiple values integrate.
    :type calculate_type: str

    :param operation_bar_colors: The colors of operation bar plots. Required same number of elements with the number of operations.
                                 If default 'None', the colors are automatically decided.
    :type operation_bar_colors: List[str] or None

    :param reading_time_color: The color of reading-time bar plots. The default value is 'brouwn'.
    :type reading_time_color: str

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :return: The bar graph represents operation count and reading time in each page.
    :rtype: matplotlib.figure.Figure
    """
    df = pagewise_aggregation.df
    if df.empty:
        return

    if _is_str(contents_id):
        pagewise_aggregation = select_contents(pagewise_aggregation, contents_id)
    elif contents_id is not None:
        raise ValueError("Please specify a contents id to the argument \"contents_id\"")
    if user_id is not None:
        pagewise_aggregation = select_user(pagewise_aggregation, user_id)

    num_pages = pagewise_aggregation.num_unique_pages()
    x = np.arange(num_pages) + 1

    width = 0.4
    if is_plot_operation:
        fig, ax_operation = plt.subplots(figsize=figsize)

        if operation_name is None:
            operation_name = pagewise_aggregation.operation_name()
        elif _is_str(operation_name):
            operation_name = [operation_name]
        else:
            operation_name = operation_name

        if calculate_type == "total":
            operation_count = df.groupby("pageno").sum()
        elif calculate_type == "average":
            operation_count = df.groupby("pageno").mean()

        next_bottom = 0
        if operation_bar_colors is not None:
            for operation, color in zip(operation_name, operation_bar_colors):
                y = operation_count[operation].values
                next_bottom = _stacked_bar(x, y, next_bottom, width, ax_operation, operation, color)
        else:
            for operation in operation_name:
                y = operation_count[operation].values
                next_bottom = _stacked_bar(x, y, next_bottom, width, ax_operation, operation)
        # ax_operation.set_ylabel("Operation count", fontsize=fontsize)
        # ax_operation.set_xlabel("Page", fontsize=fontsize)
        ax_operation.set_ylabel("Operation count")
        ax_operation.set_xlabel("Page")
        ax_operation.legend(loc='upper left', bbox_to_anchor=(1.3, 0.95))


    if is_plot_reading_time:
        if is_plot_operation:
            ax_time = ax_operation.twinx()
        else:
            fig, ax_time = plt.subplots(figsize=figsize)

        if calculate_type == "total":
            reading_time = df.groupby("pageno")["reading_seconds"].sum().values
        elif calculate_type == "average":
            reading_time = df.groupby("pageno")["reading_seconds"].mean().values

        if reading_time_basis == "seconds":
            pass
        elif reading_time_basis == "minutes":
            reading_time = reading_time / 60
        elif reading_time_basis == "hours":
            reading_time = reading_time / 3600
        else:
            raise ValueError("Invalid reading time basis")

        if is_plot_operation:
            ax_time.bar(x+width, reading_time, width=width, label="reading minutes", color=cnames[reading_time_color])
            plt.xticks(x + width/2, x)
        else:
            ax_time.bar(x, reading_time, width=width, label="reading minutes", color=cnames[reading_time_color])

        # ax_time.set_ylabel("Reading {} in the page".format(reading_time_basis), fontsize=fontsize)
        # ax_time.set_xlabel("Page", fontsize=fontsize)
        ax_time.set_ylabel("Reading {} in the page".format(reading_time_basis))
        ax_time.set_xlabel("Page")

        ax_time.legend(loc='upper left', bbox_to_anchor=(1.3, 1.0))


    plt.xticks(ticks=range(1, num_pages, 5), labels=range(1, num_pages, 5))
    plt.tight_layout()

    if fontsize is not None:
        plt.rcParams["font.size"] = fontsize

    if save_file is not None:
        plt.savefig(save_file)

    if is_plot_operation and is_plot_reading_time:
        return ax_operation, ax_time
    elif is_plot_operation:
        return ax_operation
    elif is_plot_reading_time:
        return ax_time


def visualize_pages_in_time_range(time_range_aggregation, contents_id, user_id=None, xlabel=None, ylabel=None,
                                  ax=None, figsize=None, fontsize=None, save_file=None, show_legend=False):
    """
    Draw a line graph which represents which page is read in time ranges.

    :param time_range_aggregation: TImeRangeAggregation instance
    :type time_range_aggregation: TimeRangeAggregation

    :param contents_id: The contents id to make graph
    :type contents_id: str

    :param user_id: The user id to make graph
    :type user_id: str, List[str], or None

    :param xlabel: The label name of x-axis
    :type xlabel: str

    :param ylabel: The label name of y-axis
    :type ylabel: str

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes or None

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :param show_legend: Whether to show legend of the graph. If the number of users in this graph is large,
                        this argument is recommended to be set False.
    :type show_legend: bool

    :return: The line graph which shows the page tracking
    :rtype: matplotlib.axes.Axes
    """

    if not _is_str(contents_id):
        raise ValueError("Please specify a contents id to the argument \"contents_id\"")

    ax = _set_ax(ax, figsize)

    if user_id is None:
        user_id = time_range_aggregation.user_id()
    elif _is_str(user_id):
        user_id = [user_id]

    time_range_aggregation = select_contents(time_range_aggregation, contents_id)
    time_range_df = time_range_aggregation.df
    for column in ['elapsed_seconds', 'elapsed_minutes', 'elapsed_hours']:
        if column in time_range_df.columns:
            time_range_basis = column
            break

    max_time = 0
    max_page = 0
    for user in user_id:
        user_df = time_range_df[time_range_df['userid'] == user]
        if user_df.empty:
            continue
        ax.step([0]+user_df[time_range_basis], [0]+user_df['pageno'], label=user)
        max_time = max(max_time, max(user_df[time_range_basis]))
        max_page = max(max_page, max(user_df['pageno']))

    if fontsize is not None:
        plt.rcParams["font.size"] = fontsize
    if xlabel is None:
        xlabel = time_range_basis.replace("_", " ")
    if ylabel is None:
        ylabel = "page"
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if show_legend:
        ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1.0))
    plt.grid(axis='both', which='both')
    if save_file is not None:
        plt.savefig(save_file)
    return ax


def visualize_operation_in_time_range(time_range_aggregation, contents_id, user_id=None, operation_name=None,
                                     calculate_type="total", operation_bar_colors=None,
                                     xlabel=None, ylabel=None, ax=None, figsize=None, fontsize=None, save_file=None):
    """
    Draw a bar graph which represents how many operations are used in time ranges.

    :param time_range_aggregation: TImeRangeAggregation instance
    :type time_range_aggregation: TimeRangeAggregation

    :param contents_id: The contents id to make graph
    :type contents_id: str

    :param user_id: The user id to make graph
    :type user_id: str, List[str], or None

    :param operation_name: The operation name to make a bar graph. Default 'None' makes a bar graph for all operations.
    :type operation_name: str, List[str], or None

    :param calculate_type: 'total' or 'average'. How a multiple values integrate.
    :type calculate_type: str

    :param operation_bar_colors: The colors of operation bar plots. Required same number of elements with the number of operations.
                                 If default 'None', the colors are automatically decided.
    :type operation_bar_colors: List[str] or None

    :param xlabel: The label name of x-axis
    :type xlabel: str

    :param ylabel: The label name of y-axis
    :type ylabel: str

    :param ax: The axes to plot the figure on. If None, new axes is created
    :type ax: matplotlib.axes.Axes or None

    :param figsize: Figure size
    :type figsize: tuple(float, float) or None

    :param save_file: The file path for saving the graph
    :type save_file: str or None

    :return: The line graph which shows the page tracking
    :rtype: matplotlib.axes.Axes
    """

    ax = _set_ax(ax, figsize)

    if user_id is None:
        user_id = time_range_aggregation.user_id()
    time_range_aggregation = select_user(time_range_aggregation, user_id)
    time_range_aggregation = select_contents(time_range_aggregation, contents_id)
    time_range_df = time_range_aggregation.df
    for column in ['elapsed_seconds', 'elapsed_minutes', 'elapsed_hours']:
        if column in time_range_df.columns:
            time_range_basis = column
            break

    if operation_name is None:
        operation_name = time_range_aggregation.operation_name()
    elif _is_str(operation_name):
        operation_name = [operation_name]
    else:
        operation_name = operation_name

    if calculate_type == "total":
        operation_count = time_range_df.groupby(time_range_basis).sum()
    elif calculate_type == "average":
        operation_count = time_range_df.groupby(time_range_basis).mean()

    width = 0.8
    next_bottom = 0
    x = time_range_df[time_range_basis].unique()
    if operation_bar_colors is not None:
        for operation, color in zip(operation_name, operation_bar_colors):
            y = operation_count[operation].values
            next_bottom = _stacked_bar(x, y, next_bottom, width, ax, operation, color)
    else:
        for operation in operation_name:
            y = operation_count[operation].values
            next_bottom = _stacked_bar(x, y, next_bottom, width, ax, operation)

    xlabel = xlabel if xlabel is not None else time_range_basis.replace("_", " ")
    ylabel = ylabel if ylabel is not None else "operation count"
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1.0))
    plt.tight_layout()


    if fontsize is not None:
        plt.rcParams["font.size"] = fontsize

    if save_file is not None:
        plt.savefig(save_file)

    return ax
