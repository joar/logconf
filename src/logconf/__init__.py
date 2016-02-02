import logging
from logconf.dsl import DSLBase
from logconf.dsl import Loggers, Logger, RootLogger, Handlers, Handler

_log = logging.getLogger(__name__)


def logconf(dsl_expression):
    config = {
        'version': 1
    }
    config.update(to_dict_recursive(dsl_expression))
    return config


def to_dict_recursive(start):
    _log.debug('to_dict_recursive: start=%r', start)
    if isinstance(start, (DSLBase, dict)):
        if isinstance(start, DSLBase):
            _log.debug('is DSLBaser: %r', start)
            start = start.to_dict()

        return {k: to_dict_recursive(v) for k, v in start.items()}
    elif isinstance(start, list):
        return [to_dict_recursive(i) for i in start]
    else:
        return start


if __name__ == '__main__':
    from pprint import pprint

    import json
    import logging.config

    logging.basicConfig(level=logging.DEBUG)

    a = logconf(
        Handlers(
            Handler('logging.StreamHandler', logging.DEBUG, 'verbose',
                    'verbose'),
            console=Handler(
                klass='logging.StreamHandler'
            )
        ) +
        RootLogger(
            logging.DEBUG,
            ['console']
        ) +
        Loggers(
            Logger('logconf.dsl', logging.DEBUG, ['console']),
            foo=Logger(level=logging.DEBUG, handlers=['console'])
        )
    )

    #logging.config.dictConfig(a)

    print(json.dumps(a, indent=4
                     ))

    pprint(a)
