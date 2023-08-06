# AI Arena Python Environment

To get started with our python environment you can run the `training.py` file.

This file shows you how to do a few things in our environment:

* Initialize a new model
* Import a pretrained model
* Set up the game environment
* Run training with one-sided and selfplay reinforcement learning
* Save your model in the format that works with our researcher platform

We have set you up with a starter model in the `starter_model` directory. This is a simple Policy Gradient that implements a version of the [REINFORCE](https://proceedings.neurips.cc/paper/1999/file/464d828b85b0bed98e80ade0a5c43b0f-Paper.pdf) algorithm. We encourage you to replace this with your own models!

Additionally, we set up some basic training loops in the `simulation_methods.py` file. Feel free to change these up and make them your own!

**NOTE:** There are two variables in the `training.py` file which you should not change because our game requires these to be constant:

* `n_features`: This is the dimensionality of the state
* `n_actions`: This is the dimensionality of the policy

Lastly, we have included the rules-based agent `agent_sihing.py` (the researcher platform benchmark) in case you want to train specifically against it. But be careful about overfitting because we will introduce more benchmarks which require generalization...

