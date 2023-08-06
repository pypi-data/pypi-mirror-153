# -*- coding: utf-8 -*-
"""
Created on Tue June 1 16:30:41 2018
@author: daniel.velasquez
"""

import numpy as np
import pandas as pd
import numpy.random as random
import matplotlib.pyplot as plt
import datetime as dt
from dateutil.relativedelta import relativedelta as rd

import sys
from .representation import LSTM_Actor
from .representation import LSTM_Bandit
from .representation import LSTM_Critic
from .utils import *

import tensorflow as tf
import copy
from collections import namedtuple, deque
from tf_agents.replay_buffers.tf_uniform_replay_buffer import TFUniformReplayBuffer as replay_buffer

# Working Directory


# from .representation import nn

class Agent:
    """Interacts with and learns from the environment."""

    def __init__(self, asset_names, state_size, action_size, batch_size=64, seed=100):
        """Initialize an Agent object.

        Params
        ======
            state_size (int): dimension of each state
            action_size (int): dimension of each action
            batch_size: minibatch size
            gamma: discount factor
            tau: for soft update of target parameters
            lr: learning rate
        """
        self.asset_names = asset_names
        self.state_size = state_size
        self.action_size = action_size
        self.batch_size = batch_size
        self.seed = seed

    def soft_update(self, local_model, target_model, tau):
        """Soft update model parameters.
        θ_target = τ*θ_local + (1 - τ)*θ_target

        Params
        ======
            local_model: TF model
            target_model: TF model
            tau (float): interpolation parameter
        """
        target_w = [tau*x + (1-tau)*y for x,y in zip(local_model.get_weights(), target_model.get_weights())]
        target_model.set_weights(target_w)


## Q-Learning Agent in discrete action and state spaces.



## LSTM Agent
class LSTMAgent(Agent):
    """Interacts with and learns from the environment."""

    def __init__(self, asset_names, state_size, n_lags, action_size, n_hidden, batch_size=16, lr_actor=1e-4, gamma_risk=2.5,  seed=100):
        super().__init__(asset_names, state_size, action_size, batch_size, seed)
        self.n_lags = n_lags
        self.gamma_risk = tf.constant(gamma_risk, dtype=tf.float32)
        self.actor_local = LSTM_Bandit(state_size, action_size, action_size, n_hidden,'softmax', return_sequences=False, dropout=0.2)
        self.optimizer = tf.keras.optimizers.Adam(lr=lr_actor)

    def act(self, state):
        """Returns actions for given state as per current policy."""
        action = self.actor_local.predict(state)
        return action

    def policy(self, series_df, period='monthly'):
        rets_input = tf.expand_dims(returns(series_df, period)[self.asset_names][-self.n_lags:].values, 0)
        port = pd.Series(tf.squeeze(self.act(rets_input)[0]).numpy(),index=self.asset_names)
        return port

    def loss(self,y, w_pred):
        """
        custom loss arguments are actual observation and model prediction.
        """
        # loss_val = tf.math.negative(tf.math.pow(tf.reduce_prod(tf.math.add(tf.constant(1, dtype=tf.float32), tf.matmul(y, w_pred)), axis=1), tf.math.subtract(tf.constant(1, dtype=tf.float32),self.gamma_risk)))
        # loss_val = tf.math.negative(tf.reduce_mean(tf.matmul(y, w_pred), axis=1) - tf.math.scalar_mul(self.gamma_risk, tf.math.reduce_variance(tf.matmul(y, w_pred), axis=1)))
        loss_val = tf.math.negative(tf.math.divide(tf.reduce_mean(tf.matmul(y, w_pred), axis=1), tf.math.reduce_std(tf.matmul(y, w_pred), axis=1)))
        return loss_val

    def training(self, series_df, n_epochs = 100, period='monthly', hor_in_y=5, verbose=True, save_model=True, model_dir=""):
        port_env = portfolio_environment(series_df[self.asset_names], period, self.n_lags, hor_in_y, None, batch_size=self.batch_size, rl=False, is_return=False)
        port_env.reset() # reset the environment
        self.actor_local.compile(loss=self.loss, optimizer=self.optimizer)
        history = self.actor_local.fit(port_env.dataset, epochs=n_epochs, verbose=verbose)
        if save_model:
            self.actor_local.save_weights(model_dir + "lstm_actor")
        return history

