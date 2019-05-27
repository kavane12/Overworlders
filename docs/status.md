---
layout:	default
title:	Status
---

**Project Summary**

The goal of this project is to create an AI capable of combat with other players. 
Furthermore, we wanted our AI to be proficient at the new mechanics introduced with
Minecraft's 1.9 Combat Update, where melee combat was overhauled in three key ways:

- Attacks need to be recharged between swings to do meaningful damage
- Shields were added that can block all damage in front of the player when activated
- Axes now do higher damage with a longer recharge timer than the sword,
and can disable shields for a period of time

Our implementation of the AI intends to make use of all features introduced above as well
as unchanged mechanics to defeat other players of equal level of equipment.


**Approach**

We initially considered using a genetic algorithm to train our AI. However, we decided
would not be feasible, due to the amount of time it would take to train. Instead, we opted
to use a reinforcement learning approach. Deep Q learning was ideal for our combat AI
due to the continuous nature of the state space.

The Deep Q learning implementation is a fairly standard approach, based on the one found in the last resource link below. It uses a neural network constructed with Keras to predict q values of actions given a state. Training is done on a replay memory, which contains sets of state, action, resulting state, and reward. The loss function for training the network is 

    (Q(s, a) - q*)^2

Q(s, a) is the network's current prediction for the value of action a in state s. q*, the target value of that action, is computed: 

    q* = r + gamma * Q'(s', a')

Where r is the reward recieved, s' is the observed resulting state, gamma is the discount factor, Q' is a saved past version of the predition network (updated periodically), and a' is the optimal action in s' as predicted by Q'.

![alt text](https://raw.githubusercontent.com/kavane12/Overworlders/master/docs/pics/deep-q-learning.png)

The state space contains several variables: 


**Evaluation**


**Remaining Goals & Challenges**


**Resources Used**
Libraries:
Tensorflow/Keras
Malmo

http://microsoft.github.io/malmo/0.30.0/Documentation/index.html
http://microsoft.github.io/malmo/0.30.0/Schemas/Mission.html
https://keras.io/

https://github.com/microsoft/malmo/tree/master/Malmo/samples/Python_examples/multi_agent_test.py
https://keon.io/deep-q-learning/
