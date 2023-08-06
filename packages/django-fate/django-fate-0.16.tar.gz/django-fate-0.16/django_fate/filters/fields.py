import datetime


class Field:
    def __init__(self, field=None, lookup=None):
        self._field = field
        self._lookup = lookup

    def __set__(self, instance, value):
        instance.__dict__['_value'] = value

    def __get__(self, instance, owner):
        value = instance.__dict__.get('_value')
        query_key = self._field if self._lookup is None else '__'.join((self._field, self._lookup))
        return {query_key: value}

    def __set_name__(self, owner, name):
        """如果field=None 设置为name"""
        if self._field is None:
            self._field = name


class CharField(Field):
    def __set__(self, instance, value):
        try:
            instance.__dict__['_value'] = str(value)
        except Exception as err:
            raise ValueError('查询参数转化为字符串失败!')


class IntField(Field):
    def __set__(self, instance, value):
        try:
            instance.__dict__['_value'] = int(value)
        except Exception as err:
            raise ValueError('值: {} 转化为整型失败!'.format(value))


class ArrayField(Field):
    def __set__(self, instance, value):
        if isinstance(value, list):
            _value = value
        elif isinstance(value, str):
            _value = value.split(',')
        elif value is None:
            _value = []
        else:
            raise ValueError('值: {} 要求是一个数组，或者逗号分割的字符串'.format(str(value)))
        instance.__dict__['_value'] = _value


class BoolField(Field):
    def __set__(self, instance, value):
        false_li, true_li = [False, 'false', '0', 0], [True, 'true', '1', 1]
        value = str(value).lower() if isinstance(value, str) else value
        if value not in false_li + true_li:
            raise ValueError('值: {} 必须为 true,"1",1 或者 false,"0",0'.format(str(value)))
        instance.__dict__['_value'] = value in true_li


class DateTimeField(Field):
    """本函数支持了使用不完整的日期时间来查询DateTimeField"""

    def __init__(self, field=None, lookup=None):
        if lookup:
            raise ValueError('filter模块的DateTimeField 不允许设置lookup')
        self._field = field
        self._lookup = None

    def __set__(self, instance, value):
        value = value.strip()
        date, *time = value.split(' ')
        # 如果仅仅提供了日期
        if not time:
            self._handle_only_time(instance, value)
        else:  # 如果提供了时期时间，时间类型有三种1.只提供了小时 2.只提供了分钟3.完整的时分秒
            time = time[0]
            time_type = len(time.split(':'))
            # 根据time_type获取处理函数
            handle_func = getattr(self, f'_handle_type_{time_type}', self._not_support)
            handle_func(instance, value)  # 执行处理函数

    def _handle_only_time(self, instance, value):
        """如果仅仅提供了日期"""
        date_time = datetime.datetime.strptime(value, '%Y-%m-%d')
        timedelta = datetime.timedelta(days=1)
        instance.__dict__['_value'] = [date_time, date_time + timedelta]
        self._lookup = 'range'

    def _handle_type_1(self, instance, value):
        """1.只提供了小时"""
        date_time = datetime.datetime.strptime(value, '%Y-%m-%d %H')
        timedelta = datetime.timedelta(hours=1)
        instance.__dict__['_value'] = [date_time, date_time + timedelta]
        self._lookup = 'range'

    def _hanle_type_2(self, instance, value):
        """2.只提供了分钟"""
        date_time = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M')
        timedelta = datetime.timedelta(minutes=1)
        instance.__dict__['_value'] = [date_time, date_time + timedelta]
        self._lookup = 'range'

    def _hanle_type_3(self, instance, value):
        """3.完整的时分秒"""
        date_time = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        instance.__dict__['_value'] = date_time
        self._lookup = None

    def _not_support(self, instance, value):
        raise ValueError('{} 必须为合法的日期时间格式，请使用 YYYY-MM-DD 或 '
                         'YYYY-MM-DD HH:MM:SS'.format(value))
