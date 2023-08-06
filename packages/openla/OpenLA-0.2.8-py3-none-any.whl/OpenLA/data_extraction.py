"""
This module receives event stream data and extracts information required.
"""

import datetime
import warnings
import pandas as pd
from .course_information import CourseInformation
from .data_classes.event_stream import EventStream
from .data_classes.operation_count import OperationCount
from .data_classes.time_range_aggregation import TimeRangeAggregation
from .data_classes.pagewise_aggregation import PageWiseAggregation, PageTransition
from .check import _is_int, _is_int_list, _is_str, _is_str_list


def select_user(data, user_id):
    """
    Extract the log data of the selected user.

    If the argument “user_id” is given as a list, the function extracts all users in the list.

    :param data: The instance of EventStream or converted class
    :type data: EventStream, OperationCount, PageWiseAggregation, PageTransition, or TimeRangeAggregation

    :param user_id: a user id or list of user ids
    :type user_id: str or list[str]

    :return: Extracted result.
    :rtype: The same type with input.

    """
    df = data.df
    if _is_str(user_id) or not hasattr(user_id, "__iter__"):
        selected_user_df = df[df['userid'] == user_id]
    else:
        selected_user_df = df[df['userid'].isin(user_id)]

    return_class = type(data)
    return return_class(selected_user_df)


def select_contents(data, contents_id):
    """
    Extract the log data of the selected contents.

    If the argument “contents_id” is given as a list, the function extracts all contents in the list.

    :param data: The instance of EventStream or converted class
    :type data: EventStream, OperationCount, PageWiseAggregation, PageTransition, or TimeRangeAggregation

    :param contents_id: A contents id or list of contents ids
    :type contents_id: str or list[str]

    :return: Extracted result.
    :rtype: The same type with input.
    """
    df = data.df
    if _is_str(contents_id) or not hasattr(contents_id, "__iter__"):
        selected_contents_df = df[df['contentsid'] == contents_id]
    else:
        selected_contents_df = df[df['contentsid'].isin(contents_id)]

    return_class = type(data)
    return return_class(selected_contents_df)


def select_operation(event_stream, operation_name):
    """
    Extract the event stream of the selected operation.

    If the argument “operation_name” is given as a list, the function extracts all operation names in the list.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param operation_name: An operation name or list of operation names
    :type operation_name: str or list[str]

    :return: Extracted result.
    :rtype: EventStream
    """
    df = event_stream.df
    if _is_str(operation_name) or not hasattr(operation_name, "__iter__"):
        selected_operation_df = df[df['operationname'] == operation_name]
    else:
        selected_operation_df = df[df['operationname'].isin(operation_name)]

    return EventStream(selected_operation_df)


def select_marker_type(event_stream, marker_type):
    """
    Extract the event stream of the selected type of marker operation.

    If the argument “marker_type” is given as a list, the function extracts all marker types in the list.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param marker_type: A marker type or list of marker types
    :type marker_type: str or list[str]

    :return: Extracted result.
    :rtype: EventStream
    """
    df = event_stream.df
    if _is_str(marker_type) or not hasattr(marker_type, "__iter__"):
        selected_marker_df = df[df['marker'] == marker_type]
    else:
        selected_marker_df = df[df['marker'].isin(marker_type)]

    return EventStream(selected_marker_df)


def select_device(event_stream, device_name):
    """
    Extract the event stream recorded by the selected device.

    If the argument “device_name” is given as a list, the function extracts all device names in the list.

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param device_name: A device name or list of davice names
    :type device_name: str or list[str]

    :return: Extracted result.
    :rtype: EventStream
    """
    df = event_stream.df
    if _is_str(device_name) or not hasattr(device_name, "__iter__"):
        selected_device_df = df[df['devicecode'] == device_name]
    else:
        selected_device_df = df[df['devicecode'].isin(device_name)]

    return EventStream(selected_device_df)


def select_page(event_stream, bottom=None, top=None):
    """
    Extract the event stream recorded in the page between "bottom" number and "top" number.

    If the argument "bottom" is None, extract all pages under the "top".

    If the argument "top" is None, extract all pages above the "bottom".

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param bottom: The bottom number of page for extraction
    :type bottom: int or None

    :param top: The top number of page for extraction
    :type top: int or None

    :return: Extracted result.
    :rtype: EventStream
    """
    df = event_stream.df
    if bottom is None and top is None:
        return event_stream
    elif top is None:
        selected_page_df = df[bottom <= df['pageno']]
    elif bottom is None:
        selected_page_df = df[df['pageno'] <= top]
    else:
        selected_page_df = df[(bottom <= df['pageno']) & (df['pageno'] <= top)]
    return EventStream(selected_page_df)


def select_memo_length(event_stream, bottom=None, top=None):
    """
    Extract the event stream of memo (note) operation with the length between bottom number and top number.

    If the argument "bottom" is None, extract all memo length under the "top".

    If the argument "top" is None, extract all memo length above the "bottom".

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param bottom: The bottom length of memo for extraction
    :type bottom: int or None

    :param top: The top length of memo for extraction
    :type top: int or None

    :return: Extracted result.
    :rtype: EventStream
    """

    df = event_stream.df
    if bottom is None and top is None:
        return event_stream
    elif top is None:
        selected_memo_df = df[bottom <= df['memo_length']]
    elif bottom is None:
        selected_memo_df = df[df['memo_length'] <= top]
    else:
        selected_memo_df = df[(bottom <= df['memo_length']) & (df['memo_length'] <= top)]
    return EventStream(selected_memo_df)


