
import gym
from gym import spaces
import numpy as np
import time
import sys

import logs as logger

MAX_STEP = 500
MAX_REWARD = 1000
MAX_EPISODE = 10000
MAX_EPISODE_PER_UPDATE = 100

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
		
		if self.test_version == 1 or self.test_version == 2:
			cartpole_V1(self)
		elif self.test_version == 3:
			cartpole_3(self)


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
		logger.error(f'======== reward => {totalreward} ========')
	return totalreward

def param_formula_1():
	return np.random.rand(4) * 2 - 1
	
def param_formula_2(old_params, noise_scaling):
	return old_params + (np.random.rand(4) * 2 - 1)*noise_scaling


def cartpole_V1(cartpole):
	bestparams = None

	bestreward = 0

	noise_scaling = 0.1

	parameters = None

	max_episode_per_update = MAX_EPISODE_PER_UPDATE if cartpole.test_version == 1 else 1

	for ie_episode in range(MAX_EPISODE):
		if cartpole.test_version == 1:
			if ie_episode == 0:
				parameters = param_formula_1()
			newparams = param_formula_2(parameters, noise_scaling)
			param_to_use = newparams
		else :
			parameters = param_formula_1()
			param_to_use = parameters
		reward200 = 0
		reward = 0
		for _ in range(max_episode_per_update):
			run = run_episode(cartpole, param_to_use, True if reward200 > 50 and cartpole.visu else False)
			if run == 200:
				reward200 += 1
			reward += run

		logger.warning(f'======== episode => {ie_episode} ({ie_episode * max_episode_per_update}) (reward200 {reward200}) ========')

		if reward > bestreward:
			logger.error(f'======== bestreward => {reward} ========')
			bestreward = reward
			parameters = param_to_use
			if reward200 == max_episode_per_update:
				break


def cartpole_1(cartpole):
	
	noise_scaling = 0.1
	parameters = np.random.rand(4) * 2 - 1
	bestreward = 0

	for ie_episode in range(MAX_EPISODE):
		newparams = parameters + (np.random.rand(4) * 2 - 1)*noise_scaling

		reward200 = 0
		reward = 0
		for _ in range(MAX_EPISODE_PER_UPDATE):
			run = run_episode(cartpole, newparams, True if reward200 > 50 and cartpole.visu else False)
			if run == 200:
				reward200 += 1
			reward += run
		logger.warning(f'======== episode => {ie_episode} ({ie_episode * MAX_EPISODE_PER_UPDATE}) (reward200 {reward200}) ========')

		if reward > bestreward:
			logger.error(f'======== bestreward => {reward} ========')
			bestreward = reward
			parameters = newparams
			if reward200 == MAX_EPISODE_PER_UPDATE:
			# if reward == 200 * MAX_EPISODE_PER_UPDATE:
			# if reward == 200:
				break


def cartpole_2(cartpole):
	bestparams = None

	bestreward = 0


	for i_episode in range(MAX_EPISODE):
		parameters = np.random.rand(4) * 2 - 1
		reward = run_episode(cartpole, parameters)

		if reward > bestreward:
			bestreward = reward
			bestparams = parameters
			# considered solved if the agent lasts 200 timesteps
			if reward == MAX_REWARD:
				break

		if i_episode % 1000 == 0:
			logger.warning(
				f'======== {i_episode} (avg reward = {avg_reward}  {len(all_reward0)}-{len(all_reward50)}-{len(all_reward100)}) =========')
			logger.info(f'======== params => {parameters} ========')
			logger.info(f'======== reward => {reward} ========')

			# avg_reward = []
			all_reward100 = []
			all_reward50 = []
			all_reward0 = []
			time.sleep(2)
			pass
	
	logger.info(f'======== bestparams => {bestparams} ========')

def cartpole_3(cartpole):
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

		for i_step in range(100000):

			env.render()
			logger.warning(f'=================')

			action = env.action_space.sample()
			logger.info(f'action => {action}')


			observation, reward, done, info = env.step(action)
			logger.info(f'obs => {observation} {reward}')

			# time.sleep(0.5)

			if done:
				logger.info(f'========Episode {i_episode} finished after {i_step} steps========')
				time.sleep(1)
				break


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
