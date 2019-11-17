import gym
import time
#env = gym.make("SpaceInvaders-ram-v0")
env = gym.make('Marvin-v0')

for i_episode in range(200):
	observation = env.reset()
	for t in range(100):
		env.render()
		print(f'========{i_episode} - {t}=========')
		print(f'observation A - {observation}')
		action = env.action_space.sample()
		observation, reward, done, info = env.step(action)


		print(f'action {action}')
		print(f'reward {reward}')
		print(f'done {done}')
		print(f'info {info}')
		print(f'observation B - {observation}')
		# time.sleep(0.5)

		if done:
			print(f"========Episode {i_episode} finished after {t + 1} timesteps========")
			time.sleep(1)
			break

env.close()
