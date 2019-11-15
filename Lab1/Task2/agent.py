import random


class Agent:
    def __init__(self, agentType):
        self.agentType = agentType
        self.hand = list()
        self.moneyWon = 0
        self.currentBet = 0
        self.wins = 0

    def bet(self):
        if self.agentType == 'random':              # Random agent betting.
            bet = random.randrange(0, 50, 1)        # Random bet between $0-50.
            print(f'{self.agentType} agent bet ${bet}.')
            return bet
        elif self.agentType == 'fixed':      # Fixed agent betting.
            hand = self.calculateHand()
            if hand == 'High cards!':
                bet = 15
            elif hand == 'Two of a kind!':
                bet = 25
            elif hand == 'Three of a kind!':
                bet = 50
            print(f'{self.agentType} agent bet ${bet}.')
            return bet

    def revealHand(self):
        print(f'Hand of {self.agentType} agent: {self.hand}.')

    # Possible hands are "three of a kind", "a pair" and "high cards".
    def calculateHand(self):
        ranks = list()
        for card in self.hand:
            for rank in card:
                ranks.append(rank)

        if ranks[0] == ranks[2] == ranks[4]:
            return 'Three of a kind!'
        elif ranks[0] == ranks[2] or ranks[0] == ranks[4] or ranks[2] == ranks[4]:
            return 'Two of a kind!'
        else:
            return 'High cards!'
