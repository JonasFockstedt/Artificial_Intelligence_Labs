import agent
import random

totalPot = 0

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}
rank = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suit = ['s', 'h', 'd', 'c']
deck = list()


def generateDeck():
    global deck
    index = 1
    for cardRank in rank:
        for cardSuit in suit:
            deck.append(rank[cardRank]+suit[cardSuit])
            
    random.shuffle(deck)


def assignHand(agent):
    rank.pop(random.randrange(0,12))
    print(f'Hand dealt to {agent.agentType} agent')


# Main.
if __name__ == '__main__':
    randomAgent = agent.Agent('random')
    totalPot += randomAgent.bet()
    print(f'Total pot: ${totalPot}')
    assignHand(randomAgent)
    testHand = rank[0] + suit[0]
    print(testHand)
    generateDeck()
    for card in deck:
        print(deck[card])