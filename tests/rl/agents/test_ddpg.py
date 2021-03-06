from __future__ import division
from __future__ import absolute_import

import pytest
import numpy as np
from numpy.testing import assert_allclose

from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Input, Dense, Flatten, Concatenate

from rl.agents.ddpg import DDPGAgent
from rl.memory import SequentialMemory
from rl.processors import MultiInputProcessor

from ..util import MultiInputTestEnv


def test_single_ddpg_input():
    nb_actions = 2

    actor = Sequential()
    actor.add(Flatten(input_shape=(2, 3)))
    actor.add(Dense(nb_actions))

    action_input = Input(shape=(nb_actions,), name='action_input')
    observation_input = Input(shape=(2, 3), name='observation_input')
    x = Concatenate()([action_input, Flatten()(observation_input)])
    x = Dense(1)(x)
    critic = Model(inputs=[action_input, observation_input], outputs=x)

    memory = SequentialMemory(limit=10, window_length=2)
    agent = DDPGAgent(actor=actor, critic=critic, critic_action_input=action_input, memory=memory,
                      nb_actions=2, nb_steps_warmup_critic=5, nb_steps_warmup_actor=5, batch_size=4)
    agent.compile('sgd')
    agent.fit(MultiInputTestEnv((3,)), nb_steps=10)


def test_multi_ddpg_input():
    nb_actions = 2

    actor_observation_input1 = Input(shape=(2, 3), name='actor_observation_input1')
    actor_observation_input2 = Input(shape=(2, 4), name='actor_observation_input2')
    actor = Sequential()
    x = Concatenate()([actor_observation_input1, actor_observation_input2])
    x = Flatten()(x)
    x = Dense(nb_actions)(x)
    actor = Model(inputs=[actor_observation_input1, actor_observation_input2], outputs=x)

    action_input = Input(shape=(nb_actions,), name='action_input')
    critic_observation_input1 = Input(shape=(2, 3), name='critic_observation_input1')
    critic_observation_input2 = Input(shape=(2, 4), name='critic_observation_input2')
    x = Concatenate()([critic_observation_input1, critic_observation_input2])
    x = Concatenate()([action_input, Flatten()(x)])
    x = Dense(1)(x)
    critic = Model(inputs=[action_input, critic_observation_input1, critic_observation_input2], outputs=x)

    processor = MultiInputProcessor(nb_inputs=2)
    memory = SequentialMemory(limit=10, window_length=2)
    agent = DDPGAgent(actor=actor, critic=critic, critic_action_input=action_input, memory=memory,
                      nb_actions=2, nb_steps_warmup_critic=5, nb_steps_warmup_actor=5, batch_size=4,
                      processor=processor)
    agent.compile('sgd')
    agent.fit(MultiInputTestEnv([(3,), (4,)]), nb_steps=10)
