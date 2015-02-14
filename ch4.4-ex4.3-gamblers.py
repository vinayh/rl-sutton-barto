import matplotlib.pyplot as plt

########################
# Constant declarations
########################
p = 0.4 # Probability of the coin coming up heads
num_states = 100 # From 0 to 100, inclusive
theta = 1e-30 # Small positive number, threshold to stop value iteration
gamma = 1 # Discount factor

rewards = [0] * (num_states + 1) # Creating array with num_states elements
rewards[num_states] = 1 # Setting reward of $100 state to 1
values = [0] * (num_states + 1) # Creating values array by default equal to rewards
policy = [0] * (num_states + 1) # Creating array to hold wager for each state


########################
# Function declarations
########################

def main():
	#print "State\tValue\t\t\tPolicy"
	iterations = 0
	delta = 9999 # Large number

	while (delta >= theta): # If delta is below threshold, end and print result
		iterations += 1
		delta = 0 # Delta value to store max change in value
		for capital in range(1, num_states): # For every state (capital)
			old_v = values[capital] # Save old value
			bellman(capital) # Run Bellman on capital, save to value
			delta = max(delta, abs(old_v - values[capital])) # Set delta to max change in value

	for state in range(1, num_states + 1):
		print values[state]
	print iterations
	plt.plot(values)
	plt.suptitle('Gambler problem (value iteration) - Ex. 4.3 in Ch. 4.4 - p = 0.4, 32 it')
	plt.xlabel('State (Capital)')
	plt.ylabel('Value')
	plt.show()
def bellman(capital):
	max_value = 0

	for wager in range(1, min(capital, 100 - capital) + 1): # Every possible wager
		win_state = capital + wager # Possible states are (index +/- capital)
		lose_state = capital - wager

		# print "Capital is ", capital, "\n"
		# print "Win state is ", win_state, " with value ", values[win_state]
		# print "Lose state is ", lose_state, " with value ", values[lose_state], "\n\n",

		sigma = p * (rewards[win_state] + gamma * values[win_state]) # Prob of winning
		sigma += (1 - p) * (rewards[lose_state] + gamma * values[lose_state]) # Losing
		# sigma /= 2
		
		if sigma > max_value: 
			values[capital] = sigma # Sigma value to store max expected value
			policy[capital] = wager

		#if capital is 50:
		#	print wager,
		#	print values[capital], policy[capital]
########################
# Code to run
########################

main()