import gym
from Network import Network

env = gym.make("CartPole-v1")
net = Network(env.observation_space.shape[0], 2, 0.001, .6, .9, .05, .995, 100)
for ep in range(100):
    state = env.reset()
    t = 0
    while True:
        env.render()
        action = net.getAction(state)
        nextState, reward, done, _ = env.step(action)
        net.log(state, action, nextState, reward, done)
        state = nextState
        net.train()
        t += 1
        if done:
            print("Episode finished after {} timesteps".format(t + 1))
            break
    net.update()
env.close()
