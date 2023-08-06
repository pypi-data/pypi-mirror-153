from logging import getLogger, NullHandler, DEBUG, INFO, ERROR


logger = getLogger('Pybrary')
logger.addHandler(NullHandler())
debug = logger.debug
info = logger.info
error = logger.error
exception = logger.exception


def level(level):
    if level.lower()=='debug':
        level = DEBUG
    elif level.lower()=='info':
        level = INFO
    elif level.lower()=='error':
        level = ERROR
    else:
        raise ValueError('level must be in debug, info, error')
    logger.level = level
