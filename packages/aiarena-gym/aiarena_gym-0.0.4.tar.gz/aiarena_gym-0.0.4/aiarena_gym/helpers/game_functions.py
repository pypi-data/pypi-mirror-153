from aiarena_gym.helpers.game_parameters import game_parameters
import numpy as np

max_consecutive_actions = 10


def scale_attribute(percentage, min_value, max_value):
    return min_value + (max_value - min_value) * percentage


def adjust_power(base_power, consecutive_actions):
    return base_power * max(max_consecutive_actions - consecutive_actions, 0) / max_consecutive_actions


def get_damage(action, current_power, other_defence, consecutive_actions, shield_hit):
    base_damage = scale_attribute(
        adjust_power(current_power, consecutive_actions) / 100, 
        game_parameters['min_damage'], 
        game_parameters['max_damage']
    )
    hit_damage = 0
    if "Punch" in action:
        hit_damage = base_damage * game_parameters['punch_power_multiple']
    elif "Low Kick" in action:
        hit_damage = base_damage * game_parameters['low_kick_power_multiple']

    if shield_hit:
        hit_damage *= (1 - other_defence / 100)

    return hit_damage

def get_state(your_state, opponent_state, your_attributes, opponent_attributes):
    relative_distance = your_state["x"] - opponent_state["x"]
    return np.array([[
        relative_distance,
        your_state["direction"] * np.sign(relative_distance) * -1,
        opponent_state["direction"] * np.sign(relative_distance),
        your_state["health"],
        opponent_state["health"],
        (your_attributes["power"] - opponent_attributes["power"]) / 100,
        (your_attributes["speed"] - opponent_attributes["speed"]) / 100,
        (your_attributes["defence"] - opponent_attributes["defence"]) / 100,
        (your_attributes["accuracy"] - opponent_attributes["accuracy"]) / 100,
    ]])