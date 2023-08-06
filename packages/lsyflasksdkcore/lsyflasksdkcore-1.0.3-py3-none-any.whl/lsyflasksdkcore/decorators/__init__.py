# -*- coding: utf-8 -*-


class lazyproperty:
    """
    延迟计算属性
    https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p10_using_lazily_computed_properties.html?highlight=%E9%9D%99%E6%80%81%E5%B1%9E%E6%80%A7
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value
