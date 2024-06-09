import random
import sys
from collections import defaultdict
from typing import Any

import numpy as np


# based on
# https://www.gocoder.one/blog/rl-tutorial-with-openai-gym
# https://github.com/chenmagi/q-cartpole-td0

class QLearning:
    def __init__(self, init_table: dict[Any, dict[Any, float]] = None, learning_rate=0.9, epsilon=1.0,
                 epsilon_decay=0.9999, discount_factor=0.8, log=False, log_file=None):

        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.discount_factor = discount_factor
        self.log = log
        self.log_file = log_file

        # initialize q-value table with initial values (if provided)
        self.q_table = defaultdict(lambda: defaultdict(float))
        if init_table is not None:
            for key in init_table:
                self.q_table[key].update(init_table[key])

        # action map for converting action keys to full actions
        self._action_map = {}

    def train(self, env, num_episodes=1000, max_steps_per_episode=99, eval_every=None, eval_kwargs=None, pbar=True):
        pbar_fn = self.__get_pbar(pbar, desc='evaluating', leave=True)

        history = []
        eval_args = eval_kwargs or {}
        for episode in pbar_fn(range(num_episodes)):
            obs, info = env.reset()
            for step in range(max_steps_per_episode):
                obs, done = self._training_step(env, obs)
                if done:
                    break
            if eval_every is not None and (episode + 1) % eval_every == 0:
                history.append(self.evaluate(env, **eval_args, _leave_pbar=False))

        return history

    def _training_step(self, env, obs):
        action = self.choose_action(env, obs)
        next_obs, r, term, trunc, info = env.step(action)
        best_next_action = self.choose_action(env, next_obs)

        update = r + self.discount_factor * self.q_table[next_obs][best_next_action] - self.q_table[obs][action]

        self.q_table[obs][action] += self.learning_rate * update

        self.epsilon *= self.epsilon_decay

        return next_obs, term or trunc

    def choose_action(self, env, obs, deterministic=False):
        if (not deterministic and random.uniform(0, 1) < self.epsilon) or not self.q_table[obs]:
            # explore
            return env.action_space.sample(obs)
            #TODO the gym API does not require the current state to sample actions.
            # must find a way to sample actions without it in pddlgymnasium.
        else:
            return max(self.q_table[obs].keys(), key=lambda action: self.q_table[obs][action])

    def evaluate(self, env, num_episodes=1, max_steps_per_episode=1000, aggregate_episode_rewards=False, render=False,
                 pbar=True, _leave_pbar=True):
        pbar_fn = self.__get_pbar(pbar, desc='evaluating', leave=_leave_pbar)

        episode_rewards = []
        for episode in pbar_fn(range(num_episodes)):
            acc_rewards = 0
            obs, info = env.reset()
            if render:
                env.render()
            for step in range(max_steps_per_episode):
                action = self.choose_action(env, obs, deterministic=True)
                obs, r, term, trunc, info = env.step(action)
                if render:
                    env.render()
                acc_rewards += self.discount_factor ** step * r
                if term or trunc:
                    break
            episode_rewards.append(acc_rewards)

        if aggregate_episode_rewards:
            return np.mean(episode_rewards)
        else:
            return episode_rewards

    def to_policy(self, env, deterministic=True):
        return lambda obs: self.choose_action(env, obs, deterministic=deterministic)

    @staticmethod
    def __get_pbar(pbar, desc='', leave=False):
        if pbar:
            try:
                from tqdm.auto import tqdm
            except ImportError:
                print('to show a progressbar, you must first install tqdm: `pip install tqdm`', file=sys.stderr)
                raise
            return lambda x: tqdm(x, desc=desc, leave=leave)
        else:
            return lambda x: x
