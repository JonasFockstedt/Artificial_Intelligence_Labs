import agent
import random

totalPot = 0

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}
deck = list()
randomAgent = agent.Agent('random')
fixedAgent = agent.Agent('fixed')

'''ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['s', 'h', 'd', 'c']'''


def generateDeck():
    global deck
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['s', 'h', 'd', 'c']

    for cardSuit in suits:
        for cardRank in ranks:
            deck.append(cardRank+cardSuit)

    random.shuffle(deck)    # Shuffles deck.


def assignHand(agent):
    global deck
    for cardNumber in range(0, 3):      # Hand three cards to the agent.
        agent.hand.append(deck.pop())
    agent.hand.sort()
    print(f'Hand dealt to {agent.agentType} agent.')


def compareHands(firstAgent, secondAgent):
    global totalPot
    if firstAgent.calculateHand() and secondAgent.calculateHand() == 'High cards!':
        handTuple = tuple(zip(firstAgent.hand, secondAgent.hand))
        for index in handTuple:
            if index[0] > index[1]:
                assignWin(firstAgent)
                break
            else:
                assignWin(secondAgent)
                break


def assignWin(agent):
    global totalPot
    print(f'{agent.agentType} agent wins!')
    agent.moneyWon = totalPot
    totalPot = 0
    print()


def biddingPhase():
    global totalPot
    for x in range(1, 4):
        print(f'Bidding phase {x}:')
        totalPot += randomAgent.bet()
        totalPot += fixedAgent.bet()
        print()


def cardDealingPhase():
    print('Card dealing phase:')
    assignHand(randomAgent)
    assignHand(fixedAgent)
    randomAgent.revealHand()
    fixedAgent.revealHand()


    # Main.
if __name__ == '__main__':
    generateDeck()
    cardDealingPhase()
    print()

    '''assignHand(randomAgent)
    assignHand(fixedAgent)
    totalPot += randomAgent.bet()
    totalPot += fixedAgent.bet()
    randomAgent.revealHand()
    fixedAgent.revealHand()'''
    biddingPhase()
    print()

    randomAgent.calculateHand()
    fixedAgent.calculateHand()
    print(f'Total pot: ${totalPot}')
    compareHands(randomAgent, fixedAgent)
    print(f'{randomAgent.agentType} agent has won ${randomAgent.moneyWon}.')
    print(f'{fixedAgent.agentType} agent has won ${fixedAgent.moneyWon}.')
