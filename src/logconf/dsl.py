class DotDict(dict):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __add__(self, other):
        self.update(other)
        return self


class DSLBase:
    wrap_with_key = None

    def __init__(self):
        self.data = DotDict()

    def to_dict(self):
        if self.wrap_with_key is not None:
            return {self.wrap_with_key: self.data}

        return self.data

    def __add__(self, other):
        return self.to_dict() + other.to_dict()

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__,
                                self.to_dict())


class LogConf(DSLBase):
    def __init__(self, formatters=None, handlers=None, loggers=None,
                 root=None, version=1):
        super(LogConf, self).__init__()
        self.data += dict(formatters=formatters,
                          handlers=handlers,
                          loggers=loggers,
                          root=root,
                          version=version)


class Logger(DSLBase):
    def __init__(self, name, level, handlers):
        super(Logger, self).__init__()
        self.data += dict(name=name,
                          level=level,
                          handlers=handlers)


class Handlers(DSLBase):
    wrap_with_key = 'handlers'

    def __init__(self, **kwargs):
        super(Handlers, self).__init__()
        self.data += kwargs


class Handler(DSLBase):
    def __init__(self, klass=None, level=None, formatter=None):
        super(Handler, self).__init__()
        self.data += {'class': klass}
        self.data += dict(
            level=level,
            formatter=formatter
        )



