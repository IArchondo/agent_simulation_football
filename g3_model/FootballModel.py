from mesa import Model

# TODO activate player with ball
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from g1_utils.utils import calculate_distance_two_points, train_linear_two_points
from g2_player.FootballPlayer import FootballPlayer

import logging
import random
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger("FootballModel")


class FootballModel(Model):
    def __init__(self, players_per_team, width, height, goals_to_win):
        self.players_per_team = players_per_team

        self.grid = SingleGrid(width, height, False)
        self.distance_model = self.__train_distance_model()

        # TODO: change so it only activates player with ball
        self.schedule = RandomActivation(self)

        ## Create Agents
        # generate_ids
        self.ids_team_a = ["A_" + str(id) for id in range(self.players_per_team)]
        self.ids_team_b = ["B_" + str(id) for id in range(self.players_per_team)]
        self.ids = self.ids_team_a + self.ids_team_b
        # TODO since id is still only an integer, make a dict between real ids and integers

        self.id_dict = {}
        for i in range(len(self.ids)):
            # Create dict linking real ids to used ids
            self.id_dict[self.ids[i]] = i

            player = FootballPlayer(
                unique_id=self.ids[i], team=self.ids[i][0], model=self
            )

            self.schedule.add(player)

            ## Place agent on grid
            # TODO this should be later be improved to create a formation of some sorts
            empty_place = self.grid.find_empty()
            self.grid.place_agent(player, empty_place)
            logger.info("Agent " + str(self.ids[i]) + " placed in " + str(empty_place))

        # Give the ball to a player
        ball_options = self.__determine_furthest_back_per_team()
        kickoff_team = random.choice(list(ball_options.keys()))
        chosen_player = ball_options[kickoff_team]

        logger.info("Team " + str(kickoff_team) + " wins the coin toss")
        self.schedule.agents[self.id_dict[chosen_player]].has_ball = True
        logger.info("Ball given to player " + str(chosen_player))

        self.plot_grid()

    def __train_distance_model(self):
        """Calculates the maximum distance in the pitch and trains a linear model
            to determine passing accuracy-distance ratio

        Returns:
            dict: dict with slope and intercept
        """

        max_distance = calculate_distance_two_points(
            (0, 0), (self.grid.width, self.grid.height)
        )

        output_dict = train_linear_two_points((1, 0.95), (max_distance, 0.1))

        return output_dict

    def __determine_furthest_back_per_team(self):
        """Determine player that is furthest back for each team
        
        Returns:
            dict: Dict with teams as keys and player id as value
        """
        pos_dict = {agent.unique_id: agent.pos[1] for agent in self.schedule.agents}

        team_A = {key: pos_dict[key] for key in pos_dict.keys() if key[0] == "A"}
        team_B = {key: pos_dict[key] for key in pos_dict.keys() if key[0] == "B"}

        # Calcualte min value for positions in each team
        min_A = team_A[min(team_A, key=team_A.get)]
        min_B = team_B[max(team_B, key=team_B.get)]

        # # Get players located in such value
        players_A = [key for key in team_A.keys() if pos_dict[key] == min_A]
        players_B = [key for key in team_B.keys() if pos_dict[key] == min_B]

        # Return random player from list
        output_dict = {
            "A": random.choice(players_A),
            "B": random.choice(players_B),
        }

        return output_dict

    def who_has_ball(self):
        """Determine which player has the ball
        
        Returns:
            int: Index of player who has ball
        """
        has_ball = [agent.has_ball for agent in self.schedule.agents]
        index_has_ball = [i for i, x in enumerate(has_ball) if x]
        if len(index_has_ball) == 1:
            id_has_ball = [
                key
                for key in self.id_dict.keys()
                if self.id_dict[key] == index_has_ball[0]
            ]
            return {
                "index": index_has_ball[0],
                "id": id_has_ball[0],
                "player": self.schedule.agents[index_has_ball[0]],
            }

        elif len(index_has_ball) == 0:
            logger.error("No one has ball")

        else:
            logger.error("More than one player has the ball")

    def plot_grid(self):
        # gather ball position
        ball_coord = self.who_has_ball()["player"].pos
        ball_coord_x = ball_coord[0]
        ball_coord_y = ball_coord[1]
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
        # plot ball
        plt.scatter(ball_coord_y, ball_coord_x, c="black")
        plt.show()

    def step(self):
        self.who_has_ball()["player"].step()
        self.plot_grid()
