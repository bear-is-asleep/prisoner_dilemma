import numpy as np
import matplotlib.pyplot as plt
import json

#MY classes
from agent import factory

class PrisonersDilemma:
    def __init__(self, config, factory):
        """
        Initialize the Prisoner's Dilemma game with a given configuration.

        Parameters
        ----------
        config : dict
            Configuration dictionary containing game parameters.
        factory : AgentFactory
            Factory to create agent instances.
        """
        self.agents = [factory.create(agent['type'], agent['name']) for agent in config['agents']]
        self.payoff_matrix = config['payoff_matrix']
        self.rounds = config['rounds']

    def play_round(self, agent1, agent2):
        """
        Play a round between two agents.

        Parameters
        ----------
        agent1 : Agent
            The first agent.
        agent2 : Agent
            The second agent.
        """
        action1 = agent1.choose_action(agent2.name)
        action2 = agent2.choose_action(agent1.name)

        agent1.update_history(agent2.name, action1, action2)
        agent2.update_history(agent1.name, action2, action1)

        payoff1, payoff2 = self.get_payoffs(action1, action2)
        agent1.update_score(payoff1)
        agent2.update_score(payoff2)

    def get_payoffs(self, action1, action2):
        """
        Get the payoffs for two actions.

        Parameters
        ----------
        action1 : str
            The action of the first agent.
        action2 : str
            The action of the second agent.

        Returns
        -------
        tuple
            Payoffs for the first and second agents.
        """
        return self.payoff_matrix[action1][action2]

    def run(self):
        """
        Run the game for the specified number of rounds.
        """
        for _ in range(self.rounds):
            for i, agent1 in enumerate(self.agents):
                for agent2 in self.agents[i+1:]:
                    self.play_round(agent1, agent2)

    def visualize_games(self,save=False):
        """
        Visualize the history of interactions.
        """
        
        for agent in self.agents:
            for opponent_name, agent_actions in agent.history.items():
                opponent = next(op for op in self.agents if op.name == opponent_name)
                opponent_actions = opponent.history[agent.name]

                # Initialize scores
                agent_scores = [0]
                opponent_scores = [0]

                # Calculate cumulative scores
                for i in range(len(agent_actions)):
                    action1, action2 = agent_actions[i], opponent_actions[i]
                    payoff1, payoff2 = self.get_payoffs(action1, action2)
                    agent_scores.append(agent_scores[-1] + payoff1)
                    opponent_scores.append(opponent_scores[-1] + payoff2)

                rounds = range(len(agent_actions))
                fig,ax = plt.subplots(figsize=(10, 2))

                # Plot agent's actions
                agent_colors = ['green' if action == 'cooperate' else 'red' for action in agent_actions]
                ax.scatter(rounds, [1] * len(agent_actions), c=agent_colors, marker='o', label=f'{agent.name} actions')

                # Plot opponent's actions
                opponent_colors = ['green' if action == 'cooperate' else 'red' for action in opponent_actions]
                ax.scatter(rounds, [0] * len(opponent_actions), c=opponent_colors, marker='x', label=f'{opponent_name} actions')
                
                #Label points with the scores at each point
                for i, txt in enumerate(agent_scores[1:]):
                    ax.annotate(txt, (rounds[i], 1), fontsize=14, xytext=(0, -15), textcoords='offset points')
                for i, txt in enumerate(opponent_scores[1:]):
                    ax.annotate(txt, (rounds[i], 0), fontsize=14, xytext=(0, 15), textcoords='offset points')
                
                # Add labels, legend, and grid
                ax.set_yticks([0.2, 0.8], [opponent_name, agent.name])
                ax.set_xticks([])
                ax.set_xlabel('Round')
                ax.set_title(f"{agent.name} ({agent.label}) vs {opponent_name} ({opponent.label})")
                ax.legend()
                if save:
                    plt.savefig(f"games/{agent.name}_vs_{opponent_name}.png")
                    plt.close(fig)
                else:
                  plt.show()
    def visualize_scores(self):
        """
        Visualize the scores of the agents.
        """
        scores = [agent.score for agent in self.agents]
        names_labels = [f'{agent.name} ({agent.label})' for agent in self.agents]

        fig,ax = plt.subplots(figsize=(10, 5))
        ax.bar(names_labels, scores)
        ax.set_ylabel('Score')
        ax.set_title('Agent Scores')
        plt.show()


def load_config(config_file):
    """
    Load configuration from a file.

    Parameters
    ----------
    config_file : str
        The path to the configuration file.

    Returns
    -------
    dict
        The configuration dictionary.
    """
    with open(config_file, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_config('config.json')
    game = PrisonersDilemma(config,factory)
    game.run()
    game.visualize_games(save=True)
    game.visualize_scores()