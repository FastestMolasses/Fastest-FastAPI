from loguru import logger


def setup_logging():
    # Format of the logs
    log_format = (
        '<green>{time:YYYY-MM-DD HH:mm:ss!UTC}</green> | '
        '<level>{level: <8}</level> | '
        '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
        '<level>{message}</level>'
    )

    # General logs
    logger.add(
        'logs/server.log',
        rotation='10 MB',
        retention='30 days',
        level='INFO',  # INFO logs will log everything from INFO and above (WARNING, ERROR, etc.)
        format=log_format,
        enqueue=True,
        filter=lambda record: not bool(record['exception']),
    )

    # Exception logs
    logger.add(
        'logs/exceptions.log',
        rotation='10 MB',
        retention='30 days',
        level='ERROR',  # ERROR will only log errors
        format=log_format,
        enqueue=True,
        backtrace=True,
        diagnose=True,
        filter=lambda record: bool(record['exception']),
    )
