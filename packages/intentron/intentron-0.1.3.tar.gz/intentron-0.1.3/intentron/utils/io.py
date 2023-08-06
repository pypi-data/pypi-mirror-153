from loguru import logger
logger.add("pipeline_{time}.log", format="{time} - {level} - {message}", level="DEBUG")
log = logger
