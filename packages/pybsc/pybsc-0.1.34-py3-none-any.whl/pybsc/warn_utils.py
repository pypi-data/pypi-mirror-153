import logging

import coloredlogs


base_logger = logging.getLogger(__name__)


def deprecated_warning(msg, cls=UserWarning,
                       logger=None):
    if logger is None:
        logger = base_logger
    coloredlogs.install(level='DEBUG', logger=logger)

    def _deprecated_warning(fn):
        def decorated(*args, **kwargs):
            logger.warning(msg)
            return fn(*args, **kwargs)

        return decorated

    return _deprecated_warning
