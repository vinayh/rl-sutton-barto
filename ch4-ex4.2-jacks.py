########################
# Constant declarations
########################

gamma = 0.9
max_transfer = 5
max_cars = 20
theta = 0.01
num_states = (max_cars + 1) ** 2

# Expected values for Poisson random variables
lambda_a_rental = 3
lambda_b_rental = 4
lambda_a_return = 3
lambda_b_return = 2

value = [0] * num_states
policy = [0] * num_states
cars = [0] * num_states

########################
# Function declarations
########################

def policy_evaluation(): # Iterate the Bellman equation, done in place
	delta = 1
	while delta >= theta: # Repeat until delta is less than theta
		delta = 0
		for s in range(num_states): # Iterates through every state
			v = value[s] # Preserves old value of state
			value[s] = bellman(s)
			delta = max(delta, abs(v-value[s])) # Sets delta to the largest update

def policy_improvement():
	for s in range(num_states + 1):
		b = policy[s];
		policy[s] = 2
		if b != policy[s]:
			return False # policy_stable set to false
		else:
			return True # policy_stable set to true

def bellman(s):
	a = s // 21
	b = s % 21
	num_transfer = get_policy(a, b)
	num_transfer = max(-b, min(num_transfer, a)) # Ensure num to transfer exists in source
	num_transfer = max(-max_transfer, min(num_transfer, max_transfer)) # Ensure transfer does not exceed max
	
	new_a = a - num_transfer
	new_b = b + num_transfer
	temp = 0
	
	for n in range(num_states):
		prob_a = prob[(new_a * max_cars + (n // max_cars))] # Set probabilities of getting to new state
		prob_b = prob[(new_b * max_cars + (n % max_cars))]
		rew_a = reward_a[new_a] # Set rewards of getting to new state
		rew_b = reward_b[new_b]
		temp += prob_a * prob_b * (rew_a + rew_b + gamma * get_value(a, b)) # Sum the component of Bellman

def poisson(expected, n):
	return (expected**n)*(e**(-expected))/(factorial(n)) # Evaluates Poisson random variable

def get_value(a, b):
	return value[a*max_cars + b]

def get_policy(a, b):
	return policy[a*max_cars + b]

########################

policy_stable = False
while not policy_stable:
	policy_evaluation()
	policy_stable = policy_improvement()
