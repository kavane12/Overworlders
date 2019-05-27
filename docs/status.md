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

Since there are many variables that can influence the outcome of PvP (player vs player)
combat, we used a Deep Q-learning approach to create our AI.


**Evaluation**


**Remaining Goals & Challenges**


**Resources Used**

https://github.com/microsoft/malmo/tree/master/Malmo/samples/Python_examples/multi_agent_test.py