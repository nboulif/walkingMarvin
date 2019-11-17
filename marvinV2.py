import gym
import time
#env = gym.make("SpaceInvaders-ram-v0")
env = gym.make('Marvin-v0')

for i_episode in range(200):
	observation = env.reset()
	while True:
		env.render()
		# print(f'========{i_episode}=========')
		# print(f'observation A - {observation}')
		action = env.action_space.sample()
		# action = [1, 1, 1, 1]
		# action = [0, -1, 0, -1]
		# action = [-1, -1, -1, -1]
		# action = [0, 0, 0, 0]

		observation, reward, done, info = env.step(action)


		# print(f'action {action}')
		print(f'reward {reward}')
		# print(f'done {done}')
		# print(f'info {info}')

		# print(f'observation B - {observation[-11:-1]}')

		

		print(f'body.angle => {observation[0]}')
		print(f'body.position => {env.body.position}')
		print(f'lidar => {[i for i in observation[14:24]]}, ')
			
		# print(f'observation B - {observation}')

		time.sleep(0.2)
		# time.sleep(0.5)

		if done:
			print(f"========Episode {i_episode} finished after timesteps========")
			time.sleep(2)
			observation = env.reset()
			# break

env.close()
