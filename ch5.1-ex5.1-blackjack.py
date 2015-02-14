# Player cards are output to 10s, with dealer showing card to 1s and ace at 101-200
import random

################################################
# Constant declarations and classes
################################################

num_states = 200 # Combinations of 10 sums, 10 dealer cards, and whether ace is usable
hands_to_play = 200000
returns = [0] * (num_states + 1) # Creating array with num_states elements
visits = [0] * (num_states + 1)
stateValues = [0] * (num_states + 1)

class Hand:
	cards = 0
	value = 0
	ace = False
	usableAce = False

	def __init__(self, deck):
		self.cards = deck.twoCards()

	def draw(self, deck):
		self.cards.append(deck.oneCard())

	# Value of hand
	def value(self):
		sum = 0
		for card in self.cards:
			value = getVal(card)
			if value is 1: # In case of ace
				self.ace = True
			sum += value
		if sum <= 11:
			sum += value # For ace
			self.usableAce = True
		return sum

	def stateToPlay(self, showing):
		index = calcIndex(self, showing)
		return (index, self.value(), showing, self.usableAce())

	def showing(self):
		return self.cards[0]

	def toDraw(self):
		if self.value() is 20 or 21:
			return False
		else:
			return True

class Deck:
	cards = range(1, 53)

	def __init__(self):
		self.create()

	def create(self):
		self.cards = range(1, 53)
		random.shuffle(self.cards)

	def oneCard(self):
		toReturn = self.cards[0]
		if len(self.cards) <= 1:
			self.create()
		else:
			self.cards = self.cards[1:]
		return toReturn

	def twoCards(self):
		toReturn = self.cards[0:2]
		if len(self.cards) <= 2:
			self.create()
		else:
			self.cards = self.cards[2:]
		return toReturn

################################################
# Functions
################################################
def calcReward(playerValue, dealerValue):
	# If one or both players went bust or tied
	if playerValue > 21:
		return -1
	if dealerValue > 21:
		return 1
	if playerValue == dealerValue:
		return 0

	# If neither player went bust
	if (playerValue > dealerValue):
		return 1
	else:
		return -1

def calcIndex(player, showing):
	ace = 0
	value = player.value()
	if player.usableAce:
		ace = 100

	showing = min((showing % 13) + 1, 10)

	#print 'Player value is ', player.value()
	return 10 * (value - 12) + (showing - 1) + ace;

def getVal(card):
	value = (card % 13) + 1 # Get number on card
	value = min(value, 10) # Face cards = 10
	return value

def main():
	for _ in range(hands_to_play):
		statesSeen = [0]

		# Makes a deck, player hand, and dealer hand
		deck = Deck()
		player = Hand(deck)
		dealer = Hand(deck)
		
		# Copies dealer's top card to 'showing', adds to seen states
		showing = dealer.showing()
		
		if player.value() >= 12 and player.value() <= 21:
			statesSeen[0] = calcIndex(player, showing) # Add int to statesSeen
		#statesSeen[0] = player.stateToPlay(showing)

		# Hit from deck, add appropriate state to seen states
		while player.toDraw():
			player.draw(deck)
			statesSeen.append(calcIndex(player, showing))

		# Dealer draws if value is < 17
		while dealer.value() < 17:
			dealer.draw(deck)
		# Reward from game is calculated from player values
		reward = calcReward(player.value(), dealer.value())

		# For each state that was seen, increment visits and add reward to returns
		for state in statesSeen:
			#if (player.value() >= 12) and (player.value() <= 21):
				returns[state] += reward
				visits[state] = visits[state] + 1

	for index, visit in enumerate(visits):
		#stateValues[index] = float(reward) / visits[index]
		if visit is 0:
			print 0
			continue

		print float(returns[index]) / visit

################################################
# Runtime code
################################################

main()