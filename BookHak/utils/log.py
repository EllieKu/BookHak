import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

fh = logging.FileHandler(filename='log.log')
formatter = logging.Formatter("%(asctime)s %(message)s")

logger.addHandler(fh)
