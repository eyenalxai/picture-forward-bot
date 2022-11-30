import logging

logger = logging
logger.basicConfig(
    level=logger.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
