import logging

_log = logging.getLogger(__name__)


class DotDict(dict):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __add__(self, other):
        _log.debug('DotDict.__add__: self=%r, other=%r', self, other)
        self.update(other)
        return self

    def __repr__(self):
        return '<DotDict {0}>'.format(super(DotDict, self).__repr__())


class DSLBase:
    wrap_with_key = None

    def __init__(self):
        self.data = DotDict()

    def to_dict(self):
        _log.debug('%s.to_dict: self.data=%r',
                   self.__class__.__name__,
                   self.data)
        if self.wrap_with_key is not None:
            _log.debug('self.wrap_with_key=%r', self.wrap_with_key)
            return DotDict({self.wrap_with_key: self.data})

        assert isinstance(self.data, DotDict)

        return self.data

    def __add__(self, other):
        _log.debug('__add__: %r + %r', self.to_dict(), other.to_dict())
        return self.to_dict() + other.to_dict()

    def __repr__(self):
        return '<{} data={}>'.format(self.__class__.__name__,
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


class WrapWithNameMixin:
    def __init__(self):
        self.wrapping_disabled = False

    def disable_wrap(self, disable):
        _log.debug('%s.disable_wrap(%r): self=%r',
                   self.__class__.__name__,
                   disable,
                   self)
        self.wrapping_disabled = disable
        return self

    @property
    def wrap_with_name(self):
        if self.wrapping_disabled:
            return None

        return self.data.get('name')


class ItemWrapper(DSLBase):
    def __init__(self, *args, **kwargs):
        _log.debug('%s.__init__(args=%r, kwargs=%r)',
                   self.__class__.__name__,
                   args,
                   kwargs)
        super(ItemWrapper, self).__init__()

        for arg in args:
            self.data += arg.to_dict()

        self.data += {k: v.disable_wrap(True) for k, v in kwargs.items()}


class Handlers(ItemWrapper):
    wrap_with_key = 'handlers'


class Loggers(ItemWrapper):
    wrap_with_key = 'loggers'


class Logger(DSLBase, WrapWithNameMixin):
    def __init__(self, name=None, level=None, handlers=None):
        super(Logger, self).__init__()
        self.data += dict(name=name,
                          level=level,
                          handlers=handlers)


class RootLogger(Logger):
    def __init__(self, level, handlers):
        name = 'root'
        super(RootLogger, self).__init__(name, level, handlers)


class Handler(DSLBase, WrapWithNameMixin):
    def __init__(self, klass=None, level=None, formatter=None, name=None):
        super(Handler, self).__init__()
        self.data += {'class': klass}
        self.data += dict(
            level=level,
            formatter=formatter,
            name=None
        )

    @property
    def wrap_with_key(self):
        return self.data.get('name')



