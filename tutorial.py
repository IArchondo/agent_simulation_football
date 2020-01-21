import logging

import numpy as np

logger = logging.getLogger("Base")
logging.basicConfig(level=logging.INFO)

from g3_model.FootballModel import FootballModel


football = FootballModel(4, 4, 5, 2)


football.plot_grid()

football.step()
