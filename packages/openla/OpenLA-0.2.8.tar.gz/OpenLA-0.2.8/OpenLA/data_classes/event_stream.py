import warnings
from ..check import _is_str, _is_str_list


class EventStream(object):
    def __init__(self, df):
        self._df = df

    @property
    def df(self):
        return self._df

    def num_users(self):
        """
        Get the number of users in the event stream

        :return: The number of users in the event stream
        :rtype: int
        """
        return self.df['userid'].nunique()

    def user_id(self):
        """
        Get the unique user ids in the event stream

        :return: One-dimensional array of user ids in the event_stream
        :rtype: List[str]
        """
        return list(self.df['userid'].unique())

    def contents_id(self):
        """
        Get the unique contents ids in the event stream

        :return: One-dimensional array of contents ids in the event stream
        :rtype: List[str]
        """
        return list(self.df['contentsid'].unique())

    def operation_name(self):
        """
        Get the unique operations in event stream

        :return: One-dimensional array of operation names in the event stream
        :rtype: List[str]
        """
        return list(self.df['operationname'].unique())

    def marker_type(self):
        """
        Get the unique marker types in the event stream

        :return: One-dimensional array of marker-types in the event stream
        :rtype: List[str]
        """
        return list(self.df['marker'].dropna().unique())

    def device_code(self):
        """
        Get the unique device codes in the event stream

        :return: One-dimensional array of device-code in the event stream
        :rtype: List[str]
        """
        return list(self.df['devicecode'].unique())

    def operation_count(self, operation_name=None, user_id=None, contents_id=None, separate_marker_type=False):
        """
        Get the count of each operation in event stream

        :param user_id: The user to count operation
        :type user_id: str or None

        :param contents_id: The contents to count operation
        :type contents_id: str, List[str], or None

        :param operation_name: The name of operation to count
        :type operation_name: str or None

        :param separate_marker_type: whether to count 'MARKER' operations by separating the type "difficult" or "important"
        :type separate_marker_type: bool

        :return: If "operation_name" is None, return dictionary of the number of each operation in event stream.
                 (Key: operation name, Value: The count of the operation)

                 else if "operation_name" is indicated, return the count of the operation
        :rtype: dict or int
        """
        def _attach_marker_type(row):
            op = row['operationname']
            marker_type = row['marker']

            if op in ('ADD MARKER', 'DELETE MARKER'):
                return op + ' ' + marker_type
            else:
                return op

        df = self.df
        if separate_marker_type:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                df['operationname'] = df.loc[:, ['operationname', 'marker']].apply(_attach_marker_type, axis=1)

        if user_id is not None:
            df = df[df['userid'] == user_id]

        if contents_id is not None:
             if _is_str(contents_id) or not hasattr(contents_id, "__iter__"):
                 df = df[df['contentsid'] == contents_id]
             else:
                 df = df[df['contentsid'].isin(contents_id)]

        operation_count_dict = dict(df['operationname'].value_counts())
        if operation_name is None:
            return operation_count_dict
        else:
            if not _is_str(operation_name) and hasattr(operation_name, "__iter__"):
                op_dict = {}
                for op_name in operation_name:
                    op_dict[op_name] = operation_count_dict.get(op_name, 0)
                return op_dict

            else:
                return operation_count_dict.get(operation_name, 0)


    def to_csv(self, save_file):
        if save_file[-4:] != ".csv":
            save_file += ".csv"
        self.df.to_csv(save_file, index=False, encoding="utf-8-sig")