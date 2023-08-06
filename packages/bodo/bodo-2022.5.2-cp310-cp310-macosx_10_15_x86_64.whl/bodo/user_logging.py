"""
    Contains all of the helper functions and state information
    for user logging. This includes helpers for setting debug
    targets with the verbose flag.
"""
import logging
_default_logger = logging.getLogger('Bodo Default Logger')
_default_logger.setLevel(logging.DEBUG)
default_handler = logging.StreamHandler()
default_handler.setLevel(logging.DEBUG)
default_formater = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
default_handler.setFormatter(default_formater)
_default_logger.addHandler(default_handler)
_bodo_logger = _default_logger
_default_verbose_level = 0
_bodo_verbose_level = _default_verbose_level


def restore_default_bodo_verbose_level():
    global _bodo_verbose_level
    _bodo_verbose_level = _default_verbose_level


def get_verbose_level():
    return _bodo_verbose_level


def set_verbose_level(level):
    global _bodo_verbose_level
    if not isinstance(level, int) or level < 0:
        raise TypeError('set_verbose_level(): requires an integer level >= 0')
    _bodo_verbose_level = level


def restore_default_bodo_verbose_logger():
    global _bodo_logger
    _bodo_logger = _default_logger


def get_current_bodo_verbose_logger():
    return _bodo_logger


def set_bodo_verbose_logger(logger):
    global _bodo_logger
    if not isinstance(logger, logging.Logger):
        raise TypeError(
            'set_bodo_verbose_logger(): requires providing an initialized  logging.Logger type'
            )
    _bodo_logger = logger


def log_message(header, msg, *args, **kws):
    import bodo
    if bodo.get_rank() == 0:
        logger = get_current_bodo_verbose_logger()
        occz__vyt = '\n' + '=' * 80
        chrhi__zoiz = '\n'.join([occz__vyt, header.center(80, '-'), msg,
            occz__vyt])
        logger.info(chrhi__zoiz, *args, **kws)
