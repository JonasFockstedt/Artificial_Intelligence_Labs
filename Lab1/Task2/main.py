import agent
import random

totalPot = 0
deck = list()
randomAgent = agent.Agent('random')
fixedAgent = agent.Agent('fixed')
reflexAgent = agent.Agent('reflex')


def generateDeck():
    global deck
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['s', 'h', 'd', 'c']

    for cardSuit in suits:
        for cardRank in ranks:
            deck.append(cardRank+cardSuit)

    random.shuffle(deck)    # Shuffles deck.


# Deal hand to given agent.
def assignHand(agent):
    global deck
    for cardNumber in range(0, 3):      # Hand three cards to the agent.
        agent.hand.append(deck.pop())
    agent.hand.sort()   # Sort hand in rising order.


# Determine which agent has won the round.
def compareHands(firstAgent, secondAgent):
    global totalPot
    # If their hand has the same ranking.
    if firstAgent.calculateHand() and secondAgent.calculateHand() == 'High cards!' or 'Two of a kind!' or 'Three of a kind!':
        # Iterates through both agent's hands, saved in a tuple.
        handTuple = tuple(zip(firstAgent.hand, secondAgent.hand))
        for index in handTuple:
            # If the first agent has a card with higher value, the first agent wins.
            if index[0] > index[1]:
                assignWin(firstAgent)
                break
            # If the second agent has a card with higher value, the second agent wins.
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
    # Tree bidding phases.
    for x in range(1, 4):
        print(f'Bidding phase {x}:')
        totalPot += firstAgent.bet()
        totalPot += secondAgent.bet()
        print()


def showdownPhase(firstAgent, secondAgent):
    firstAgent.revealHand()
    secondAgent.revealHand()
    compareHands(firstAgent, secondAgent)

# Clear hand of two agents.


def resetHands(firstAgent, secondAgent):
    firstAgent.hand.clear()
    secondAgent.hand.clear()


    # Main.
if __name__ == '__main__':
    # Start first game, random versus fixed agent.
    print(f'Game between random and fixed agent:')
    for number in range(0, 50):
        print(f'Round {number}.')
        cardDealingPhase(randomAgent, fixedAgent)
        print()
        biddingPhase(randomAgent, fixedAgent)
        print()
        showdownPhase(randomAgent, fixedAgent)

    # Print out result of the game.
    print(f'{randomAgent.agentType} agent has won a total of ${randomAgent.moneyWon}.')
    print(f'{fixedAgent.agentType} agent has won a total of ${fixedAgent.moneyWon}.')
    print(f'{randomAgent.agentType} agent won {randomAgent.wins} times!')
    print(f'{fixedAgent.agentType} agent won {fixedAgent.wins} times!')
    # Calculate the agent who won the most money, and by how much.
    randomVFixedWinner = randomAgent.agentType if randomAgent.moneyWon > fixedAgent.moneyWon else fixedAgent.agentType
    randomVFixedDiff = max(randomAgent.moneyWon, fixedAgent.moneyWon) - \
        min(randomAgent.moneyWon, fixedAgent.moneyWon)
    # Clear agent properties before next game.
    randomAgent.clear()
    fixedAgent.clear()

    # Start second game, random versus reflex agent.
    print(f'Game between random and reflex agent:')
    for number in range(0, 50):     # Plays 50 rounds.
        print(f'Round {number}.')
        cardDealingPhase(randomAgent, reflexAgent)
        print()
        biddingPhase(randomAgent, reflexAgent)
        print()
        showdownPhase(randomAgent, reflexAgent)

    # Print out result of the game.
    print(f'{randomAgent.agentType} agent has won a total of ${randomAgent.moneyWon}.')
    print(f'{reflexAgent.agentType} agent has won a total of ${reflexAgent.moneyWon}.')
    print(f'{randomAgent.agentType} agent won {randomAgent.wins} times!')
    print(f'{reflexAgent.agentType} agent won {reflexAgent.wins} times!')
    # Calculate the agent who won the most money, and by how much.
    randomVReflexWinner = randomAgent.agentType if randomAgent.moneyWon > reflexAgent.moneyWon else reflexAgent.agentType
    randomVReflexDiff = max(randomAgent.moneyWon, reflexAgent.moneyWon) - \
        min(randomAgent.moneyWon, reflexAgent.moneyWon)
    # Clear agent properties before next game.
    randomAgent.clear()
    reflexAgent.clear()

    # Start third game, fixed versus reflex agent.
    print(f'Game between fixed and reflex agent:')
    for number in range(0, 50):     # Plays 50 rounds.
        print(f'Round {number}.')
        cardDealingPhase(fixedAgent, reflexAgent)
        print()
        biddingPhase(fixedAgent, reflexAgent)
        print()
        showdownPhase(fixedAgent, reflexAgent)

    # Print out result of the game.
    print(f'{fixedAgent.agentType} agent has won a total of ${fixedAgent.moneyWon}.')
    print(f'{reflexAgent.agentType} agent has won a total of ${reflexAgent.moneyWon}.')
    print(f'{fixedAgent.agentType} agent won {fixedAgent.wins} times!')
    print(f'{reflexAgent.agentType} agent won {reflexAgent.wins} times!')
    # Calculate the agent who won the most money, and by how much.
    fixedVReflexWinner = fixedAgent.agentType if fixedAgent.moneyWon > reflexAgent.moneyWon else reflexAgent.agentType
    fixedVReflexDiff = max(fixedAgent.moneyWon, reflexAgent.moneyWon) - \
        min(fixedAgent.moneyWon, reflexAgent.moneyWon)
    # Clear agent properties before next game.
    fixedAgent.clear()
    reflexAgent.clear()

    # Print out summarization of the three matches.
    print('\nSUMMARIZATION:')
    print(f'{randomVFixedWinner} agent won the match between random and fixed agent with ${randomVFixedDiff} difference.')
    print(f'{randomVReflexWinner} agent won the match between random and reflex agent with ${randomVReflexDiff} difference.')
    print(f'{fixedVReflexWinner} agent won the match between fixed and reflex agent with ${fixedVReflexDiff} difference.')
