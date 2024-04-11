import sys
from carprice.exception import CarPriceException
from carprice.logger import logging
from carprice.pipeline.training_pipeline import TrainPipeline

try:
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
except Exception as e:
    raise CarPriceException(e, sys) from e