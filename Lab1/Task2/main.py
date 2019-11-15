import agent
import random

totalPot = 0

# Rank: {2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A}
# Suit: {s, h, d, c}
deck = list()
randomAgent = agent.Agent('random')
fixedAgent = agent.Agent('fixed')
reflexAgent = agent.Agent('reflex')

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
    if firstAgent.calculateHand() and secondAgent.calculateHand() == 'High cards!' or 'Two of a kind!' or 'Three of a kind!':
        handTuple = tuple(zip(firstAgent.hand, secondAgent.hand))
        for index in handTuple:
            if index[0] > index[1]:
                assignWin(firstAgent)
                break
            elif index[0] < index[1]:
                assignWin(secondAgent)
                break


def assignWin(agent):
    global totalPot
    print(f'{agent.agentType} agent wins!')
    agent.moneyWon += totalPot
    agent.wins += 1
    totalPot = 0
    print()


def cardDealingPhase(firstAgent, secondAgent):
    print('Card dealing phase:')
    generateDeck()
    resetHands(firstAgent, secondAgent)
    assignHand(firstAgent)
    assignHand(secondAgent)


def biddingPhase(firstAgent, secondAgent):
    global totalPot
    for x in range(1, 4):
        print(f'Bidding phase {x}:')
        totalPot += firstAgent.bet()
        totalPot += secondAgent.bet()
        print()


def showdownPhase(firstAgent, secondAgent):
    firstAgent.revealHand()
    secondAgent.revealHand()
    compareHands(firstAgent, secondAgent)


def resetHands(firstAgent, secondAgent):
    firstAgent.hand.clear()
    secondAgent.hand.clear()

    # Main.
if __name__ == '__main__':
    randomVFixedWinner = 0
    randomVFixedDiff = 0
    randomVReflexWinner = 0
    randomVReflexDiff = 0
    fixedVReflexWinner = 0
    fixedVReflexDiff = 0

    print(f'Game between random and fixed agent:')
    for number in range(0, 50):
        print(f'Round {number}.')
        cardDealingPhase(randomAgent, fixedAgent)
        print()
        biddingPhase(randomAgent, fixedAgent)
        print()
        showdownPhase(randomAgent, fixedAgent)

    print(f'{randomAgent.agentType} agent has won a total of ${randomAgent.moneyWon}.')
    print(f'{fixedAgent.agentType} agent has won a total of ${fixedAgent.moneyWon}.')
    print(f'{randomAgent.agentType} agent won {randomAgent.wins} times!')
    print(f'{fixedAgent.agentType} agent won {fixedAgent.wins} times!')
    randomVFixedWinner = randomAgent.agentType if randomAgent.moneyWon > fixedAgent.moneyWon else fixedAgent.agentType
    randomVFixedDiff = max(randomAgent.moneyWon, fixedAgent.moneyWon) - \
        min(randomAgent.moneyWon, fixedAgent.moneyWon)
    randomAgent.clear()
    fixedAgent.clear()

    print(f'Game between random and reflex agent:')
    for number in range(0, 50):
        print(f'Round {number}.')
        cardDealingPhase(randomAgent, reflexAgent)
        print()
        biddingPhase(randomAgent, reflexAgent)
        print()
        showdownPhase(randomAgent, reflexAgent)

    print(f'{randomAgent.agentType} agent has won a total of ${randomAgent.moneyWon}.')
    print(f'{reflexAgent.agentType} agent has won a total of ${reflexAgent.moneyWon}.')
    print(f'{randomAgent.agentType} agent won {randomAgent.wins} times!')
    print(f'{reflexAgent.agentType} agent won {reflexAgent.wins} times!')
    randomVReflexWinner = randomAgent.agentType if randomAgent.moneyWon > reflexAgent.moneyWon else reflexAgent.agentType
    randomVReflexDiff = max(randomAgent.moneyWon, reflexAgent.moneyWon) - \
        min(randomAgent.moneyWon, reflexAgent.moneyWon)
    randomAgent.clear()
    reflexAgent.clear()

    print(f'Game between fixed and reflex agent:')
    for number in range(0, 50):
        print(f'Round {number}.')
        cardDealingPhase(fixedAgent, reflexAgent)
        print()
        biddingPhase(fixedAgent, reflexAgent)
        print()
        showdownPhase(fixedAgent, reflexAgent)

    print(f'{fixedAgent.agentType} agent has won a total of ${fixedAgent.moneyWon}.')
    print(f'{reflexAgent.agentType} agent has won a total of ${reflexAgent.moneyWon}.')
    print(f'{fixedAgent.agentType} agent won {fixedAgent.wins} times!')
    print(f'{reflexAgent.agentType} agent won {reflexAgent.wins} times!')
    fixedVReflexWinner = fixedAgent.agentType if fixedAgent.moneyWon > reflexAgent.moneyWon else reflexAgent.agentType
    fixedVReflexDiff = max(fixedAgent.moneyWon, reflexAgent.moneyWon) - \
        min(fixedAgent.moneyWon, reflexAgent.moneyWon)
    fixedAgent.clear()
    reflexAgent.clear()

    print(f'{randomVFixedWinner} agent won the match between random and fixed agent with ${randomVFixedDiff} difference.')
    print(f'{randomVReflexWinner} agent won the match between random and reflex agent with ${randomVReflexDiff} difference.')
    print(f'{fixedVReflexWinner} agent won the match between fixed and reflex agent with ${fixedVReflexDiff} difference.')