#################
## DDPG
class DDPGAgent(Agent):
    """Interacts with and learns from the environment."""

    def __init__(self, asset_names, state_size, n_lags, action_size, n_hidden, update_every=10, buffer_size=int(1e3), batch_size=16, gamma=0.99, tau=1e-3, lr_actor=1e-4, lr_critic=1e-4, seed=100):
        super().__init__(asset_names, state_size, action_size, batch_size, seed)
        self.gamma = gamma
        self.tau = tau
        self.update_every = update_every
        self.n_lags = n_lags
        self.actor_local = LSTM_Actor(state_size, action_size, action_size, n_hidden, 'softmax', return_sequences=False, dropout=0.2)
        self.actor_target = LSTM_Actor(state_size, action_size, action_size, n_hidden, 'softmax', return_sequences=False, dropout=0.2)
        self.actor_optimizer = tf.keras.optimizers.Adam(lr=lr_actor)
        self.critic_local = LSTM_Critic(state_size, action_size, 1, n_hidden, None, None, return_sequences=False, dropout=0.2)
        self.critic_target = LSTM_Critic(state_size, action_size, 1, n_hidden, None, None, return_sequences=False, dropout=0.2)
        self.critic_optimizer = tf.keras.optimizers.Adam(lr=lr_critic)

        # Noise process
        self.noise = OUNoise((1, action_size), seed, 0., 0.15, sigma=0.05)

        data_spec =  (tf.TensorSpec([n_lags, state_size], tf.float32, "states"),
                      tf.TensorSpec([action_size], tf.float32, 'prev_actions'),
                      tf.TensorSpec([action_size], tf.float32, 'actions'),
                      tf.TensorSpec([1], tf.float32, 'rewards'), tf.TensorSpec([n_lags,state_size], tf.float32, "next_states"),
                      tf.TensorSpec([1], tf.float32, 'done'))

        self.memory = replay_buffer(data_spec, 1, buffer_size)
        self.t_step = 0

    def step(self, states, prev_actions, actions, reward, next_states, done):
        # Save experience in replay memory
        values_batched = tf.nest.map_structure(lambda t: tf.stack([t]), (states, actions, prev_actions, reward, next_states, done))
        self.memory.add_batch(values_batched)

        # Learn every update_every time steps.
        self.t_step = (self.t_step + 1) % self.update_every

        if self.t_step == 0:
            # If enough samples are available in memory, get random subset and learn
            if self.memory.num_frames().numpy() > self.batch_size:
                experiences  = self.memory.get_next(sample_batch_size=self.batch_size, num_steps=1)
                self.learn(experiences, self.gamma)

    def act(self, state, actions, add_noise=True):
        """Returns actions for given state as per current policy."""
        action = self.actor_local.predict([state, actions])
        if add_noise:
            action += self.noise.sample()
        return action/action.sum()

    def training(self, series_df, n_episodes = 100, period='monthly', hor_in_y=5, deque_length=12, model_dir=""):
        port_env = portfolio_environment(series_df[self.asset_names], period, self.n_lags, hor_in_y)
        scores_deque = deque(maxlen=deque_length)
        scores_list = []
        max_score = -np.Inf
        for i_episode in range(1, n_episodes+1):
            port_env.reset() # reset the environment
            score = 0
            while port_env.done==0:
                states = port_env.states
                prev_actions = port_env.prev_actions
                actions = self.act(port_env.states, True)
                port_env.step(actions)           # send all actions to tne environment
                next_states = port_env.states         # get next state (for each agent)
                reward = tf.constant(port_env.reward)
                done = tf.constant(port_env.done, dtype=tf.float32)
                score += port_env.reward                         # update the score (for each agent)
                self.step(states, prev_actions, actions, reward, port_env.states, done)

            scores_deque.append(score)
            scores_list.append(score)
            print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_deque)), end="")
            if i_episode % 100 == 0:
                self.actor_local.save_weights(model_dir + "ddpg_actor")
                self.critic_local.save_weights(model_dir + "ddpg_critic")
                print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_deque)))
        return scores_list

    def learn(self, experiences, gamma):
        """Update policy and value parameters using given batch of experience tuples.
        Q_targets = r + γ * critic_target(next_state, actor_target(next_state))
        where:
            actor_target(state) -> action
            critic_target(state, action) -> Q-value

        Params
        ======
            experiences tuple of (s, a, r, s', done) tuples
            gamma (float): discount factor
        """
        states, actions, rewards, next_states, dones = experiences[0][0][:, 0,:,:], experiences[0][1][:,0,:], experiences[0][2][:,0,:], experiences[0][3][:, 0,:,:], experiences[0][4][:,0,:]
        # ---------------------------- update critic ---------------------------- #
        # Get predicted next-state actions and Q values from target models
        actions_next = self.actor_target(next_states)
        Q_targets_next = self.critic_target([next_states, actions_next])
        # Compute Q targets for current states (y_i)
        Q_targets = rewards + gamma * (1 - dones)* Q_targets_next
        # Compute critic loss
        # ---------------------------- update critic ---------------------------- #
        critic_loss = self.update_critic(states, actions, Q_targets)
        # ---------------------------- update actor ---------------------------- #
        actor_loss = self.update_actor(states)
        # ----------------------- update target networks ----------------------- #
        self.soft_update(self.critic_local, self.critic_target, self.tau)
        self.soft_update(self.actor_local, self.actor_target, self.tau)

    def update_critic(self, states, actions, Q_targets):
        variables = self.critic_local.trainable_variables
        with tf.GradientTape() as tape:
            loss = tf.math.reduce_mean(tf.square(self.critic_local([states, actions], training=True) - Q_targets))
            grads, _ = tf.clip_by_global_norm(tape.gradient(loss, self.critic_local.trainable_variables))
        self.critic_optimizer.apply_gradients(zip(grads, self.critic_local.trainable_variables))
        return loss

    def update_actor(self, states):
        with tf.GradientTape() as tape:
            loss = tf.math.negative(tf.math.reduce_mean(tf.square(self.critic_local([states, self.actor_local(states, training=True)]))))
            grads, _ = tf.clip_by_global_norm(tape.gradient(loss, self.actor_local.trainable_variables), 1.0)
        self.actor_optimizer.apply_gradients(zip(grads, self.actor_local.trainable_variables))
        return loss

    def reset(self):
        self.noise.reset()