def select_time(event_stream, start_time=None, end_time=None):
    """
    Extract the event stream recorded between "start_time" and "end_time".

    If the argument "start_time" is None, extract all event stream before "end_time".

    If the argument "end_time" is None, extract all event stream after "start_time".

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param start_time: The start time of event stream for extraction
    :type start_time: pandas.Timestamp or datetime.datetime or None

    :param end_time: The end time of event stream for extraction
    :type end_time: pandas.Timestamp or datetime.datetime or None

    :return: Extracted result.
    :rtype: EventStream
    """

    df = event_stream.df
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        df["timestamp"] = pd.to_datetime(df["eventtime"])

    if start_time is None and end_time is None:
        return event_stream
    elif start_time is None:
        selected_time_df = df[df["timestamp"] < end_time]
    elif end_time is None:
        selected_time_df = df[start_time <= df["timestamp"]]
    else:
        selected_time_df = df[(start_time <= df["timestamp"]) & (df["timestamp"] < end_time)]

    del selected_time_df["timestamp"]
    return EventStream(selected_time_df)


def select_by_lecture_time(course_info, event_stream, lecture_week, timing='during',
                           extension_minutes_before_lecture=0, extension_minutes_after_lecture=0,
                           include_other_lecture_time=False):
    """
    Extract the event stream recorded after, before, or during lecture.

    :param course_info: CourseInformation instance.
                       (See course_information module to know about class CourseInformation)
    :type course_info: CourseInformation

    :param event_stream: EventStream instance
    :type event_stream: EventStream

    :param lecture_week: a lecture week to extract event stream.
    :type lecture_week: int

    :param timing: The timing to extract the event stream. Choose from "after", "before", or "during".
    :type timing: str

    :param extension_minutes_before_lecture: If you want to include some minutes before the lecture started into the lecture time, use this argument.
                                             If you do not want to include some minutes after the lecture started into the lecture time, negative value can be used.
    :type extension_minutes_before_lecture: int

    :param extension_minutes_after_lecture: If you want to include some minutes after the lecture ended into the lecture time, use this argument.
                                            If you do not want to include some minutes before lecture ended into the lecture time, nagative calue can be used.
    :type extension_minutes_after_lecture: int

    :param include_other_lecture_time: If this argument is False, the extracted result does not include the lecture time except for selected lecture week.
                                       For example, in the case of 'lecture_week=2', 'timing=before', and 'include_other_lecture_time=False',
                                       the extracted result is the event stream from the end of lecture 1 to the begin of lecture 2.
                                       If this argument is True and the argument 'timing' is 'before' or 'after', the extracted result include the lecture time before/after selected lecture week.
                                       For example, in the case of 'lecture_week=2', 'timing=before', and 'include_other_lecture_time=True',
                                       the extracted result is the event stream from the first log of the stream to the begin of lecture 2.

    :return: Extracted result.
    :rtype: EventStream
    """
    assert type(lecture_week) == int, "Please indicate int type value for the argument 'lecture_week'."

    assert timing in ['during', 'before', 'after'], \
        "invalid timing was inputted. please pass 'during' or 'before' or 'after' for timing."

    lecture_start = course_info.lecture_start_time(lecture_week)
    lecture_end = course_info.lecture_end_time(lecture_week)
    lecture_weeks_in_course = course_info.lecture_week()

    if timing == 'during':
        start_time = lecture_start - datetime.timedelta(minutes=extension_minutes_before_lecture)
        end_time = lecture_end + datetime.timedelta(minutes=extension_minutes_after_lecture)

    elif timing == 'before':
        if (not include_other_lecture_time) and (lecture_week-1 in lecture_weeks_in_course):
            start_time = course_info.lecture_end_time(lecture_week-1) + datetime.timedelta(minutes=extension_minutes_after_lecture)
        else:
            start_time = None
        end_time = lecture_start - datetime.timedelta(minutes=extension_minutes_before_lecture)

    elif timing == 'after':
        start_time = lecture_end + datetime.timedelta(minutes=extension_minutes_after_lecture)
        if (not include_other_lecture_time) and (lecture_week+1 in lecture_weeks_in_course):
            end_time = course_info.lecture_start_time(lecture_week+1) - datetime.timedelta(minutes=extension_minutes_before_lecture)
        else:
            end_time = None

    return select_time(event_stream=event_stream, start_time=start_time, end_time=end_time)


def concat_data(data_list):
    """
    Concatenate multiple data belonging to same class in EventStream, OperationCount, PageWiseAggregation, PageTransition, or TimeRangeAggregation

    :param data_list: List of data to concatenate
    :type data_list: list[EventStream], list[OperationCount], list[PageWiseAggregation], list[PageTransition], or list[TimeRangeAggregation]

    :return: The concatenated instance.
    """

    data_type = type(data_list[0])
    data_check_list = [type(data) == data_type for data in data_list]
    is_same_type = all(data_check_list)
    is_acceptable_type = data_type in [EventStream, OperationCount, PageWiseAggregation, PageTransition, TimeRangeAggregation]
    assert is_same_type and is_acceptable_type, \
        "The function 'concat_data' can accept the list of same type elements belonging to EventStream, OperationCount, PageWiseAggregation, PageTransition, or TimeRangeAggregation"

    concat_df = pd.DataFrame()
    for data in data_list:
        concat_df = pd.concat([concat_df, data.df], axis=0)

    return data_type(concat_df)

