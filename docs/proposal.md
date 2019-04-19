---
layout:	default
title:	Proposal
---

_Summary:_
	The focus of our project is to create a "PvP" combat AI which which will allow the agent to fight other agents (controlled either by AI or a player). Agents will fight 1 on 1 in an arena of fixed size. The weapon and armor setup we will use is to be determined, but we are planning to incorporate the shield mechanics introduced in the combat update. The agent will get the position of its opponent from the worldstate observation, and calculate the opponent's position relative to itself. This will be the primary input to a desicion making algorithm, most likely a neural network, which will output the actions for the agent to take (such as turning, moving, attacking, or blocking)

_AI/ML Algorithms:_
	We plan to use a genetic algorithm to train a population of AIs. In each generation, AIs will be paired off to fight 1v1, and selection will be based on damage done to the opponent.


_Evaluation Plan:_
	We will also make a basic hard-coded combat AI, to use as a baseline. That way, we can measure progression of our AIs based on their performance, in terms of win rate, against this static AI. The goal will be be to exceed the performance of the hard-coded AI.
  
_Instructor Appointment:_
	Our meeting with the instructor is planned for 4:30pm May 8th
