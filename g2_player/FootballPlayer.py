import logging

from mesa import Agent

logger = logging.getLogger("FootballPlayer")


class FootballPlayer(Agent):
    def __init__(self, unique_id, team):
        super().__init__(unique_id, model)

        self.unique_id = unique_id
        self.team = team
        self.has_ball = False

        if self.team == "A":
            self.movement_direction = 1

        if self.team == "B":
            self.movement_direction = -1

    def move_forward(self):
        """Move forward one position
        """
        current_position = self.pos
        new_position = current_position.copy()
        new_position[1] = new_position[1] + self.movement_direction

        self.model.grid.move_agent(self, random_empty_cell)
        logger.info("Player moved forward to cell " + str(new_position))

    def check_forward(self):
        """Check if an opposing player is in front of player
        
        Returns:
            boolean: True if an opposing player is in front
        """
        current_position = self.pos
        forward_position = current_position.copy()
        forward_position[1] = forward_position[1] + self.movement_direction

        forward_cell = self.model.grid.get_cell_list_contents(forward_position)
        forward_cell = list(forward_cell)

        if len(forward_cell) > 1:
            if forward_cell[0].team != self.team:
                logger.debug("Opposing player is in front")
                return True

            else:
                logger.debug("Teammate is in front")
                return False

        else:
            logger.debug("No one is in front")
            return False

    def step(self):
        logger.info("Agent " + str(self.unique_id) + " activated")
        if self.check_forward():
            self.move_forward
