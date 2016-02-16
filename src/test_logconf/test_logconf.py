import logging

from enum import Enum

import pytest

from logconf import logconf, C
from logconf.dsl import Handler, Handlers, RootLogger, Logger, Loggers, \
    Formatters, Formatter


def test_logger():
    conf = logconf(
        Logger('test',
               level=logging.ERROR,
               handlers=['console'])
    )

    assert conf == {
        'version': 1,
        'test': {
            'level': logging.ERROR,
            'handlers': ['console'],
        }
    }


def test_root_logger():
    conf = logconf(
        RootLogger(level=logging.DEBUG,
                   handlers=['console'])
    )
    assert conf == {
        'version': 1,
        'root': {
            'level': logging.DEBUG,
            'handlers': ['console'],
        }
    }


class ArgMode(Enum):
    ADD = 1
    ARGS = 2
    KWARGS = 4


@pytest.mark.parametrize('arg_mode', list(ArgMode))
def test_logconf_args(arg_mode):
    console = Handler('console',
                      klass='logging.StreamHandler',
                      stream='ext://sys.stdout',
                      formatter='brief',
                      level=logging.DEBUG)
    handlers = Handlers(console)

    brief = Formatter('brief', '%(levelname)s %(name)s %(msg)s')
    formatters = Formatters(brief)

    root = RootLogger(
        logging.DEBUG,
        ['console']
    )

    arglogger = Logger('arglogger', logging.INFO, ['console'])
    kwarglogger = Logger(level=logging.WARNING, handlers=['console'])

    loggers = Loggers(
        arglogger,
        kwarglogger=kwarglogger
    )

    if arg_mode == ArgMode.ADD:
        conf = logconf(root + loggers)
    elif arg_mode == ArgMode.ARGS:
        conf = logconf(root, loggers)
    elif arg_mode == ArgMode.KWARGS:
        conf = logconf(root,
                       loggers=C(arglogger, kwarglogger=kwarglogger))
    else:
        raise Exception('ArgMode {0!r} not accounted for'.format(arg_mode))

    assert conf == {
        'version': 1,
        'root': {
            'level': logging.DEBUG,
            'handlers': ['console'],
        },
        'loggers': {
            'arglogger': {
                'handlers': ['console'],
                'level': logging.INFO,
            },
            'kwarglogger': {
                'handlers': ['console'],
                'level': logging.WARNING,
            },
        },
    }


def test_real_world_1():
    conf = logconf(
        Handlers(
            Handler('console_debug',
                    'logging.StreamHandler',
                    'verbose',
                    'DEBUG')
        ),
        Loggers(
            Logger('foo.server',
                   'DEBUG',
                   ['console_debug'],
                   False)
        ),
        Formatters(
            Formatter('verbose',
                      '%(asctime)s - %(levelname)s - %(message)s')
        ),
        disable_existing_loggers=False
    )

    assert conf == {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console_debug': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'foo.server': {
                'handlers': ['console_debug'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
        'formatters': {
            'verbose': {
                'format': '%(asctime)s - %(levelname)s - %(message)s',
            },
        },
    }
