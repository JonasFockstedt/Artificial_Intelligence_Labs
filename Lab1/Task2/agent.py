import random
import json


class Agent:
    def __init__(self, agentType):
        self.agentType = agentType
        self.hand = list()
        self.moneyWon = 0
        self.currentBet = 0
        self.wins = 0
        self.cardStrength = 0

    def bet(self):
        if self.agentType == 'random':              # Random agent betting.
            bet = random.randrange(0, 50, 1)        # Random bet between $0-50.
            print(f'{self.agentType} agent bet ${bet}.')
            return bet
        elif self.agentType == 'fixed':             # Fixed agent betting.
            hand = self.calculateHand()
            if hand == 'High cards!':
                bet = 15
            elif hand == 'Two of a kind!':
                bet = 25
            elif hand == 'Three of a kind!':
                bet = 50
            print(f'{self.agentType} agent bet ${bet}.')
            return bet
        elif self.agentType == 'reflex':            # Reflex agent betting.
            # Betting its card strength +8, since 42 is the highest possible value of a
            # hand, and $50 the highest possible betting amount.
            print(f'{self.agentType} agent bet ${self.cardStrength+8}.')
            return self.cardStrength+8

    def revealHand(self):
        print(f'Hand of {self.agentType} agent: {self.hand}.')

    # Possible hands are "three of a kind", "a pair" and "high cards".
    def calculateHand(self):
        ranks = list()
        for card in self.hand:
            for rank in card:
                ranks.append(rank)

        self.calculateStrength(ranks)
        if ranks[0] == ranks[2] == ranks[4]:
            return 'Three of a kind!'
        elif ranks[0] == ranks[2] or ranks[0] == ranks[4] or ranks[2] == ranks[4]:
            return 'Two of a kind!'
        else:
            return 'High cards!'

    def calculateStrength(self, cardList):
        self.cardStrength = 0
        cardValue = 0
        with open(".\\ranks.json") as json_file:
            data = json.load(json_file)

        # Jump every other element in card list since suits are in every other element.
        for card in cardList[::2]:
            if card == 'T':
                cardValue = 10
            elif card == 'J':
                cardValue = 11
            elif card == 'Q':
                cardValue = 12
            elif card == 'K':
                cardValue = 13
            elif card == 'A':
                cardValue = 14
            else:
                cardValue = int(card)

            if cardValue == data['ranks'][card]:
                self.cardStrength += cardValue

    def clear(self):
        self.moneyWon = 0
        self.currentBet = 0
        self.wins = 0
        self.cardStrength = 0
