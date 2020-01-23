import logging

import numpy as np

logger = logging.getLogger("Base")
logging.basicConfig(level=logging.WARN)

from g3_model.FootballModel import FootballModel

football = FootballModel(10, 9, 13, 60)

football.simulate_whole_game(True)
