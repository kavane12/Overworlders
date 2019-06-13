---
layout: default
title:  Final Report
---

## Video

<p align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/d3RGnFj9Nww" frameborder="0" allowfullscreen></iframe>
</p>

## Project Summary

Our project aims to create an AI that is capable of advanced combat in Minecraft. Our AI was created with Minecraft's 1.9 Combat in mind, meaning it makes use of several newly introduced combat mechanics, which are:

- Attacks need to be recharged inbetween swings to maximize damage; spammed attacks do next to no damage
- Shields were introduced that can block all frontal damage when held up; however while held up the player is slowed and unable to attack

We considered using axes for our AI since they can disable shields for a period of time, but opted not to as it has a lower dps than the sword and the chance of disabling a shield using it is prohibitedly low.

Our AI learns through a Deep Q learning algorithm and fights a copy of itself in a 20 by 20 block large arena. Both AIs come equipped in full iron armor (one agent uses a golden helmet for distinguishing the two AIs, but stat-wise is identical to an iron one). They wield stone swords, a basic bow, and a shield in the offhand.

<p align="center">
<img src="https://raw.githubusercontent.com/kavane12/Overworlders/master/docs/pics/final_equipment.png">
</p>

## Approach
The approach we chose for this project is deep Q learning. Some other options which were considered included genetic algorithm and Q-table, while a simple hard-coded AI serves as a baseline. The genetic algorithm, which was our initial proposal, was deemed to be unfeasible, due to the excessive amount of training time which would be required - each member of the population would need to fight in at least 1 1v1 battle every generation, meaning at least dozens of battles every generation, and then hundreds, or even thousands of generations would likely be needed to see significant results. A Q-table based reinforcement learning algorithm would be another possible method, with advantages and disadvantages compared to our deep Q approach. Deep Q learning inherently works with our continuous state space, while with a Q table, we would be forced to make a tradeoff between the granularity of the state space and the size of our Q table. However, it is possible that, even with the large table size, a Q table may take fewer iterations to show results, making it quicker to train overall.

Our deep Q learning implementation remains unchanged from that in our status report, with the exception of network size, which is set up to automatically scale with the sizes of the input (state space) and output (action space). The network has 4 hidden layers; the first is 3 times the size of the input, the second is 2\*input + 1\*output, the third is 1\*input + 2\*output, and the last is 3\*output. As is typical in deep Q learning, the network is meant to approximate the quality of all available actions in a given state. It is trained on selections of \[state, actions, nextState, reward] sets, sampled from a replay memory. Gradient descent is performed by trying to minimize the difference between Q(s, a), the network's predicted quality for action a in state s, and q*, the estimated actual value for that action. q* is found by adding the reward, r, to the maximum action quality in nextState s', times gamma, the discount factor. This is found by putting s' into the target net Q', a stored version of the training net, and taking the quality value of the max quality action returned, a'. Using a standard squared error function, this means loss can be represented by the following equation:

    l = (Q(s,a) - (r + gamma * Q'(s', a')))
  
The above is unchanged since the status report; however, what has changed are the state and action spaces, and reward system, as we have added support for features such as pitching, jumping, and using a bow, as well as given the agent more information about what its opponent is doing. The state space now has 26 variables, up siginicantly from 6 previously. These include variables to indicate what the agent is currently doing (moving, strafing, blocking, turning, pitching, blocking, or drawing the bow), how long since it has attacked, how long it has been drawing the bow (if it is doing so), its life, y position, and pitch, and distance to the opponent in forward/backward and left/right components. It also has all the same information about the opponent as it has about itself.

The actions space consists of 28 actions: 3 move actions (forward, stop, or backward), 3 strafe actions (left, none, or right), 9 turn actions (turn at 100%, 60%, 25%, or 10% speed in each directions, or stop turning), 7 pitch actions (40%, 15%, 5%, and 0% speed, again supporting both directions), jump, attack, start or stop blocking, and start or stop drawing the bow. The attack, block, and draw actions were partially abstracted, so that the AI would not have to deal with switching hotbar slots directly, but could instead just select what action it wanted to performed, and the necessary hotbar actions would be handled automatically.

Rewards are the trickiest part about setting up a deep Q learning environment, and took significant trial and error to get right, with there still being room for improvement. Ideally, we wanted to keep the reward system as simple as possible in order to allow the agent to learn the best strategy organically without being too prescriptive. Therefore, initially we tried only giving the agent a reward for doing damage, and a penalty for taking damage. However, this did not work, for several reasons. One is that it is too hard for the agent to get to the state where it can do damage purely through random actions, because doing so requires so many things to go right: the agent must be looking in the right direction, at the right distance (for melee) or with the right pitch (for ranged), and select the correct combat actions (attack for melee, or draw followed by release for ranged). Additionally, the reward for doing damage would not be recieved until several cycles after the action which resulted in the damage was issued (especially for ranged combat, as the projectile takes time to travel), making it much more difficult for the learning algorithm to correctly associate the reward with the action. Therefore, we had to implement a complex reward structure, in order to guide the AI towards the desired actions, and reward it more immediately. The final reward function, and the calculations of each component, are shown below.

<p align="center">
<img src="https://raw.githubusercontent.com/kavane12/Overworlders/master/docs/pics/rewards.PNG">
</p>

Angle and distance are relative to the opponent to the opponent (e.g. angle 0 means facing the opponent, distance 2 means 2 blocks from the opponent). attackCharge and shotCharge are variables indicating how fully charged (between 0 and 1) the attack or bow shot was.

## Evaluation
Write eval here

## References & Resources
Libraries:
- Tensorflow/Keras
- Malmo

Documentation:
- [Project Malmo](http://microsoft.github.io/malmo/0.30.0/Documentation/index.html)
- [Malmo Mission Schema](http://microsoft.github.io/malmo/0.30.0/Schemas/Mission.html)
- [Keras](https://keras.io/)

Other resources:
- [Malmo's Multi Agent Python Example](https://github.com/microsoft/malmo/tree/master/Malmo/samples/Python_examples/multi_agent_test.py)
- [Intro to Deep Q Learning](https://keon.io/deep-q-learning/)

