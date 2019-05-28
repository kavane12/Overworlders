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

We used a fairly standard deep Q learning approach, based on the one found in the last resource link below. It uses a neural network constructed with Keras to predict q values of actions given a state. Training is done on a replay memory, which contains sets of state, action, resulting state, and reward. The loss function for training the network is 

    (Q(s, a) - q*)^2

Q(s, a) is the network's current prediction for the value of action a in state s. q*, the target value of that action, is computed: 

    q* = r + gamma * Q'(s', a')

Where r is the reward recieved, s' is the observed resulting state, gamma is the discount factor, Q' is a saved past version of the predition network (updated periodically), and a' is the optimal action in s' as predicted by Q'.

![alt text](https://raw.githubusercontent.com/kavane12/Overworlders/master/docs/pics/deep-q-learning.png)

For the purpose of this status report, we used a fairly minimal state space, containing 6 variables: foward/backward distance to the opponent (relative to the agent), left/right distance to the opponent (again relative to the agent), time since last attack,
the agent's current forward/backward movement direction, its current left/right movement direction, and it's current turning speed. The action space is a bit larger, because we wanted to allow the agent to turn at different speeds. Ideally the action space would be continuous, allowing the agent to select any turn speed between -1 and 1. However, since actions correspond to indices of the outputs of the neural network, they must be discrete. Therefore, we allowed the agent 7 options for turn commands: 0.7, 0.4, 0.2, 0, 0.2, 0.4, and 0.7. In addition to these, the agent can start moving forward (move 1), stop moving (move 0), and start moving backwards (move -1), and the same for strafing. Finally, it can issue a command to make a single attack.

The main reward structure used consists of rewarding the agent when it does damage (proportional to the damage done), and penalizing it when it takes damage (again proprotionally). Because we want to train the agent primarily to fight, rather than to run away, we made the reward 10 times larger than the penalty. In addition to these main rewards, we added additional smaller rewards to guide the agent during its initial training. These included a reward for being in range of the enemy, and another for looking in its general direction. When both these conditions are met, it gets an additional reward, plus another if it makes a sufficiently charged attack. If the agent, however, at any point makes an attack that is not sufficiently charged, it incurs a small penalty. This is because with the current Minecraft combat system, attacks will do very little to no damage if attack commands are issued too fast; instead the weapon needs to be charged up for some duration between attacks.

**Evaluation**
In addition to the learning agent, we also made a hard coded 'basic AI' for it to fight against, for evaluation and training purposes. To start off our agent's training, we pitted it against an inactive enemy agent, or 'passive AI', which only turns to look at its opponent, but does not move on its own or attack. After about 100 training steps, the learning agent became competent at killing the passive AI. Its performance is shown below, measured in terms of damage done, and average reward recieved. 

![Training data vs. passive AI](https://raw.githubusercontent.com/kavane12/Overworlders/master/docs/pics/passiveTraining.png)

At this point, we switched over to training against the basic AI. For this training session, the basic AI's attack rate was limited to 1 per second. After about 50 episodes, our AI had learned to fight against an opponent which can fight back (performance again shown below).

![Training data vs. basic AI 1](https://raw.githubusercontent.com/kavane12/Overworlders/master/docs/pics/basicTraining1.png)

By now, we had already reached out goals for the status report, but as an additional test, we tried increasing the basic AI's attack speed to 1.5 attacks/second. This proved more difficult for our AI to handle, and there was less noticeably improvement.

![Training data vs. basic AI 2]

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
