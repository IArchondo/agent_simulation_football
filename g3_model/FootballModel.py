from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from g2_player.FootballPlayer import FootballPlayer

import logging
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger("FootballModel")


class FootballModel(Model):
    def __init__(self, players_per_team, width, height, goals_to_win):
        self.players_per_team = players_per_team
        self.grid = SingleGrid(width, height, False)
        # TODO: change so it only activates player with ball
        self.schedule = RandomActivation(self)

        ## Create Agents
        # generate_ids
        self.ids_team_a = ["A_" + str(id) for id in range(self.players_per_team)]
        self.ids_team_b = ["B_" + str(id) for id in range(self.players_per_team)]
        self.ids = self.ids_team_a + self.ids_team_b

        for i in range(len(self.ids)):
            player = FootballPlayer(
                unique_id=self.ids[i], team=self.ids[i][0], model=self
            )

            self.schedule.add(player)

            ## Place agent on grid
            # TODO this should be later be improved to create a formation of some sorts
            empty_place = self.grid.find_empty()
            self.grid.place_agent(player, empty_place)
            logger.info("Agent " + str(self.ids[i]) + " placed in " + str(empty_place))

    def plot_grid(self):
        # TODO add way to know where the ball is
        teams = np.zeros((self.grid.width, self.grid.height))

        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if cell_content != None:
                if cell_content.team == "A":
                    teams[x][y] = 1
                if cell_content.team == "B":
                    teams[x][y] = 2

        plt.imshow(teams, interpolation="nearest")
        plt.colorbar()
        plt.show()

    def step(self):
        self.schedule.step()
        self.plot_grid()
