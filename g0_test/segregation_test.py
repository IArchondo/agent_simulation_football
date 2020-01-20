from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.WARN)

logger = logging.getLogger("SegregationSimulator")


class SegregationAgent(Agent):
    def __init__(self, unique_id, ethnicity, happiness_threshold, model):
        super().__init__(unique_id, model)

        self.unique_id = unique_id
        self.happy = 0
        self.ethnicity = ethnicity
        self.happiness_threshold = happiness_threshold

    def move(self):
        """Move agent to other place on the board
        """
        # TODO do this more iteratively
        random_empty_cell = self.model.grid.find_empty()

        self.model.grid.move_agent(self, random_empty_cell)
        logger.info("Agent moved to cell " + str(random_empty_cell))

    def calculate_same_neighbors(self):
        """Calculate neighbors that are from the same ethnicity
        
        Returns:
            int: Number of same ethnicity neighbors
        """
        neighbors = self.model.grid.get_neighbors(
            pos=self.pos, moore=True, include_center=False, radius=1
        )
        same_eth = sum([neighbor.ethnicity == self.ethnicity for neighbor in neighbors])

        logger.info("Agent has " + str(same_eth) + " neighbors from same ethnicity")
        return same_eth

    def evaluate_neighbors(self, same_neighbors):
        """Evaluate neighbors and change happiness state
        
        Args:
            same_neighbors (int): Number of neighbors with same ethniicty
        """
        if same_neighbors >= self.happiness_threshold:
            self.happy = 1
            state = "happy"
        else:
            self.happy = 0
            state = "unhappy"

        logger.info("Agent is " + str(state))

    def step(self):
        """Step function. If happiness state sad, move
        """
        logger.info("Agent " + str(self.unique_id) + " activated")
        same_neighbors = self.calculate_same_neighbors()
        self.evaluate_neighbors(same_neighbors)
        if self.happy == 1:
            return
        else:
            self.move()


def overall_happiness(model):
    agent_happiness = sum([agent.happy for agent in model.schedule.agents])

    return agent_happiness


class SegregationModel(Model):
    def __init__(
        self, number_of_agents, width, height, happiness_threshold, minority_rate
    ):
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)

        ## Create Agents
        number_of_minority = round(number_of_agents * (minority_rate))
        for i in range(number_of_agents):
            if (i + 1) <= number_of_minority:
                ethnicity = 1
            else:
                ethnicity = 2
            a = SegregationAgent(i, ethnicity, happiness_threshold, self)
            self.schedule.add(a)

            # place agent on grid
            # x = self.random.randrange(self.grid.width)
            # y = self.random.randrange(self.grid.height)
            empty_place = self.grid.find_empty()
            self.grid.place_agent(a, empty_place)
            logger.info("Agent " + str(i) + " placed in " + str(empty_place))

        self.datacollector = DataCollector(
            agent_reporters={"Happiness": "happy"},
            model_reporters={"Overall_happiness": overall_happiness},
        )

    def plot_grid(self):
        ethnicities = np.zeros((self.grid.width, self.grid.height))

        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            agent_present = len(cell_content)
            if agent_present > 0:
                cell_content = list(cell_content)
                ethnicities[x][y] = cell_content[0].ethnicity

        plt.imshow(ethnicities, interpolation="nearest")
        plt.colorbar()
        plt.show()

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.plot_grid()


model = SegregationModel(85, 10, 10, 3, 0.5)

for i in range(20):
    model.step()

model.datacollector.get_model_vars_dataframe().plot()
