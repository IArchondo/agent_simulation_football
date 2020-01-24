import logging

logger = logging.getLogger("Base")
logging.basicConfig(level=logging.INFO)

from g3_model.FootballModel import FootballModel
from g4_animations.AnimationGenerator import AnimationGenerator

football = FootballModel(10, 9, 13, 60)
# 9 13

football.simulate_whole_game(True, save_plots=False)

anima = AnimationGenerator(football.game_id)

anima.execute_whole_process(duration_input=1.1)
