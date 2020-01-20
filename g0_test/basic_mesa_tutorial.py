from mesa import Agent, Model
from mesa.time import RandomActivation
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("BasicExec")


class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # TODO: check exactly how super works
        self.wealth = 1
        self.unique_id = unique_id
        logger.info("Agent " + str(unique_id) + " created")

    def step(self):
        # what the agent is going to do when activated
        logger.info("Agent " + str(self.unique_id) + " activated")
        if self.wealth == 0:
            logger.info("Agent has no money to give")
            return
        other_agent = self.random.choice(self.model.schedule.agents)
        other_agent.wealth = other_agent.wealth + 1
        self.wealth = self.wealth - 1
        logger.info("Agent gave one coin to agent " + str(other_agent.unique_id))


class MoneyModel(Model):
    def __init__(self, number_of_agents):
        self.num_agents = number_of_agents
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(number_of_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

    def step(self):
        # Advance the model by one step
        self.schedule.step()

    def check_agent_status(self):
        for i in range(len(self.schedule.agents)):
            id = self.schedule.agents[i].unique_id
            wealth = self.schedule.agents[i].wealth
            logger.info("Agent " + str(id) + " has money: " + str(wealth))


model = MoneyModel(6)

model.step()

model.check_agent_status()

model.schedule.agents[0].pos

#### Adding spatial dimension

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("BasicExec")


class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # TODO: check exactly how super works
        self.wealth = 1
        self.unique_id = unique_id
        logger.info("Agent " + str(unique_id) + " created")

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        logger.info(
            "Agent "
            + str(self.unique_id)
            + " moved from "
            + str(self.pos)
            + " to "
            + str(new_position)
        )
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth = other.wealth + 1
            self.wealth -= 1
            logger.info("Agent gave money to neighbor " + str(other.unique_id))

    def step(self):
        self.move()
        if self.wealth == 0:
            logger.info("No money to give")
        elif self.wealth > 0:
            self.give_money()


class MoneyModel(Model):
    def __init__(self, number_of_agents, width, height):
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(number_of_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            ## place agent on grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def plot_grid(self):
        agent_counts = np.zeros((self.grid.width, model.grid.height))

        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            agent_count = len(cell_content)
            agent_counts[x][y] = agent_count

        plt.imshow(agent_counts, interpolation="nearest")
        plt.colorbar()
        plt.show()

    def step(self):
        # Advance the model by one step
        self.schedule.step()
        self.plot_grid()

    def check_agent_status(self):
        for i in range(len(self.schedule.agents)):
            id = self.schedule.agents[i].unique_id
            wealth = self.schedule.agents[i].wealth
            logger.info("Agent " + str(id) + " has money: " + str(wealth))


model = MoneyModel(6, 3, 3)

model.step()

model.check_agent_status()

#### Adding data collector

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("BasicExec")


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B


class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # TODO: check exactly how super works
        self.wealth = 1
        self.unique_id = unique_id
        logger.info("Agent " + str(unique_id) + " created")

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        logger.info(
            "Agent "
            + str(self.unique_id)
            + " moved from "
            + str(self.pos)
            + " to "
            + str(new_position)
        )
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth = other.wealth + 1
            self.wealth -= 1
            logger.info("Agent gave money to neighbor " + str(other.unique_id))

    def step(self):
        self.move()
        if self.wealth == 0:
            logger.info("No money to give")
        elif self.wealth > 0:
            self.give_money()


class MoneyModel(Model):
    def __init__(self, number_of_agents, width, height):
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(number_of_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            ## place agent on grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

            # start datacollector
            self.datacollector = DataCollector(
                model_reporters={"Gini": compute_gini},
                agent_reporters={"Wealth": "wealth"},
            )

    def plot_grid(self):
        agent_counts = np.zeros((self.grid.width, model.grid.height))

        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            agent_count = len(cell_content)
            agent_counts[x][y] = agent_count

        plt.imshow(agent_counts, interpolation="nearest")
        plt.colorbar()
        plt.show()

    def step(self):
        # Advance the model by one step
        self.datacollector.collect(self)
        self.schedule.step()
        self.plot_grid()

    def check_agent_status(self):
        for i in range(len(self.schedule.agents)):
            id = self.schedule.agents[i].unique_id
            wealth = self.schedule.agents[i].wealth
            logger.info("Agent " + str(id) + " has money: " + str(wealth))


model = MoneyModel(6, 3, 3)
for i in range(10):
    model.step()

gini = model.datacollector.get_model_vars_dataframe()

gini.plot()

model.datacollector.get_agent_vars_dataframe()

model.check_agent_status()

