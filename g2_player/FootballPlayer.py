import logging

from mesa import Agent

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

    def __is_not_on_border(self):
        if ((self.team == "A") & (self.pos[1] + 1 == self.model.grid.height)) | (
            (self.team == "B") & (self.pos[1] == 0)
        ):
            return False
        else:
            return True

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

        else:
            logger.info("No one is in front")
            return True

    def step(self):
        logger.info(
            "Agent " + str(self.unique_id) + " activated on cell: " + str(self.pos)
        )
        if self.__is_not_on_border():
            if self.check_forward():
                self.move_forward()
        else:
            logger.info("Agent has reached edge of pitch")