class PGAgent(Agent):
    """Interacts with and learns from the environment.
        Policy gradient
    """
    pass


###Tabular Agent

class DiscreteAgent():
    def __init__(self, state_size, action_size, epsilon=0.1, step_size=1, discount=1, seed=100):
        # Store the parameters provided in agent_init_info.
        self.state_size = state_size
        self.action_size = action_size

        self.epsilon = epsilon
        self.step_size = step_size
        self.discount = discount
        self.rand_generator = np.random.RandomState(seed)

        # Create an array for action-value estimates and initialize it to zero.
        self.q = np.zeros((self.state_size, self.action_size)) # The array of action-value estimates.


    def agent_start(self, state):
        """The first method called when the episode starts, called after
        the environment starts.
        Args:
            state (int): the state from the environment's evn_start function.
        Returns:
            action (int): the first action the agent takes.
        """

        # Choose action using epsilon greedy.
        current_q = self.q[state,:]
        if self.rand_generator.rand() < self.epsilon:
            action = self.rand_generator.randint(self.action_size)
        else:
            action = self.argmax(current_q)
        self.prev_state = state
        self.prev_action = action
        return tf.one_hot(action, self.action_size).numpy()

    def argmax(self, q_values):
        """argmax with random tie-breaking
        Args:
            q_values (Numpy array): the array of action-values
        Returns:
            action (int): an action with the highest value
        """
        top = float("-inf")
        ties = []

        for i in range(len(q_values)):
            if q_values[i] > top:
                top = q_values[i]
                ties = []

            if q_values[i] == top:
                ties.append(i)

        return self.rand_generator.choice(ties)

