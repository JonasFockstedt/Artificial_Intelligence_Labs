import agent
import random

totalPot = 0

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}
deck = list()


def generateDeck():
    global deck
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['s', 'h', 'd', 'c']
    index = 0
    for cardSuit in suits:
        print(cardSuit)
        for cardRank in ranks:
            deck.append(cardRank+cardSuit)

    random.shuffle(deck)


def assignHand(agent):
    #ranks.pop(random.randrange(0, 12))
    print(f'Hand dealt to {agent.agentType} agent')


# Main.
if __name__ == '__main__':
    randomAgent = agent.Agent('random')
    totalPot += randomAgent.bet()
    print(f'Total pot: ${totalPot}')
    assignHand(randomAgent)
    #testHand = ranks[0] + suits[0]
    # print(testHand)
    generateDeck()
    for card in deck:
        print(card)
