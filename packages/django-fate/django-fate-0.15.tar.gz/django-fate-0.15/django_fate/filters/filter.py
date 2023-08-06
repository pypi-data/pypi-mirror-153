from .fields import Field
from django.db.models import QuerySet


class FilterMeta(type):
    def __new__(mcs, name, bases, act):
        # 检测Field的命名规范
        desc_fields = []
        for attr_name, attr in act.items():
            if isinstance(attr, Field):
                desc_fields.append(attr_name)
                if attr_name.startswith('_') or attr_name[0].isupper():
                    raise TypeError(f'{name}中的{attr_name},不能为下划线开头，不能大写字母开头')
        act['_desc_fields'] = desc_fields  # 描述符中定义的字段名称列表
        return super().__new__(mcs, name, bases, act)

    def __call__(cls, *args, **kwargs):
        self = super().__call__(*args, **kwargs)
        return self._queryset


class Filter(metaclass=FilterMeta):
    """
    cls._desc_fields  描述符中定义的字段名称列表
    cls._fields  Meta.fields中定义的且没有在描述符中定义的字段名称列表
    """
    _desc_fields = []

    def __init__(self, request, queryset=None):
        user_query = request.POST or request.GET
        # queryset为None时取Meta.model.objects 这里不能用or运算，or运算会将空queryset认为None
        if queryset is None:
            self._queryset = self.Meta.model.objects
        elif isinstance(queryset, QuerySet):
            self._queryset = queryset
        else:
            raise ValueError(f'{self.__class__.__name__} queryset必须是QuerySet Object')
        query = self._generate_query(user_query)  # 用来查询的条件
        self._queryset = self._queryset.filter(**query)

    def _generate_query(self, user_query) -> dict:
        """生成查询条件"""
        query = {}
        for key, value in user_query.items():
            if key in self._fields:  # Meta.fields中定义的且没有在描述符中定义的字段名称列表
                query[key] = value

        for key, value in user_query.items():
            if key in self._desc_fields:  # 描述符中定义的字段名称列表
                setattr(self, key, value)  # 赋值描述符
                query.update(getattr(self, key))  # 获取描述符得到一个字典
        return query

    def __init_subclass__(cls, **kwargs):
        """子类被初始化后的操作"""
        # 只收集Field描述符没有定义的字段，也就是说如果描述符和Meta.fields中都定义了某个字段名称以描述符为准
        if getattr(cls.Meta, 'fields', None):
            cls._fields = [i for i in cls.Meta.fields if i not in cls._desc_fields]
        else:
            cls._fields = []
        if not getattr(cls.Meta, 'model', None):
            raise ValueError(f'{cls.__name__}的Meta.model不能为None')

    class Meta:
        fields = None  # 支持的查询字段
        model = None
