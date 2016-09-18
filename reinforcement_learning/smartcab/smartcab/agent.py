import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here

        # Initialize Q-table
        # One dimension for state, another dimension for actions
        # By doing so, you can just map the corresponding state to choose action in the future
        self.Q = {}
        for i in ['green', 'red']:
            for j in [None, 'forward', 'left', 'right']:
                for k in self.env.valid_actions:
                    self.Q[(i, j, k)] = [4] * len(self.env.valid_actions)

        # Initialize basic parameters of the Q-learning equation
        # Learning rate
        self.alpha = 0.8
        # Discount rate
        self.gamma = 0.2
        # Simulated annealing
        self.epsilon = 1
        self.p = random.randrange(0, 100)
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
        # These are the valid inputs from valid_inputs in the class Environment in environment.py
        # 'light', 'oncoming', 'left', 'right'
        # Using 'light' and next_waypoint,  we've tuples here
        self.state = (inputs['light'], inputs['oncoming'], self.next_waypoint)

        # TODO: Select action according to your policy

        # 1. We can find the action corresponding to the maximum value of Q for the current state
        # self.Q[self.state] accesses the current state
        # index(max(self.Q[self.state])) maximizes the value of Q for that state
        max_Q = self.Q[self.state].index(max(self.Q[self.state]))

        # 2. Then we select the action to maximize the value of Q

        # "Simulated annealing"
        # to allow the agent to still explore the environment
        # and not just still the the most conservative approach
        # It is a probabilistic technique for approximating the global optimum of a given function

        # This implies epsilon (probability of random action) is 1%
        # 0 and 1 can be the only values less than epsilon, 2
        if self.p < self.epsilon:
            action = random.choice(self.env.valid_actions)
        else:
            action = self.env.valid_actions[max_Q]

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward

        # Now we want the subsequent pair of state and action, Q(s',a')
        subse_inputs = self.env.sense(self)
        subse_next_waypoint = self.planner.next_waypoint()
        subse_state = (subse_inputs['light'], subse_inputs['oncoming'], subse_next_waypoint)

        # Update our Q table
        q_old = self.Q[self.state][self.env.valid_actions.index(action)]
        q_subse_utility = reward + self.gamma * max(self.Q[subse_state])
        self.Q[self.state][self.env.valid_actions.index(action)] = \
            (1 - self.alpha) * q_old + (self.alpha * q_subse_utility)

        # Determine if trial is successful (1) or not (0)
        if (deadline == 0) & (reward < 10):
            self.y_trials[self.trials] = 0
        else:
            self.y_trials[self.trials] = 1

        # print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)


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
    # import matplotlib.pyplot as plt
    # plt.figure()
    # plt.scatter(a.x_trials, a.y_trials)
    # plt.legend()
    # plt.xlabel('Trial Number')
    # plt.ylabel('Successful = 1, Unsuccessful = 0')
    # plt.title("Training Graph: Successful or Unsuccessful (With Improvements)")
    # plt.show()

    # print a.y_trials
    # This is a list
    # print type(a.y_trials)

    success_rate = a.y_trials.count(1)
    print success_rate

    # print a.Q
    # This is a dictionary
    # We can loop through to print
    for key in a.Q:
        print key,
        print ["%0.2f" % i for i in a.Q[key]]

if __name__ == '__main__':
    run()