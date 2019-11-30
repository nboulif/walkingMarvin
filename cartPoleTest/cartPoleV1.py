
import gym
from gym import spaces
import numpy as np
import time
import sys

import logs as logger

MAX_STEP = 500
MAX_EPISODE_BASIC = 20000
MAX_EPISODE_UPDATE = 200
MAX_EPISODE_BEFORE_UPDATE = 100
POURCENTAGE_SUCCESS_MINIMUM = 100

class CartPole(object):

	def __init__(self):
		self.visu = False
		self.version = 'v0'
		self.test_version = 1
		
	def init_env(self):
		self.env = gym.make(f'CartPole-{self.version}')
		
		return None
	
	def close_env(self):
		self.env.close()
		return None

	def reset_env(self):
		return self.env.reset()

	def set_version(self, value):
		self.version = value
		return None

	def set_visu(self, value):
		self.visu = value
		return None

	def set_test_version(self, value):
		self.test_version = value
		return None

	def run(self):
		
		if self.test_version == 1:		
			cartpole_update(self)
		elif self.test_version == 2:
			cartpole_basic(self)
		elif self.test_version == 3:
			cartpole_sample(self)


def ft_avg(lst):
	return sum(lst) / len(lst)


def run_episode(cartpole, parameters, visu = False):
	observation = cartpole.reset_env()
	totalreward = 0
	for _ in range(MAX_STEP):
		if visu:
			cartpole.env.render()

		action = 0 if np.matmul(parameters, observation) < 0 else 1
		observation, reward, done, info = cartpole.env.step(action)
		totalreward += reward
		# if done and not visu:
		if done:
			break

	if visu:
		logger.debug(f'======== reward => {totalreward} ========')
	return totalreward

def param_formula_1():
	return np.random.rand(4) * 2 - 1
	
def param_formula_2(old_params, noise_scaling):
	return old_params + ( param_formula_1() * noise_scaling)


# def cartpole_V1(cartpole):
# 	bestparams = None

# 	bestreward = 0

# 	noise_scaling = 0.1

# 	parameters = None

# 	max_episode_BEFORE_update = MAX_EPISODE_BEFORE_UPDATE if cartpole.test_version == 1 else 1

# 	for ie_episode in range(10000):
# 		if cartpole.test_version == 1:
# 			if ie_episode == 0:
# 				parameters = param_formula_1()
# 			newparams = param_formula_2(parameters, noise_scaling)
# 			param_to_use = newparams
# 		else:
# 			parameters = param_formula_1()
# 			param_to_use = parameters
# 		reward200 = 0
# 		reward = 0
# 		for _ in range(MAX_EPISODE_BEFORE_UPDATE):
# 			run = run_episode(cartpole, param_to_use, True if reward200 > 50 and cartpole.visu else False)
# 			if run == 200:
# 				reward200 += 1
# 			reward += run

# 		logger.warning(f'======== episode => {ie_episode} ({ie_episode * MAX_EPISODE_BEFORE_UPDATE}) (reward200 {reward200}) ========')

# 		if reward > bestreward:
# 			logger.error(f'======== bestreward => {reward} ========')
# 			bestreward = reward
# 			parameters = param_to_use
# 			if (reward200/max_episode_BEFORE_update) * 100 == POURCENTAGE_SUCCESS_MINIMUM:
# 				break

def cartpole_basic(cartpole):
	bestparams = None

	bestreward = 0

	reward200 = 0
	
	for ie_episode in range(MAX_EPISODE_BASIC):
		parameters = param_formula_1()

		reward = run_episode(cartpole, parameters, True if reward200 > (MAX_EPISODE_BASIC / 10) - 10 and cartpole.visu else False)
		logger.warning(f'======== episode => {ie_episode} (reward200 {reward200}) ========')
		
		if reward == 200:
			reward200 += 1
			if reward200 == (MAX_EPISODE_BASIC / 10) - 10:
				break

		if reward > bestreward:
			bestreward = reward
			bestparams = parameters


	logger.info(f'======== bestparams => {bestparams} ========')

def cartpole_update(cartpole):
	bestparams = None

	noise_scaling = 0.1
	parameters = param_formula_1()
	bestreward = 0


	for ie_episode in range(MAX_EPISODE_UPDATE):
		newparams = param_formula_2(parameters, noise_scaling)

		reward200 = 0
		reward = 0
		for _ in range(MAX_EPISODE_BEFORE_UPDATE):
			run = run_episode(cartpole, newparams, True if reward200 > 190 and cartpole.visu else False)
			if run == 200:
				reward200 += 1
			reward += run
		logger.warning(f'======== episode => {ie_episode} ({ie_episode} * {MAX_EPISODE_BEFORE_UPDATE}) (reward200 {reward200}) ========')

		if reward > bestreward:
			logger.error(f'======== bestreward => {reward} ========')
			bestreward = reward
			parameters = newparams
			bestparams = parameters
			if (reward200/MAX_EPISODE_BEFORE_UPDATE) * 100 == POURCENTAGE_SUCCESS_MINIMUM:
				break
		
		if ie_episode < MAX_EPISODE_UPDATE / 10 and reward200 == 0:
			return(cartpole_update(cartpole))

	logger.info(f'======== bestparams => {bestparams} ========')

def cartpole_sample(cartpole):
	env = cartpole.env
	
	logger.warning(f'======== ENV INFO =========')

	space = spaces.Discrete(8) # Set with 8 elements {0, 1, 2, ..., 7}
	x = space.sample()
	assert space.contains(x)
	assert space.n == 8

	logger.debug(f' action_space => {env.action_space}')
	logger.debug(f' obs_space => {env.observation_space}')
	logger.debug(f' obs_space.high => {env.observation_space.high}')
	logger.debug(f' obs_space.low => {env.observation_space.low}')

	input('Press any key')

	for i_episode in range(10):
		observation = env.reset()

		logger.warning(f'========{i_episode}=========')

		logger.info(f'obs => {observation}')

		run_episode(cartpole, np.array([-0.17501466, 0.2028902 , 0.35170482, 0.45307758]), True)

		# for i_step in range(100000):

		# 	env.render()
		# 	logger.warning(f'=================')

		# 	action = env.action_space.sample()
		# 	logger.info(f'action => {action}')

		# 	observation, reward, done, info = env.step(action)
		# 	logger.info(f'obs => {observation} {reward}')

		# 	# time.sleep(0.5)

		# 	if done:
		# 		logger.info(f'========Episode {i_episode} finished after {i_step} steps========')
		# 		time.sleep(1)
		# 		break

def parse_argv(cartpole):
	argc = len(sys.argv)
	i = 1
	while i < argc:
		if sys.argv[i][0] == '-':
			if len(sys.argv[i]) == 1:
				exit(print('errror 12'))

			if sys.argv[i] == '-t':
				if i + 1 == argc:
					exit(print('errror 25'))
				i += 1
				if sys.argv[i] == 'sample':
					cartpole.set_test_version(3)
				elif sys.argv[i] == 'update':
					cartpole.set_test_version(1)
				elif sys.argv[i] == 'basic':
					cartpole.set_test_version(2)
				else :
					cartpole.set_test_version(int(sys.argv[i]))
			elif sys.argv[i] == '-v':
				cartpole.set_visu(True)
		else:
			pass

		i += 1


if __name__ == "__main__":
	
	cartpole = CartPole()

	cartpole.init_env()

	if len(sys.argv) > 1:
		parse_argv(cartpole)

	cartpole.run()

	cartpole.close_env()
