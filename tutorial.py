import logging

import numpy as np

logger = logging.getLogger("Base")
logging.basicConfig(level=logging.INFO)

from g3_model.FootballModel import FootballModel

football = FootballModel(11, 6, 10, 2)

output = football.determine_scoring_probabilities()

output["prob_B"]

# probabilities seem to be somehow reversed fix tomorrow

output["A"][min(output["A"], key=output["A"].get)]

for i in range(10):
    football.step()

for a, b, c in football.grid.coord_iter():
    print(b)
