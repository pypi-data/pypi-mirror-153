class Filter:
    """
    Used to filter the ``hopara.Table.update_rows`` operation. If support the following types:
    - EQUALS: ``Filter("column1") == [1, 2, 3]``
    - LESS_THAN: ``Filter("column1") < [1, 2, 3]``
    - GREATER_THAN: ``Filter("column1") > [1, 2, 3]``
    - LESS_EQUALS_THAN: ``Filter("column1") <= [1, 2, 3]``
    - GREATER_EQUALS_THAN: ``Filter("column1") >= [1, 2, 3``
    """
    def __init__(self, column_name: str):
        """
        :param column_name: the name of the columns to be filtered
        :type column_name: str
        """
        self.column_name = column_name

    def __dump(self, comparison_type: str, values: list) -> dict:
        if not isinstance(values, list):
            values = [values]
        return {"column": self.column_name, "comparisonType": comparison_type, "values": values}

    def __eq__(self, values: list) -> dict:
        return self.__dump("EQUALS", values)

    def __lt__(self, values: list) -> dict:
        return self.__dump("LESS_THAN", values)

    def __gt__(self, values: list) -> dict:
        return self.__dump("GREATER_THAN", values)

    def __le__(self, values: list) -> dict:
        return self.__dump("LESS_EQUALS_THAN", values)

    def __ge__(self, values: list) -> dict:
        return self.__dump("GREATER_EQUALS_THAN", values)
