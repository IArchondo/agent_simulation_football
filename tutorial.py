import logging

import numpy as np

logger = logging.getLogger("Base")
logging.basicConfig(level=logging.INFO)

from g3_model.FootballModel import FootballModel

football = FootballModel(11, 10, 10, 2)

for i in range(10):
    football.step()
