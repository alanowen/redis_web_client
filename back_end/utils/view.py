from flask._compat import with_metaclass
from flask.views import View, MethodViewType, MethodView


class CustomViewType(type):
    def __init__(cls, name, bases, d):
        super(CustomViewType, cls).__init__(name, bases, d)


class CustomView(with_metaclass(CustomViewType, View)):

    decorators = ()



