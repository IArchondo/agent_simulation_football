import logging
import math
import random
import numpy as np

from mesa import Agent
from g1_utils.utils import cap_value, calculate_distance_two_points, apply_linear_model

logger = logging.getLogger("FootballPlayer")


class FootballPlayer(Agent):
    def __init__(self, unique_id, team, model):
        super().__init__(unique_id, model)

        self.unique_id = unique_id
        self.team = team
        self.has_ball = False

        if self.team == "A":
            self.movement_direction = 1

        if self.team == "B":
            self.movement_direction = -1

    def __is_on_border(self):
        if ((self.team == "A") & (self.pos[1] + 1 == self.model.grid.height)) | (
            (self.team == "B") & (self.pos[1] == 0)
        ):
            return True
        else:
            return False

    def __count_surrounding_opposing_players(self, player):
        """Count the opposing player's in a player's vicinity
        
        Args:
            player (g2_player.FootballPlayer.FootballPlayer): input player
        
        Returns:
            int: Number of opposing players in vicinity (min 0 - max 8)
        """

        neighbors = self.model.grid.get_neighbors(
            pos=player.pos, moore=True, include_center=False, radius=1
        )

        opposing_players = sum([neighbor.team != player.team for neighbor in neighbors])

        logger.debug(
            "Player "
            + str(player.unique_id)
            + " has "
            + str(opposing_players)
            + " opposing players in his surroundings"
        )
        return opposing_players

    def __give_ball_to_player(self, receiving_player_id):
        """give ball to a given player
        
        Args:
            receiving_player_id (str): Id of the receiving player
        
        Raises:
            Exception: checks if player has the ball
        """
        if self.has_ball:
            # stop having ball
            self.has_ball = False
            # make receiving player have ball
            receiving_player_index = self.model.id_dict[receiving_player_id]
            receiving_player_pos = self.model.schedule.agents[
                receiving_player_index
            ].pos
            self.model.schedule.agents[receiving_player_index].has_ball = True

            logger.info(
                "Passed ball to player "
                + str(receiving_player_id)
                + " in position "
                + str(receiving_player_pos)
            )
        else:
            logger.error("Player does not have ball, so he can't pass it")
            raise Exception("Player does not have ball")

    def calculate_passing_probabilities(self):
        """Calculate probability of a succesful pass for each teammate
        
        Returns:
            dict: Dict with passing, interception and general probabilities
        """
        # determine distance to each teammate
        teammates = [
            player
            for player in self.model.schedule.agents
            if (player.team == self.team) and (player.unique_id != self.unique_id)
        ]

        passing_distances = {
            player: calculate_distance_two_points(self.pos, player.pos)
            for player in teammates
        }

        passing_probabilities = {
            player: apply_linear_model(
                passing_distances[player], self.model.distance_model
            )
            for player in teammates
        }

        # TODO 0.25 should be possible to alter via a yaml file
        interception_probabilities = {
            player: cap_value(
                0.25 * self.__count_surrounding_opposing_players(player), 1
            )
            for player in teammates
        }

        # TODO closeness to goal should be also taken into account
        general_probability = {
            player: passing_probabilities[player]
            * (1 - interception_probabilities[player])
            for player in teammates
        }

        ## Decide chosen pass candidate
        max_prob = general_probability[
            max(general_probability, key=general_probability.get)
        ]

        decision_candidates = [
            player.unique_id
            for player in general_probability.keys()
            if general_probability[player] == max_prob
        ]

        decision = random.choice(decision_candidates)

        output_dict = {
            player.unique_id: {
                "passing": passing_probabilities[player],
                "interception": interception_probabilities[player],
                "general": general_probability[player],
            }
            for player in teammates
        }

        ## attach chosen pass candidate
        output_dict["decision"] = decision

        return output_dict

    def move_forward(self):
        """Move forward one position
        """
        current_position_x = self.pos[0]
        current_position_y = self.pos[1]
        new_position = (
            current_position_x,
            current_position_y + self.movement_direction,
        )

        self.model.grid.move_agent(self, new_position)
        logger.info("Player moved forward to cell " + str(new_position))

    def check_forward(self):
        """Check if an opposing player is in front of player
        
        Returns:
            boolean: False if an opposing player is in front
        """
        current_position_x = self.pos[0]
        current_position_y = self.pos[1]
        forward_position = (
            current_position_x,
            current_position_y + self.movement_direction,
        )
        logger.info("Checking grid in " + str(forward_position))
        forward_cell = self.model.grid.get_cell_list_contents(forward_position)
        logger.debug("Found " + str(forward_cell))
        forward_cell = list(forward_cell)

        if len(forward_cell) > 0:
            if forward_cell[0].team != self.team:
                logger.info("Opposing player is in front")
                return False

            else:
                logger.info("Teammate is in front")
                return False

        elif self.__is_on_border():
            logger.info("Player has reached the edge of the pitch")
            return False

        else:
            return True

    def intent_pass_ball_to_player(self, receiving_player_id, success_probability):
        """ Try a pass to a given player, if missed, nearest opposing player receives ball
        
        Args:
            receiving_player_id (str): Intended receiving player
            success_probability (float): probabilities of pass to succeed 
        """

        ## calculate distance of receiving player with all opponents
        receiving_player = self.model.schedule.agents[
            self.model.id_dict[receiving_player_id]
        ]

        opposition = [
            player
            for player in self.model.schedule.agents
            if (player.team != self.team)
        ]

        distances = {
            player.unique_id: calculate_distance_two_points(
                receiving_player.pos, player.pos
            )
            for player in opposition
        }

        # choose neares opponent as possible pass receipient
        closest_opp = distances[min(distances, key=distances.get)]

        closest_players = [
            player.unique_id
            for player in opposition
            if distances[player.unique_id] == closest_opp
        ]

        pressing_player = random.choice(closest_players)

        # draw an outcome at random with given probability
        passing_options = [receiving_player_id, pressing_player]

        passing_probs = [success_probability, 1 - success_probability]

        rng = np.random.default_rng()

        outcome = rng.multinomial(1, passing_probs, 1).tolist()[0]

        ## give ball to winning player
        winning_player = passing_options[
            [i for i, x in enumerate(outcome) if x == 1][0]
        ]

        if outcome[0] == 0:
            logger.info("Ball lost")
            logger.info("Stolen by " + str(winning_player))
        if outcome[0] == 1:
            logger.info("Successful pass")
            logger.info("Received by " + str(winning_player))

        self.__give_ball_to_player(winning_player)

    def look_to_pass_ball(self):
        """Evaluate passing candidates, choose one and intend a pass
        """
        passing_prob = self.calculate_passing_probabilities()

        chosen_candidate = passing_prob["decision"]
        probabilities = passing_prob[chosen_candidate]["general"]

        self.intent_pass_ball_to_player(chosen_candidate, probabilities)

    def step(self):
        # TODO move all stepping forward into stepping forward
        logger.info(
            "Agent " + str(self.unique_id) + " activated on cell: " + str(self.pos)
        )

        if self.check_forward():
            self.move_forward()

        else:
            self.look_to_pass_ball()

