import random

class Agent:
    def __init__(self, agentType):
        self.agentType = agentType
        self.hand = list()
        self.moneyWon = 0
        self.currentBet = 0

    def bet(self):
        if self.agentType == 'random':
            bet = random.randrange(0,50,1)      # Random bet between $0-50.
            print(f'{self.agentType} agent bet ${bet}.')
            return bet
        elif self.agent.agentType == 'reflex':

            print(f'{self.agentType} agent bet ${bet}.')