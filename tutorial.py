import logging

import numpy as np

logger = logging.getLogger("Base")
logging.basicConfig(level=logging.INFO)

from g3_model.FootballModel import FootballModel

football = FootballModel(10, 9, 13, 60)

football.simulate_whole_game(False)

# xg = np.zeros((football.grid.width, football.grid.height))

# for cell in football.grid.coord_iter():
#     cell_content, x, y = cell
#     xg[x][y] = output["prob_A"][(x,y)]

# import matplotlib.pyplot as plt

# plt.imshow(xg, interpolation="nearest")
# plt.colorbar()
