#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 14:06:27 2022

@author: brandinho
"""

import json

def save_tf1_model(model):
    weights_data = []
    bias_data = []
    for l in range(len(model.neurons) + 1):
        append_name = str(l)
        if l == len(model.neurons):
            append_name += "Policy"
        weights_data.append(model.sess.run(model.parameters["Weights" + append_name]).tolist())
        if "Bias" + append_name in model.parameters:
            bias_data.append(model.sess.run(model.parameters["Bias" + append_name]).tolist())
    
    model_data = {
        "activation_function": model.activation_function.__name__,
        "output_activation": model.output_activation.__name__,
        "n_features": model.n_features,
        "n_actions": model.n_actions,
        "neurons": model.neurons,
        "weights": weights_data,
        "biases": bias_data
    }
    
    json_string = json.dumps(model_data)
    with open('saved_model/model_tf1.json', 'w') as outfile:
        outfile.write(json_string)
        
def save_tf2_model(model):
    weights_data = []
    bias_data = []
    for layer in model.layers:
        weights_data.append(layer.get_weights()[0].tolist())        
        bias_data.append([layer.get_weights()[1].tolist()])    

    model_data = {
        "activation_function": model.activation_function,
        "output_activation": model.output_activation.__name__,
        "n_features": model.n_features,
        "n_actions": model.n_actions,
        "neurons": list(model.neurons),
        "weights": weights_data,
        "biases": bias_data
    }
    
    json_string = json.dumps(model_data)
    with open('saved_model/model_tf2.json', 'w') as outfile:
        outfile.write(json_string)
        
def save_pytorch_model(model):
    weights_data = []
    bias_data = []
    for layer in model.layers:
        current_parameters = [model.tensor_to_array(params) for params in layer.parameters()]
        weights_data.append(current_parameters[0].T.tolist())
        bias_data.append(current_parameters[1].reshape(-1,1).T.tolist()) 

    model_data = {
        "activation_function": model.activation_function.__name__,
        "output_activation": model.output_activation.__name__,
        "n_features": model.n_features,
        "n_actions": model.n_actions,
        "neurons": list(model.neurons),
        "weights": weights_data,
        "biases": bias_data
    }
    
    json_string = json.dumps(model_data)
    with open('saved_model/model_pytorch.json', 'w') as outfile:
        outfile.write(json_string)        