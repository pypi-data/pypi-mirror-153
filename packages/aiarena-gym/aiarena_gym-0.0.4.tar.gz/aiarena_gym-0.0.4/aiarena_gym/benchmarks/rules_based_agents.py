#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 15:15:15 2022

@author: brandinho, unholycucumber
"""

import numpy as np

actions_list = [
    "Run Left",
    "Run Right",
    "Single Punch",
    "Double Punch",
    "Defend",
    "Jump",
    "Jump Left",
    "Jump Right",
    "Jump Punch",
    "Low Kick"
]

action_to_idx_mapping = {}
for i in range(len(actions_list)):
    action_to_idx_mapping[actions_list[i]] = i


class RulesBasedAgentSidai():
  def __init__(self):
      self.type = "rules-based-agent"
      self.random_policy = False

  def select_action(self, state):
      
    (
        relative_distance,
        you_facing_opponent,
        opponent_facing_you,
        your_health,
        opponent_health,
        relative_strength,
        relative_speed,
        relative_defence,
        relative_accuracy
    ) = state[0]

    action = "Single Punch"
    right_side = np.sign(relative_distance) > 0
    abs_distance = abs(relative_distance)
    
    if abs_distance > 0.1:
        if right_side:
            action = "Run Left"
        else:
            action = "Run Right"

    return action_to_idx_mapping[action]


class RulesBasedAgentSihing():
  def __init__(self):
      self.type = "rules-based-agent"
      self.random_policy = False

  def select_action(self, state):
      
    (
        relative_distance,
        you_facing_opponent,
        opponent_facing_you,
        your_health,
        opponent_health,
        relative_strength,
        relative_speed,
        relative_defence,
        relative_accuracy
    ) = state[0]

    action = "Single Punch"
    right_side = np.sign(relative_distance) > 0
    abs_distance = abs(relative_distance)
    
    if abs_distance > 0.15:
        if right_side:
            action = "Run Left"
        else:
            action = "Run Right"
    
    else:
        if (you_facing_opponent == -1 and opponent_facing_you == 1):
            if right_side:
                action = "Jump Left"
            else:
                action = "Jump Right"
      
        elif (you_facing_opponent == 1 and opponent_facing_you == -1):
            if abs_distance <= 0.1:
                if np.random.rand() < 0.5:
                    action = "Single Punch"
                else:
                    action = "Low Kick"
            else:
                if right_side:
                    action = "Run Left"
                else:
                    action = "Run Right"
      
        elif (you_facing_opponent == -1 and opponent_facing_you == -1):
            if right_side:
                action = "Run Left"
            else:
                action = "Run Right"
        else:
            relative_health = your_health - opponent_health
            if (your_health < 0.2 and relative_health < 0):
                if opponent_facing_you == 1:
                    core_action = "Jump"
                else:
                    core_action = "Run"
                    
                if right_side:
                    action_direction = "Left"
                else:
                    action_direction = "Right"
                action = core_action + " " + action_direction
            
            else:
                if np.random.rand() < 0.5:
                    action = "Single Punch"
                else:
                    action = "Low Kick"

    return action_to_idx_mapping[action]

opponents = {
  "Sidai": RulesBasedAgentSidai,
  "Sihing": RulesBasedAgentSihing
}