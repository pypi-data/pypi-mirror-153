import collections.abc


def is_dict(value):
    return callable(getattr(value, "keys", False))


def is_list(value):
    if isinstance(value, (str, bytes)) or is_dict(value):
        return False
    return callable(getattr(value, "__iter__", False))


def normalize_dict(value):
    result = {}
    for i in value:
        if is_dict(value[i]):
            result[i.upper()] = normalize_dict(value[i])
        elif is_list(value[i]):
            result[i.upper()] = [normalize_dict(j) for j in value[i]]
        else:
            result[i.upper()] = value[i]
    return result


class ResultDict(collections.abc.MutableMapping):
    def __init__(self, result):
        self._data = {}
        for i in result:
            if is_dict(result[i]):
                self._data[i] = ResultDict(result[i])
            elif is_list(result[i]):
                self._data[i] = [ResultDict(j) for j in result[i]]
            else:
                self._data[i] = result[i]

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        return self._data[item.upper()]

    def __setitem__(self, item, value):
        self._data[item.upper()] = value

    def __delitem__(self, item):
        del self._data[item.upper()]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)


class Function:
    def __init__(self, connection, function):
        self._connection = connection
        self._name = function.upper()
        self._description = None

    # @property
    # def description(self):
    #     if self._description is None:
    #         self._description = Description(connection=self._connection, function_name=self._name)
    #     return self._description

    def __call__(self, **kwargs):
        call_kwargs = normalize_dict(kwargs)
        result = self._connection.call(self._name, **call_kwargs)
        return ResultDict(result)