class QLearningAgent(DiscreteAgent):
    def __init__(self, state_size, action_size, epsilon=0.1, step_size=1, discount=1, seed=100):
        super().__init__(state_size, action_size, epsilon, step_size, discount, seed)

    def agent_step(self, reward, state):
        """A step taken by the agent.
        Args:
            reward (float): the reward received for taking the last action taken
            state (int): the state from the environment's step based on where the agent ended up after the last step.
        Returns:
            action (int): the action the agent is taking.
        """

        # Choose action using epsilon greedy.
        current_q = self.q[state, :]
        if self.rand_generator.rand() < self.epsilon:
            action = self.rand_generator.randint(self.action_size)
        else:
            action = self.argmax(current_q)

        # Perform an update (1 line)
        self.q[self.prev_state, self.prev_action] = self.q[self.prev_state, self.prev_action] + self.step_size*(reward + self.discount*np.max(current_q) - self.q[self.prev_state, self.prev_action])

        self.prev_state = state
        self.prev_action = action
        return tf.one_hot(action, self.action_size).numpy()

    def agent_end(self, reward):
        """Run when the agent terminates.
        Args:
            reward (float): the reward the agent received for entering the terminal state.
        """
        # Perform the last update in the episode (1 line)
        self.q[self.prev_state, self.prev_action] = self.q[self.prev_state, self.prev_action] + self.step_size*(reward - self.q[self.prev_state, self.prev_action])


class ExpectedSarsaAgent(DiscreteAgent):
    def __init__(self, state_size, action_size, epsilon=0.1, step_size=1, discount=1, seed=100):
        super().__init__(state_size, action_size, epsilon, step_size, discount, seed)

    def agent_step(self, reward, state):
        """A step taken by the agent.
        Args:
            reward (float): the reward received for taking the last action taken
            state (int): the state from the environment's step based on where the agent ended up after the last step.
        Returns:
            action (int): the action the agent is taking.
        """

        # Choose action using epsilon greedy.
        current_q = self.q[state,:]
        if self.rand_generator.rand() < self.epsilon:
            action = self.rand_generator.randint(self.action_size)
        else:
            action = self.argmax(current_q)

        # Perform an update (~5 lines)
        expec_q = np.max(current_q) * (1 - self.epsilon) + np.sum(current_q * self.epsilon/self.action_size)
        self.q[self.prev_state, self.prev_action] = self.q[self.prev_state, self.prev_action] + self.step_size*(reward + self.discount*expec_q - self.q[self.prev_state, self.prev_action])

        self.prev_state = state
        self.prev_action = action
        return tf.one_hot(action, self.action_size)

    def agent_end(self, reward):
        """Run when the agent terminates.
        Args:
            reward (float): the reward the agent received for entering the
                terminal state.
        """
        # Perform the last update in the episode (1 line)
        self.q[self.prev_state, self.prev_action] = self.q[self.prev_state, self.prev_action] + self.step_size*(reward - self.q[self.prev_state, self.prev_action])


