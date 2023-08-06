import logging


def file_logging_handler(app):
    # file handler
    f_handler = logging.FileHandler(filename="hasami.log", encoding="utf-8", mode="a")

    dt_fmt = "%Y-%m-%d %H:%M:%S"
    out_fmt = "[{asctime}] [{levelname:<6}] {name}: {funcName}:{lineno}:{message}"
    logger_fmt = logging.Formatter(out_fmt, dt_fmt, style="{")
    f_handler.setFormatter(logger_fmt)
    return f_handler
