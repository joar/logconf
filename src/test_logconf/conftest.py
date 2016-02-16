import logging
import logging.config


def pytest_configure():
    import sys
    sys._LOGCONF_REPR_PRETTY = True

    logging_config = dict(
        version=1,
        handlers=dict(
            console=dict(
                level=logging.DEBUG,
                formatter='colorized',
                stream='ext://sys.stderr',
                **{'class': 'logging.StreamHandler'}
            )
        ),
        root=dict(
            level=logging.DEBUG,
            handlers=['console']
        ),
        formatters=dict(
            colorized={
                '()': ColorizedFormatter,
                'format': '%(levelname)s'
                          ' %(name)-20s'
                          ' in File "%(pathname)s", line %(lineno)d'
                          ' in %(funcName)s\n'
                          '%(message)s',

            }
        )
    )
    logging.config.dictConfig(logging_config)


def color(code_or_name):
    colors = {
        'grey': 0,
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35, 'purple': 35,
        'cyan': 36,
        'white': 37,
        'default': 39,
    }

    code = colors.get(code_or_name, code_or_name)

    def inner(text, bold=False):
        ansi_bytes = code
        if bold:
            ansi_bytes = '1;{}'.format(ansi_bytes)

        return '\033[{ansi_bytes}m{text}\033[{normal}m'.format(
            ansi_bytes=ansi_bytes,
            text=text,
            normal=39)

    return inner


class ColorizedFormatter(logging.Formatter):

    color = {
        logging.INFO: color('green'),
        logging.DEBUG: color('blue'),
        logging.WARN: color('yellow'),
        logging.ERROR: color('red'),
        logging.CRITICAL: color('magenta'),
    }

    def format(self, record):
        level = record.levelno

        def c(s):
            return self.color[level](s)

        record.levelname = c(record.levelname)
        record.name = color('white')(record.name)

        if isinstance(record.msg, str) and level in self.color:
            record.msg = self.color.get(level)(record.msg)

        return super(ColorizedFormatter, self).format(record)
