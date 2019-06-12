---
layout: default
title:  Final Report
---

## Video

<p align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/d3RGnFj9Nww" frameborder="0" allowfullscreen></iframe>
</p>

## Project Summary

Our project aims to create an AI that is capable of advanced combat in Minecraft. Our AI was created with Minecraft's 1.9 Combat in mind, meaning it makes use of new introduced mechanics, which are:

- Attacks need to be recharged inbetween swings to maximize damage; spammed attacks do no damage
- Shields were introduced that can block all frontal damage when held up; however while held up the player cannot attack and move at a much slower speed

We considered using axes for our AI since they can disable shields for a period of time, but opted not to as it has a lower dps than the sword and the chance of disabling a shield is prohibitedly low.

Our AI learns through a Deep Q learning algorithm and fights a copy of itself in a 20 by 20 block large arena. Both AIs come equipped in full iron armor (one agent uses a golden helmet for distinguishing the two AIs, but stat-wise is identical to an iron one). They wield stone swords, a basic bow, and a shield in the offhand.

<p align="center">
![alt text](https://raw.githubusercontent.com/kavane12/Overworlders/master/docs/pics/final_equipment.png)
</p>

## Approach
Write approach here

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

