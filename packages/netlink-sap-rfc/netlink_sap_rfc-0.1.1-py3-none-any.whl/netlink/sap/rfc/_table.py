import collections.abc
import re
import textwrap

from netlink.logging import logger


def select(rfc_connection, table, *args, **kwargs):
    arguments = {'QUERY_TABLE': table.upper()}
    if args:
        arguments['FIELDS'] = [{'FIELDNAME': i.upper()} for i in args]
    if kwargs:
        options_items = []
        for i in kwargs:
            if i.upper() == '_SKIP':
                arguments['ROWSKIPS'] = kwargs[i]
                continue
            if i.upper() == '_COUNT':
                arguments['ROWCOUNT'] = kwargs[i]
                continue
            if isinstance(kwargs[i], int):
                options_items.append(f"{i.upper()} EQ {kwargs[i]}")
            else:
                if '*' in kwargs[i]:
                    options_items.append(f"{i.upper()} LIKE '{kwargs[i].replace('*', '%')}'")
                else:
                    options_items.append(f"{i.upper()} EQ '{kwargs[i]}'")
        arguments['OPTIONS'] = [{'TEXT': i} for i in
                                textwrap.wrap(' AND '.join(options_items))]
    logger.debug(f'{arguments}')
    rfc_response = rfc_connection.rfc_read_table(**arguments)
    regex = re.compile(''.join(['(.{%s})' % int(i.LENGTH) for i in rfc_response.FIELDS]))
    length = sum([int(i.LENGTH) for i in rfc_response.FIELDS])
    fields = tuple([i.FIELDNAME for i in rfc_response.FIELDS])
    result = []
    for data in rfc_response.DATA:
        line = data.WA + ' '*(length-len(data.WA))
        m = regex.match(line)
        if m:
            rcd = {}
            for i in range(m.lastindex):
                rcd[rfc_response.FIELDS[i].FIELDNAME] = m.group(i+1).rstrip()
            result.append(Record(fields, **rcd))
    return result


class Record(collections.abc.Mapping):
    def __init__(self, fields, **kwargs):
        self._fields = fields
        self._data = {}
        for kw in kwargs:
            self._data[kw.upper()] = kwargs[kw]

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, item):
        if isinstance(item, int):
            # get by index in field-list
            item = self._fields[item]
        return self._data[item.upper()]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)
