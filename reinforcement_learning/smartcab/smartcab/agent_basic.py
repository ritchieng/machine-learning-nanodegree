import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(
            env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        # Trials for plotting
        self.trials = -1
        self.max_trials = 100
        self.x_trials = range(0, self.max_trials)
        self.y_trials = range(0, self.max_trials)

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.trials = self.trials + 1

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state

        # TODO: Select action according to your policy
        # random.choice(list) chooses a random element from the list
        # We can access the list through Environment.valid_actions since
        # valid_actions = [None, 'forward', 'left', 'right']
        action = random.choice(Environment.valid_actions)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward

        if (deadline == 0) & (reward < 10):
            self.y_trials[self.trials] = 0
        else:
            self.y_trials[self.trials] = 1


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

    # print Q table
    import matplotlib.pyplot as plt
    plt.figure()
    plt.scatter(a.x_trials, a.y_trials)
    plt.legend()
    plt.xlabel('Trial Number')
    plt.ylabel('Successful = 1, Unsuccessful = 0')
    plt.title("Training Graph: Successful or Unsuccessful")
    plt.show()

    # Success rate
    print a.y_trials.count(1)

if __name__ == '__main__':
    run()