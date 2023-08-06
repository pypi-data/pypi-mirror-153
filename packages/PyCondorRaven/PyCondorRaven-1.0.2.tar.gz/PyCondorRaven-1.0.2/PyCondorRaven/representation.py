# -*- coding: utf-8 -*-
"""
Created on Tue June 1 16:30:41 2018
@author: daniel.velasquez
"""

import numpy as np
import pandas as pd
import datetime as dt
import tensorflow as tf
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torch.optim as optim

class LSTM_Bandit(tf.keras.Model):
    """Actor (Policy) Model."""
    def __init__(self, state_size, action_size, n_output, n_hidden,  output_activation=None, return_sequences=False, dropout=0, tc=False):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
        """
        super(LSTM_Bandit, self).__init__()
        input_shape=[None, state_size] # n_lags x state size
        self.tc = tc
        self.lstm_layer = tf.keras.models.Sequential([
          tf.keras.layers.LSTM(n_hidden, return_sequences=return_sequences, dropout=dropout, recurrent_dropout=dropout, stateful=False, input_shape=input_shape),
          tf.keras.layers.Dense(int(n_hidden/2), activation="relu"),
          tf.keras.layers.Dense(n_output, activation=output_activation)
        ])

    @tf.function
    def call(self, input, training=False):
        '''
        input: (lagged series, states)
        '''
        return tf.expand_dims(self.lstm_layer(input, training=training), axis=-1)


class LSTM_Actor(tf.keras.Model):
    """Actor (Policy) Model."""
    def __init__(self, state_size, action_size, n_output, n_hidden, output_activation=None, return_sequences=False, dropout=0):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
        """
        super(LSTM_Actor, self).__init__()
        self.lstm_layer = tf.keras.models.Sequential([
          tf.keras.layers.LSTM(n_hidden, return_sequences=return_sequences, dropout=dropout, recurrent_dropout=dropout, stateful=False, input_shape=[None, state_size]),
          tf.keras.layers.Dense(int(n_hidden/2), activation="relu")#,
        ])
        self.output_layer = tf.keras.layers.Dense(n_output, activation=output_activation)

    @tf.function
    def call(self, input, training=False):
        '''
        input: (lagged series, actions, horizon)
        '''
        x = self.lstm_layer(input[0], training=training)
        return self.output_layer(tf.concat([x,input[1], input[2]], 1))

class LSTM_Critic(tf.keras.Model):
    """Critic (Policy) Model."""
    def __init__(self, state_size, action_size, n_output, n_hidden, lstm_activation=None, output_activation=None, return_sequences=False, dropout=0):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
        """
        super(LSTM_Critic, self).__init__()
        self.lstm_layer = tf.keras.models.Sequential([
          tf.keras.layers.LSTM(n_hidden, return_sequences=return_sequences, dropout=dropout, recurrent_dropout=dropout, stateful=False, input_shape=[None, state_size]),
          tf.keras.layers.Dense(n_output, activation=lstm_activation)#,
          # tf.keras.layers.Lambda(lambda x: x * 400)
        ])
        self.output_layer = tf.keras.layers.Dense(1, activation=output_activation)

    @tf.function
    def call(self, input, training=False):
        '''
        input: (lagged series, actions, horizon)
        '''
        x = self.lstm_layer(input[0], training=training)
        return self.output_layer(tf.concat([x,input[1],input[2]], 1))

class QNetwork(tf.keras.Model):
    """Q network."""

    def __init__(self, state_size, action_size, n_hidden=8, activation='relu', dropout=0):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
        """
        super(QNetwork, self).__init__()
        self.model = tf.keras.models.Sequential([
          tf.keras.layers.Dense(n_hidden, activation="relu",input_shape=[None, state_size]),
          tf.keras.layers.Dropout(dropout),
          tf.keras.layers.Dense(action_size, activation=None)#,
        ])

    @tf.function
    def call(self, state, training=False):
        return self.model(state)
#
# #################
#
# def hidden_init(layer):
#     fan_in = layer.weight.data.size()[0]
#     lim = 1. / np.sqrt(fan_in)
#     return (-lim, lim)
#
# class Actor(nn.Module):
#     """Actor (Policy) Model."""
#
#     def __init__(self, state_size, action_size, seed, fc1_units=256, fc2_units=128):
#         """Initialize parameters and build model.
#         Params
#         ======
#             state_size (int): Dimension of each state
#             action_size (int): Dimension of each action
#             seed (int): Random seed
#             fc1_units (int): Number of nodes in first hidden layer
#             fc2_units (int): Number of nodes in second hidden layer
#         """
#         super(Actor, self).__init__()
#         self.seed = torch.manual_seed(seed)
#         self.fc1 = nn.Linear(state_size, fc1_units)
#         #self.bn1 = nn.BatchNorm1d(fc1_units)
#         self.fc2 = nn.Linear(fc1_units, fc2_units)
#         #self.bn2 = nn.BatchNorm1d(fc2_units)
#         self.output = nn.Linear(fc2_units, action_size)
#         self.reset_parameters()
#
#     def reset_parameters(self):
#         self.fc1.weight.data.uniform_(*hidden_init(self.fc1))
#         self.fc2.weight.data.uniform_(*hidden_init(self.fc2))
#         self.output.weight.data.uniform_(-3e-3, 3e-3)
#
#     def forward(self, state):
#         """Build an actor (policy) network that maps states -> actions."""
#         x = F.relu(self.fc1(state))
#         x = F.relu(self.fc2(x))
#         ## Softmax output
#         return F.softmax(self.output(x))
#
#
# class Critic(nn.Module):
#     """Critic (Value) Model."""
#
#     def __init__(self, state_size, action_size, seed, fcs1_units=256, fc2_units=128, fc3_units=64):
#         """Initialize parameters and build model.
#         Params
#         ======
#             state_size (int): Dimension of each state
#             action_size (int): Dimension of each action
#             seed (int): Random seed
#             fcs1_units (int): Number of nodes in the first hidden layer
#             fc2_units (int): Number of nodes in the second hidden layer
#         """
#         super(Critic, self).__init__()
#         self.seed = torch.manual_seed(seed)
#         self.fcs1 = nn.Linear(state_size, fcs1_units)
#         #self.bn1 = nn.BatchNorm1d(fcs1_units)
#         self.fc2 = nn.Linear(fcs1_units+action_size, fc2_units)
#         #self.bn2 = nn.BatchNorm1d(fc2_units)
#         self.fc3 = nn.Linear(fc2_units, fc3_units)
#         self.fc4 = nn.Linear(fc3_units, 1)
#         self.reset_parameters()
#
#     def reset_parameters(self):
#         self.fcs1.weight.data.uniform_(*hidden_init(self.fcs1))
#         self.fc2.weight.data.uniform_(*hidden_init(self.fc2))
#         self.fc3.weight.data.uniform_(*hidden_init(self.fc3))
#         self.fc4.weight.data.uniform_(-3e-3, 3e-3)
#
#     def forward(self, state, action):
#         """Build a critic (value) network that maps (state, action) pairs -> Q-values."""
#         xs = F.relu(self.fcs1(state))
#         x = torch.cat((xs, action), dim=1)
#         x = F.relu(self.fc2(x))
#         #x = F.leaky_relu(self.fc3(x))
#         return self.fc4(x)
