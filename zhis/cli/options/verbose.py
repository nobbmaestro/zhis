import logging

import click


def configure_logger(ctx, param, value: bool):  # pylint: disable=unused-argument
    levels = (
        logging.CRITICAL,
        logging.INFO,
        logging.DEBUG,
    )

    level = levels[min(len(levels), value)]

    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(asctime)s %(module)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
    )


def verbose_option(func):
    return click.option(
        "-v",
        "--verbose",
        callback=configure_logger,
        expose_value=False,
        is_eager=True,
        count=True,
        help="Increase verbosity (-v, -vv...).",
    )(func)
