import numpy as np

class AgentFactory:
    def __init__(self):
        self.agent_classes = {}

    def register(self, name):
        """
        Register an agent class with the factory.

        Parameters
        ----------
        name : str
            The name of the agent class.
        """
        def decorator(agent_class):
            self.agent_classes[name] = agent_class
            return agent_class
        return decorator
            
    def create(self, name, *args, **kwargs):
        """
        Create an instance of a registered agent class.

        Parameters
        ----------
        name : str
            The name of the agent class to instantiate.
        *args
            Positional arguments to pass to the agent constructor.
        **kwargs
            Keyword arguments to pass to the agent constructor.

        Returns
        -------
        Agent
            An instance of the requested agent class.
        """
        if name not in self.agent_classes:
            raise ValueError(f"Agent class '{name}' not registered.")
        return self.agent_classes[name](*args, **kwargs)

#Create instances of the AgentFactory and register the agent classes
factory = AgentFactory()

class Agent:
    def __init__(self, name):
        """
        Initialize an agent with a given name.

        Parameters
        ----------
        name : str
            The name of the agent.
        """
        self.name = name
        self.history = {}
        self.oponent_history = {}
        self.score = 0
        self.label = ''
        self.description = ''
    def __str__(self):
        return f'{self.name} ({self.label}): {self.description}'

    def choose_action(self, opponent_name):
        """
        Choose an action based on the opponent's name.

        Parameters
        ----------
        opponent_name : str
            The name of the opponent agent.

        Returns
        -------
        action : str
            The chosen action ('cooperate' or 'defect').
        """
        pass

    def update_history(self, opponent_name, action, oponent_action):
        """
        Update the interaction history with an opponent.

        Parameters
        ----------
        opponent_name : str
            The name of the opponent agent.
        action : str
            The action taken ('cooperate' or 'defect').
        opponent_action : str
            The action taken by the opponent ('cooperate' or 'defect').
        """
        if opponent_name not in self.history:
            self.history[opponent_name] = []
            self.oponent_history[opponent_name] = []
        self.history[opponent_name].append(action)
        self.oponent_history[opponent_name].append(oponent_action)

    def update_score(self, payoff):
        """
        Update the agent's score based on the payoff.

        Parameters
        ----------
        payoff : int
            The payoff received in the current interaction.
        """
        self.score += payoff

@factory.register('TitForTat')
class TitForTatAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.label = 'TFT'
        self.description = 'Cooperates on the first move, then mimics the opponent\'s previous move.'
    def choose_action(self, opponent_name):
        """
        Choose an action based on the opponent's name.

        Parameters
        ----------
        opponent_name : str
            The name of the opponent agent.

        Returns
        -------
        action : str
            The chosen action ('cooperate' or 'defect').
        """
        if opponent_name in self.history:
            return self.oponent_history[opponent_name][-1]
        return 'cooperate'

@factory.register('Random')
class RandomAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.label = 'R'
        self.description = 'Randomly chooses to cooperate or defect.'
    def choose_action(self, opponent_name):
        """
        Choose an action based on the opponent's name.

        Parameters
        ----------
        opponent_name : str
            The name of the opponent agent.

        Returns
        -------
        action : str
            The chosen action ('cooperate' or 'defect').
        """
        return np.random.choice(['cooperate', 'defect'])

@factory.register('TitForTwoTats')
class TitForTwoTatsAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.label = 'TF2T'
        self.description = 'Cooperates until the opponent defects twice in a row, then defects.'
    def choose_action(self, opponent_name):
        """
        Choose an action based on the opponent's name.

        Parameters
        ----------
        opponent_name : str
            The name of the opponent agent.

        Returns
        -------
        action : str
            The chosen action ('cooperate' or 'defect').
        """
        if opponent_name in self.history:
            if len(self.history[opponent_name]) >= 2:
                if self.oponent_history[opponent_name][-1] == 'defect' and self.oponent_history[opponent_name][-2] == 'defect':
                    return 'defect'
        return 'cooperate'

@factory.register('Grudger')
class GrudgerAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.label = 'G'
        self.description = 'Cooperates until the opponent defects, then defects for the rest of the game.'
    def choose_action(self, opponent_name):
        """
        Choose an action based on the opponent's name.

        Parameters
        ----------
        opponent_name : str
            The name of the opponent agent.

        Returns
        -------
        action : str
            The chosen action ('cooperate' or 'defect').
        """
        if opponent_name in self.history:
            if 'defect' in self.oponent_history[opponent_name]:
                return 'defect'
        return 'cooperate'

@factory.register('Cooperator')
class CooperatorAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.label = 'C'
        self.description = 'Always cooperates.'
    def choose_action(self, opponent_name):
        """
        Choose an action based on the opponent's name.

        Parameters
        ----------
        opponent_name : str
            The name of the opponent agent.

        Returns
        -------
        action : str
            The chosen action ('cooperate' or 'defect').
        """
        return 'cooperate'

@factory.register('Defector')
class DefectorAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.label = 'D'
        self.description = 'Always defects.'
    def choose_action(self, opponent_name):
        """
        Choose an action based on the opponent's name.

        Parameters
        ----------
        opponent_name : str
            The name of the opponent agent.

        Returns
        -------
        action : str
            The chosen action ('cooperate' or 'defect').
        """
        return 'defect'



