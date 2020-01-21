import logging

import numpy as np

logger = logging.getLogger("Base")
logging.basicConfig(level=logging.INFO)

from g3_model.FootballModel import FootballModel


football = FootballModel(4, 4, 5, 2)

football.who_has_ball()["player"].calculate_passing_probabilities()


# football.schedule.agents[football.id_dict["A_2"]].\
#     count_surrounding_players(football.schedule.agents[football.id_dict["A_0"]])

# type(football.schedule.agents[football.id_dict["A_2"]])

football.plot_grid()


points = [(1, 0.9), (max_distance, 0.1)]
x_coords, y_coords = zip(*points)
A = vstack([x_coords, ones(len(x_coords))]).T
m, c = lstsq(A, y_coords)[0]
print("Line Solution is y = {m}x + {c}".format(m=m, c=c))
