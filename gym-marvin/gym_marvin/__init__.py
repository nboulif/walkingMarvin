from gym_marvin.envs.registration import register

# 42
register(
   	id='Marvin-v0',
   	entry_point='gym_marvin.envs.forty_two:Marvin',
)