class portfolio_environment:
    def __init__(self, series_df, period, n_lags, hor_in_y, port_ini, batch_size=1, rl=True, reward_type=0, tc=0.0025, is_return=True, ret_type='log'):
        '''
        params:
        =======
        series_df:
        rf: bool. Reinforcement learning environment.
        reward_tye: {0: simple_reward}
        '''
        if port_ini is not None:
            self.prev_actions = tf.convert_to_tensor(port_ini.values[np.newaxis,:], dtype=tf.float32)
        else:
            self.prev_actions = tf.convert_to_tensor((np.ones(series_df.values.shape[1])/len(np.ones(series_df.values.shape[1])))[np.newaxis,:], dtype=tf.float32)
        self.date_ini = series_df.index[0]
        self.date_last = series_df.index[-1]
        self.max_date_ini = self.date_last + relativedelta(years=-hor_in_y)
        self.series = series_df
        self.asset_names = series_df.columns
        self.reward = 0
        self.done = 0
        self.period = period
        self.freq = dict(monthly=12, quarterly=4, semiannualy=2, yearly=1)[period]
        self.rl = rl
        self.hor_in_y = hor_in_y
        self.horizon = hor_in_y * self.freq
        self.times_left = self.horizon
        if self.rl:
            self.time_steps = 1
            self.shuffle_buffer = None
            self.batch_size = 1
        else:
            self.time_steps = self.horizon
            self.shuffle_buffer = 1000
            self.batch_size = batch_size
        self.n_lags = n_lags
        self.dataset = None
        self.iterator = None
        self.size = None
        self.states = None
        self.next_per = None
        self.reward_type = reward_type #reward_fun = (self.simple_reward)[reward_type]
        self.tc = tc
        self.is_return = is_return
        self.ret_type = ret_type

    def reset(self):
        tf.keras.backend.clear_session()
        if self.rl:
            if self.is_return:
                series_start = int(np.random.choice(np.arange(self.n_lags, len(self.series)-self.horizon),1))
                series_batch = self.series[(series_start-self.n_lags):(series_start+self.horizon),:]
            else:
                series_temp = self.series[self.series.index<=self.max_date_ini]
                n_lags_temp = len(self.series.loc[self.series.index <= (self.date_ini + relativedelta(months=self.freq*self.n_lags))])
                date_ref_hor = self.series.index[int(np.random.choice(np.arange(n_lags_temp, len(series_temp)),1))]
                date_ini_hor = date_ref_hor + relativedelta(months=-self.freq*self.n_lags)
                date_last_hor = date_ref_hor + relativedelta(years=self.hor_in_y)
                series_df_hor = self.series.loc[(self.series.index>=date_ini_hor) & (self.series.index<=date_last_hor),:]
                series_batch = returns(series_df_hor, period=self.period, type=self.ret_type).values
        else:
            if self.is_return:
                series_batch = self.series.values
            else:
                series_batch = returns(self.series, period=self.period, type=self.ret_type).values
        self.dataset = tf_windowed_dataset(series_batch, self.n_lags, self.time_steps, self.batch_size, self.shuffle_buffer, output_all=True, output_mean=False)
        self.size = len(list(self.dataset))
        self.iterator = iter(self.dataset)
        # self.states, self.next_per = self.iterator.get_next()
        self.reward = 0
        self.done = 0
        self.time = 0
        self.times_left = self.horizon - self.time

    def step(self, actions):
        self.states, self.next_per = self.iterator.get_next()
        self.reward = self.simple_reward(actions)
        self.time = self.time + 1
        self.times_left = self.horizon - self.time
        prev_actions_temp = actions*np.exp(self.next_per[0,:,:].numpy())
        self.prev_actions = tf.convert_to_tensor(prev_actions_temp/np.sum(prev_actions_temp)) #Previous action updated by return
        if self.time == self.size:
            self.done = 1

    def simple_reward(self, actions):
        reward = np.log((actions @ np.exp(self.next_per[0,:,:].numpy().T))[0] - self.tc*np.sum(np.abs(actions - self.prev_actions)))
        return reward


class OUNoise:
    """Ornstein-Uhlenbeck process."""

    def __init__(self, size, seed, mu=0., theta=0.15, sigma=0.2):
        """Initialize parameters and noise process."""
        self.mu = mu * np.ones(size)
        self.size = size
        self.theta = theta
        self.sigma = sigma
        self.seed = random.seed(seed)
        self.reset()

    def reset(self):
        """Reset the internal state (= noise) to mean (mu)."""
        self.state = copy.copy(self.mu)

    def sample(self):
        """Update internal state and return it as a noise sample."""
        x = self.state
        dx = self.theta * (self.mu - x) + self.sigma * np.random.standard_normal(self.size)#np.array([random.random() for i in range(len(x))])
        self.state = x + dx
        return self.state
