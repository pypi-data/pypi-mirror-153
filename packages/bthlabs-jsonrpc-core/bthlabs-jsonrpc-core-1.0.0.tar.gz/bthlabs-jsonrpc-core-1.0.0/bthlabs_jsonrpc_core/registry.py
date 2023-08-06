# -*- coding: utf-8 -*-
# django-jsonrpc-core | (c) 2022-present Tomek Wójcik | MIT License
class MethodRegistry:
    INSTANCE = None
    DEFAULT_NAMESPACE = 'jsonrpc'

    def __init__(self, *args, **kwargs):
        self.registry = {}
        self.registry[self.DEFAULT_NAMESPACE] = {}

    @classmethod
    def shared_registry(cls, *args, **kwargs):
        if cls.INSTANCE is None:
            cls.INSTANCE = cls(*args, **kwargs)

        return cls.INSTANCE

    def register_method(self, namespace, method, handler):
        if namespace not in self.registry:
            self.registry[namespace] = {}

        self.registry[namespace][method] = handler

    def get_methods(self, namespace):
        return self.registry.get(namespace, {}).keys()

    def get_handler(self, namespace, method):
        return self.registry.get(namespace, {}).get(method, None)
