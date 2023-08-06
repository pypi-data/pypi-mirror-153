from ..check import _is_str, _is_str_list


class OperationCount(object):
    def __init__(self, df):
        self._df = df

    @property
    def df(self):
        return self._df

    def num_users(self):
        """
        Get the number of users in the Dataframe

        :return: The number of users in the Dataframe
        :rtype: int
        """
        return self.df['userid'].nunique()

    def user_id(self):
        """
        Get the unique user ids in the Dataframe

        :return: One-dimensional array of user ids in the event_stream
        :rtype: List[str]
        """
        return list(self.df['userid'].unique())

    def contents_id(self):
        """
        Get the unique contents ids in the Dataframe

        :return: One-dimensional array of contents ids in the Dataframe
        :rtype: List[str]
        """
        return list(self.df['contentsid'].unique())

    def operation_name(self):
        """
        Get the unique operations in the Dataframe

        :return: One-dimensional array of operation names in the Dataframe
        :rtype: List[str]
        """
        return list(self.df.columns.drop(['userid', 'contentsid']).values)

    def operation_count(self, operation_name=None, user_id=None, contents_id=None):
        """
        Get the count of specified operations

        :param user_id: The user to count operation. If it is None, the total count of all users is returned.
        :type user_id: str or None

        :param contents_id: The contents to count operation. If it is None, the total count in all contents is returned.
        :type contents_id: str or None

        :param operation_name: The name of operation to count
        :type operation_name: str or None

        :return: If "operation_name" is None, return dictionary of the number of each operation in the Dataframe.
                 (Key: operation name, Value: The count of the operation)

                 else if "operation_name" is indicated, return the count of the operation
        :rtype: dict or int
        """
        df = self.df

        if user_id is not None:
            if _is_str(user_id) or not hasattr(user_id, "__iter__"):
                df = df[df['userid'] == user_id]
            else:
                df = df[df['userid'].isin(user_id)]

        if contents_id is not None:
             if _is_str(contents_id) or not hasattr(contents_id, "__iter__"):
                 df = df[df['contentsid'] == contents_id]
             else:
                 df = df[df['contentsid'].isin(contents_id)]

        operation_count_dict = dict(df.drop(['userid', 'contentsid'], axis=1).sum())
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