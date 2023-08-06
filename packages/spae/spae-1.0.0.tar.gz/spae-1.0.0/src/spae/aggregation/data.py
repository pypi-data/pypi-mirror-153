import datetime
import re

from dateutil.relativedelta import relativedelta

from pyspark.sql.types import TimestampType
from pyspark.sql.functions import unix_timestamp, min, max

from .exceptions import DataSetEmpty

types = {}
def handles(*data_types):

    def registry(data_type_definition):
        for data_type in data_types:
            types[data_type] = data_type_definition
        return data_type_definition

    return registry

class DataType:
    @staticmethod
    def get_range(table, column, condition):
        using = column.column
        d_range = table.df.filter(condition).select(min(using).alias('__min'), max(using).alias('__max')).collect()[0]
        return d_range['__min'], d_range['__max']

    @staticmethod
    def preprocess_column(table, column):
        return column

    @staticmethod
    def get_value(value):
        return value

    @staticmethod
    def get_min_value(value):
        return float(value)

    @staticmethod
    def get_max_value(value):
        return float(value)

    @staticmethod
    def get_step(step):
        return step

    @classmethod
    def get_value_list(cls, min_value, max_value, step):
        step = cls.get_step(step)
        value_list = []
        while min_value <= max_value:
            value_list.append(min_value)
            min_value += step

        value_list.append(min_value)

        if len(value_list) == 0:
            raise DataSetEmpty()

        return value_list


@handles(TimestampType, 'DateTime')
class DateTime(DataType):
    @staticmethod
    def get_range(table, column, condition):
        start, end = DataType.get_range(table, column, condition)
        if isinstance(start, int):
            start = datetime.datetime.fromtimestamp(start)

        start = start.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        return (start, end)

    @staticmethod
    def preprocess_column(table, column):
        trans_to = f'spae__{column}__stamp'
        table.df = table.df.withColumn(trans_to, unix_timestamp(table.df[column]))
        return trans_to

    @staticmethod
    def get_value(value):
        return datetime.datetime.fromtimestamp(value)

    @staticmethod
    def get_step(step):
        duration_dict = {
            'M': 'months',
            'd': 'days',
            'w': 'weeks',
            'h': 'hours',
            'm': 'minutes',
            'y': 'years'
        }
        params = {}
        if step:
            duration = 0
            for n, unit in re.findall('([0-9]+)(\w)', step):
                n = int(n)
                unit = duration_dict[unit]
                if unit in params:
                    params[unit] += n
                else:
                    params[unit] = n
            if not params:
                params = {'days': 1}
            return relativedelta(**params)
        else:
            return datetime.timedelta(days=1)

    @classmethod
    def get_value_list(cls, min_value, max_value, step):
        step = cls.get_step(step)
        value_list = []
        if not isinstance(min_value, datetime.datetime):
            min_value = datetime.datetime.fromtimestamp(min_value)

        if not isinstance(max_value, datetime.datetime):
            max_value = datetime.datetime.fromtimestamp(max_value)

        while min_value <= max_value:
            value_list.append(min_value.timestamp())
            min_value += step

        value_list.append(min_value.timestamp())

        if len(value_list) == 0:
            raise DataSetEmpty()

        return value_list


@handles('Int')
class IntType(DataType):
    @staticmethod
    def get_step(step):
        if step:
            return int(step)
        else:
            return 1


@handles('Category')
class Category(IntType):
    @staticmethod
    def get_step(step):
        if step is not None:
            return step
        else:
            return 1
