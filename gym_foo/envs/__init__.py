  from gym_foo.envs.foo_env import FooEnv
  from gym_foo.envs.foo_extrahard_env import FooExtraHardEnv

  register(
		id='MyEnv-v0',
		entry_point='gym.envs.my_collection:MyEnv',
)