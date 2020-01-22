import logging

import numpy as np

logger = logging.getLogger("Base")
logging.basicConfig(level=logging.INFO)

from g3_model.FootballModel import FootballModel

football = FootballModel(11, 6, 10, 2)

for i in range(20):
    football.step()

football.who_has_ball()["player"].shoot()


# TODO add way to know where the ball is
# xg = np.zeros((football.grid.width, football.grid.height))

# for cell in football.grid.coord_iter():
#     cell_content, x, y = cell
#     xg[x][y] = output["prob_A"][(x,y)]

# import matplotlib.pyplot as plt

# plt.imshow(xg, interpolation="nearest")
# plt.colorbar()
