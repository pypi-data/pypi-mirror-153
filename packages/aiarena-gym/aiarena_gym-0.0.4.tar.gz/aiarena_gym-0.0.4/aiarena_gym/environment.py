#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 09:39:22 2021

@author: brandinho
"""

import numpy as np
from aiarena_gym.helpers.game_parameters import game_parameters
from aiarena_gym.helpers.game_functions import get_damage, scale_attribute, get_state


class Game():
    def __init__(self, seconds = 60):
        self.left_bounds = 0 + game_parameters['character_width'] / 2
        self.right_bounds = 1 - game_parameters['character_width'] / 2
        self.char_fraction = game_parameters['character_width'] / \
            game_parameters['char_fraction_denominator']

        self.seconds = seconds
        self.animation_speed = 0.05  # 50 milliseconds
        self.max_animation_frames = self.seconds / self.animation_speed
        self.jump_time_ratio = game_parameters['jump_multiple'] / \
            game_parameters['default_multiple']

        self.animation_states = {0: [], 1: []}
        self.pending_action = {0: None, 1: None}
        self.consecutive_actions = {0: 0, 1: 0}

        self.actions_list = [
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
        self.animation_frames = {
            "Get Hit": 3,
            "Run Left": 9,
            "Run Right": 9,
            "Single Punch": 4,
            "Double Punch": 9,
            "Defend": 7,
            "Start Defend": 4,
            "Continue Defend": 4,
            "Hit Shield": 2,
            "End Defend": 2,
            "Stun": 23,
            "Jump": 10 + 5,
            "Jump Left": 10 + 5,
            "Jump Right": 10 + 5,
            "Jump Punch": 10 + 5,
            "Low Kick": 8
        }
        
    @staticmethod
    def get_random_start_position():
        your_starting_location = np.random.choice([0.2, 0.8])
        opponent_starting_location = np.round(1 - your_starting_location, 1)
        your_starting_direction = int(np.sign(0.5 - your_starting_location))
        opponent_starting_direction = -1 * your_starting_direction
        return [
            your_starting_location,
            opponent_starting_location,
            your_starting_direction,
            opponent_starting_direction
        ]

    def load_fighters(self, your_model, opponent_model, your_attributes, opponent_attributes):
        (
            your_starting_location,
            opponent_starting_location,
            your_starting_direction,
            opponent_starting_direction
        ) = self.get_random_start_position()
        self.your_fighter = {
            "model": your_model,
            "battle_attributes": your_attributes,
            "state": {
                "x": your_starting_location,
                "y": 0,
                "shield_health": game_parameters['shield_health'] / 100,
                "direction": your_starting_direction,
                "health": 1,
                "action": "Nothing",
                "frames_before_unlocking": 0
            }
        }
        self.opponent_fighter = {
            "model": opponent_model,
            "battle_attributes": opponent_attributes,
            "state": {
                "x": opponent_starting_location,
                "y": 0,
                "shield_health": game_parameters['shield_health'] / 100,
                "direction": -1 * your_starting_direction,
                "health": 1,
                "action": "Nothing",
                "frames_before_unlocking": 0
            }
        }
        self.fighters = [self.your_fighter, self.opponent_fighter]
        return self.your_fighter["state"], self.opponent_fighter["state"]

    def reset(self, randommize_attributes=False, random_policy=False, randomize_side=True):
        self.animation_frame = 0
        if randommize_attributes:
            self.your_fighter["battle_attributes"] = {
                "power": np.random.rand() * 100,
                "speed": np.random.rand() * 100,
                "defence": np.random.rand() * 100,
                "accuracy": np.random.rand() * 100,
            }
            self.opponent_fighter["battle_attributes"] = {
                "power": np.random.rand() * 100,
                "speed": np.random.rand() * 100,
                "defence": np.random.rand() * 100,
                "accuracy": np.random.rand() * 100,
            }
        if randomize_side:
            (
                your_starting_location,
                opponent_starting_location,
                your_starting_direction,
                opponent_starting_direction
            ) = self.get_random_start_position()
                    
            self.your_fighter["state"]["x"] = your_starting_location
            self.opponent_fighter["state"]["x"] = opponent_starting_location
            self.your_fighter["state"]["direction"] = your_starting_direction
            self.opponent_fighter["state"]["direction"] = opponent_starting_direction
            
        if random_policy:
            self.opponent_fighter["model"].random_policy = True
        else:
            self.opponent_fighter["model"].random_policy = False

        return self.load_fighters(
            self.your_fighter["model"],
            self.opponent_fighter["model"],
            self.your_fighter["battle_attributes"],
            self.opponent_fighter["battle_attributes"]
        )

    def switch_opponent(self, new_opponent):
        self.opponent_fighter["model"] = new_opponent
        self.fighters = [self.your_fighter, self.opponent_fighter]

    def swap_fighters(self):
        temp = self.your_fighter
        self.your_fighter = self.opponent_fighter
        self.opponent_fighter = temp
        self.fighters = [self.your_fighter, self.opponent_fighter]

    def scale_specific_attribute(self, fighter, attribute):
        scaledAttribute = fighter["battle_attributes"][attribute]
        if attribute == "speed":
            scaledAttribute = scale_attribute(
                fighter['battle_attributes']['speed'] / 100, 
                game_parameters['min_speed'], 
                game_parameters['max_speed']
            )
        elif attribute == "power":
            scaledAttribute = scale_attribute(
                fighter['battle_attributes']['power'] / 100, 
                game_parameters['min_damage'], 
                game_parameters['max_damage']
            )
        return scaledAttribute

    def shift_vertical(self, jump_frame, action):
        new_y = None
        vertical_multiple = game_parameters['jump_multiple'] * 0.5

        if jump_frame == 3:
            new_y = vertical_multiple * 0.65 / 2
        elif jump_frame == 4:
            new_y = vertical_multiple * 0.65

        if "Punch" not in action:
            if jump_frame == 4 + 1:
                new_y = vertical_multiple * (0.65 + 0.74) / 2
            elif jump_frame == 4 + 2:
                new_y = vertical_multiple * 0.74
            elif jump_frame == 5 + 2:
                new_y = vertical_multiple * (0.74 + 0.8) / 2
            elif jump_frame == 5 + 3:
                new_y = vertical_multiple * 0.8
            elif jump_frame == 6 + 3:
                new_y = vertical_multiple * (0.8 + 0.47) / 2
            elif jump_frame == 6 + 4:
                new_y = vertical_multiple * 0.47
            elif jump_frame == 7 + 4:
                new_y = vertical_multiple * 0.47 / 2
            elif jump_frame == 7 + 5:
                new_y = 0
        elif "Punch" in action:
            if jump_frame == 5 + 2:
                new_y = vertical_multiple * (0.65 + 0.78) / 2
            elif jump_frame == 5 + 3:
                new_y = vertical_multiple * 0.78
            elif jump_frame == 6 + 3:
                new_y = vertical_multiple * (0.78 + 0.7) / 2
            elif jump_frame == 6 + 4:
                new_y = vertical_multiple * 0.7
            elif jump_frame == 7 + 4:
                new_y = vertical_multiple * (0.7 + 0.58) / 2
            elif jump_frame == 7 + 5:
                new_y = vertical_multiple * 0.58
            elif jump_frame == 8 + 5:
                new_y = vertical_multiple * 0.58 / 2
            elif jump_frame == 8 + 6:
                new_y = 0
        return new_y

    def move_fighter(self, current_fighter, other_fighter, current_x, other_x, current_y, other_y, action):
        new_x = current_x
        space_between_fighters = 0
        step_size = self.scale_specific_attribute(current_fighter, "speed")
        speed_up = 1.25 if current_y > 0 else 1
        marginal_step_size = speed_up * \
            step_size / self.animation_frames[action]
        free_space = abs(current_y - other_y) > game_parameters['vertical_jump_clearance']

        if "Jump" in action and current_fighter["state"]["frames_before_unlocking"] == self.animation_frames[action]:
            new_x = current_x
        else:
            other_defending = "Defend" in other_fighter['state']['action']
            if "Left" in action:
                if current_x < other_x or free_space:
                    new_x = max(current_x - marginal_step_size, self.left_bounds)
                else:
                    current_left_bound = current_x - self.char_fraction
                    other_right_bound = other_x + self.char_fraction
                    if (
                        other_defending and 
                        other_fighter['state']['direction'] == 1 and 
                        current_x - other_x < game_parameters['shield_distance']
                    ):
                        space_between_fighters = current_x - other_x - game_parameters['shield_distance']
                    else:
                        space_between_fighters = current_left_bound - other_right_bound
                    new_x = current_x - min(marginal_step_size, space_between_fighters)
            elif "Right" in action:
                if current_x > other_x or free_space:
                    new_x = min(current_x + marginal_step_size, self.right_bounds)
                else:
                    current_right_bound = current_x + self.char_fraction
                    other_left_bound = other_x - self.char_fraction
                    if (
                        other_defending and 
                        other_fighter['state']['direction'] == -1 and 
                        other_x - current_x < game_parameters['shield_distance']
                    ):
                        space_between_fighters = other_x - current_x - game_parameters['shield_distance']
                    else:
                        space_between_fighters = other_left_bound - current_right_bound
                    new_x = current_x + min(marginal_step_size, space_between_fighters)
        return new_x

    def adjust_landing_position(self, current_x, other_x, current_y, other_y):
        new_x = current_x
        if abs(current_y - other_y) < game_parameters['vertical_jump_clearance']:
            horizontal_spacing = current_x - other_x
            if abs(horizontal_spacing) < self.char_fraction:
                if (
                    (horizontal_spacing < 0 and other_x > self.left_bounds + game_parameters['character_width']) or
                    (other_x > self.right_bounds - game_parameters['character_width'])
                ):
                    new_x = other_x - self.char_fraction
                else:
                    new_x = other_x + self.char_fraction
        return new_x

    def is_defending(self, current_fighter, other_fighter):
        defended = False
        other_action = other_fighter['state']['action']
        if "Defend" in other_action and other_action != "End Defend":
            if current_fighter['state']['x'] < other_fighter['state']['x'] and current_fighter['state']['direction'] == -1:
                defended = True
            elif current_fighter['state']['x'] > other_fighter['state']['x'] and current_fighter['state']['direction'] == 1:
                defended = True

        return defended

    def adjust_position_defend(self, current_fighter, other_fighter):
        current_x = current_fighter['state']['x']
        other_x = other_fighter['state']['x']
        space_between = abs(current_x - other_x)

        new_current_x = current_x
        new_other_x = other_x
        if space_between < game_parameters['shield_distance']:
            if (current_x < other_x and current_fighter['state']['direction'] == 1):
                new_other_x = current_x + game_parameters['shield_distance']
                if new_other_x > self.right_bounds:
                    new_other_x = self.right_bounds
                    new_current_x = new_other_x - game_parameters['shield_distance']
            elif current_x > other_x and current_fighter['state']['direction'] == -1:
                new_other_x = current_x - game_parameters['shield_distance']
                if new_other_x < self.left_bounds:
                    new_other_x = self.left_bounds
                    new_current_x = new_other_x + game_parameters['shield_distance']
        return [new_current_x, new_other_x]

    def is_in_range(self, direction, current_x, other_x, current_y, other_y, action):
        vertical_alignment = False
        hit_extension = 0
        if action == "Low Kick":
            vertical_alignment = current_y == 0 and other_y < game_parameters['vertical_low_kick_hitbox']
            hit_extension = game_parameters['low_kick_extension']
        elif "Punch" in action:
            vertical_alignment = abs(current_y - other_y) < game_parameters['vertical_punch_hitbox']
            hit_extension = game_parameters['punch_extension']

        fighter_in_range = False
        shield_in_range = False

        if vertical_alignment:
            if direction == 1 and other_x > current_x:
                current_right_bound = current_x + self.char_fraction
                other_left_bound = other_x - self.char_fraction
                other_shield_bound = other_x - game_parameters['shield_distance']
                if current_right_bound + hit_extension > other_left_bound:
                    fighter_in_range = True
                if current_right_bound + hit_extension > other_shield_bound:
                    shield_in_range = True
            elif direction == -1 and other_x < current_x:
                current_left_bound = current_x - self.char_fraction
                other_right_bound = other_x + self.char_fraction
                other_shield_bound = other_x + game_parameters['shield_distance']
                if current_left_bound - hit_extension < other_right_bound:
                    fighter_in_range = True
                if current_left_bound - hit_extension < other_shield_bound:
                    shield_in_range = True
        return [fighter_in_range, shield_in_range]

    def is_hit_landing_frame(self, action, frames_before_unlocking):
        hit_landing_frame = False

        if "Jump" in action:
            hit_landing_frame = (self.animation_frames[action] - frames_before_unlocking) == 9
        elif "Punch" in action:
            hit_landing_frame = (self.animation_frames[action] - frames_before_unlocking) == 2
            if action == "Double Punch":
                hit_landing_frame = hit_landing_frame or frames_before_unlocking == 3
        elif "Kick" in action:
            hit_landing_frame = (self.animation_frames[action] - frames_before_unlocking) == 4
        return hit_landing_frame

    def state_transition(self, which_fighter, action):
        current_fighter = self.fighters[which_fighter]
        other_fighter = self.fighters[(which_fighter + 1) % 2]

        current_x = current_fighter["state"]["x"]
        other_x = other_fighter["state"]["x"]
        current_y = current_fighter["state"]["y"]
        other_y = other_fighter["state"]["y"]

        frames_before_unlocking = self.fighters[which_fighter]["state"]["frames_before_unlocking"]

        new_current_x = current_x
        new_other_x = other_x
        if "Left" in action or "Right" in action:
            new_current_x = self.move_fighter(
                current_fighter, 
                other_fighter, 
                current_x, 
                other_x, 
                current_y, 
                other_y, 
                action
            )
            new_direction = -1 if "Left" in action else 1
            self.fighters[which_fighter]["state"]["x"] = new_current_x
            self.fighters[which_fighter]["state"]["direction"] = new_direction

        if "Jump" in action:
            jump_frame = self.animation_frames[action] - frames_before_unlocking + 1
            new_current_y = self.shift_vertical(jump_frame, action)
            new_current_x = self.adjust_landing_position(new_current_x, other_x, current_y, other_y)
            self.fighters[which_fighter]["state"]["x"] = new_current_x
            if new_current_y is not None:
                self.fighters[which_fighter]["state"]["y"] = new_current_y

        if action == "Start Defend":
            [new_current_x, new_other_x] = self.adjust_position_defend(current_fighter, other_fighter)
            current_fighter['state']['x'] = new_current_x
            other_fighter['state']['x'] = new_other_x

        if "Punch" in action or "Kick" in action:
            is_accurate_hit = np.random.rand() < current_fighter['battle_attributes']['accuracy'] / 100
            hit_landing_frame = self.is_hit_landing_frame(action, frames_before_unlocking)
            if (is_accurate_hit and hit_landing_frame):
                [fighter_in_range, shield_in_range] = self.is_in_range(
                    current_fighter['state']['direction'], 
                    current_x, 
                    other_x, 
                    current_y, 
                    other_y, 
                    action
                )
                damage_parameters = [
                    action, 
                    current_fighter['battle_attributes']['power'],
                    other_fighter['battle_attributes']['defence'], 
                    self.consecutive_actions[which_fighter]
                ]
                if self.is_defending(current_fighter, other_fighter):
                    if shield_in_range:
                        shield_damage = get_damage(*damage_parameters, True)
                        other_fighter['state']['shield_health'] = max(
                            other_fighter['state']['shield_health'] - shield_damage, 0
                        )
                        other_fighter['state']['action'] = "Hit Shield"
                        other_fighter['state']['frames_before_unlocking'] = self.animation_frames['Hit Shield'] + 1
                elif fighter_in_range:
                    damage = get_damage(*damage_parameters, False)
                    other_fighter['state']['health'] = max(
                        other_fighter['state']['health'] - damage, 0
                    )
                    other_fighter['state']['action'] = "Get Hit"
                    other_fighter['state']['frames_before_unlocking'] = self.animation_frames['Get Hit'] + 1

        self.fighters[which_fighter]['state']['action'] = action

    def check_game_over(self):
        your_health = self.fighters[0]["state"]["health"]
        opponent_health = self.fighters[1]["state"]["health"]

        winner = None
        game_over = False
        if self.animation_frame == self.max_animation_frames - 1:
            game_over = True
        elif your_health <= 0 or opponent_health <= 0:
            game_over = True

        if game_over:
            if your_health > opponent_health:
                winner = "You"
            elif your_health < opponent_health:
                winner = "Opponent"
            else:
                winner = "Tie"
        return game_over, winner

    def perform_action(self, action_idx, which_fighter):
        if self.fighters[which_fighter]["state"]["frames_before_unlocking"] == 0:
            if (which_fighter == 1):
                opponent_state = get_state(
                    self.opponent_fighter["state"],
                    self.your_fighter["state"],
                    self.opponent_fighter["battle_attributes"],
                    self.your_fighter["battle_attributes"]
                )
                action_idx = self.opponent_fighter["model"].select_action(opponent_state)
            action = self.actions_list[action_idx]
            self.fighters[which_fighter]["state"]["frames_before_unlocking"] = self.animation_frames[action]
            self.state_transition(which_fighter, action)
        else:
            self.state_transition(
                which_fighter, self.fighters[which_fighter]["state"]["action"])
            self.fighters[which_fighter]["state"]["frames_before_unlocking"] -= 1

        if which_fighter == 1:
            self.animation_frame += 1

    def step(self, action_idx):
        self.perform_action(action_idx, 0)
        game_over, winner = self.check_game_over()
        for _ in range(self.fighters[0]["state"]["frames_before_unlocking"]):
            if not game_over:
                self.perform_action(None, 1)
                game_over, winner = self.check_game_over()
                if self.fighters[0]["state"]["frames_before_unlocking"] != 0:
                    self.perform_action(None, 0)
                    game_over, winner = self.check_game_over()
        return self.your_fighter["state"], self.opponent_fighter["state"], game_over, winner
