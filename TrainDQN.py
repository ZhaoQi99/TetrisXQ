# -*- coding: utf-8 -*-
import os
import random

import numpy as np
import tensorflow as tf

from Settings import Settings
from TrainInfo import TrainInfo
from agent.dqn.QMLPModel import QMLPModel
from agent.dqn.data.BatchManager import BatchManager
from environment.player.HumanPlayer import HumanPlayer
from environment.player.TetrisAIPlayer import TetrisAIPlayer
from graphics.DummyGraphicModule import DummyGraphicModule
from graphics.GraphicModule import GraphicModule

SAVE_POINT = 20
USE_GRAPHIC_INTERFACE = True
ENVIRONMENT_TYPE = 'AI'


def main(_):
    settings = Settings()

    epsilon = settings.START_EPSILON

    with tf.Session() as sess:
        train_info = TrainInfo(settings)

        q_network_model = QMLPModel(settings)
        batch_module = BatchManager(settings)
        graphic_interface = DummyGraphicModule()
        if USE_GRAPHIC_INTERFACE:
            graphic_interface = GraphicModule(settings, train_info)
        if ENVIRONMENT_TYPE == 'HUMAN':
            env_model = HumanPlayer(settings, graphic_interface)
        else:
            env_model = TetrisAIPlayer(settings, graphic_interface)

        train_step = 0
        merged_summary = tf.summary.merge_all()
        writer = tf.summary.FileWriter('./train/log/train_log', sess.graph)

        init = tf.global_variables_initializer()
        sess.run(init)
        print("훈련 시작: " + str(settings.LEARNING_EPOCH) + " 게임 학습...")
        for index in range(settings.LEARNING_EPOCH):
            turn_count = 0
            current_end = False
            current_state = env_model.get_current_state()

            while not current_end:
                train_step += 1
                if turn_count >= settings.MAX_TURNS:
                    break

                if (float(random.randrange(0, 9999)) / 10000) <= epsilon:
                    action = random.randrange(0, settings.ACTIONS)
                else:
                    q_values = q_network_model.get_forward(sess, current_state)[0]
                    action = np.argmax(q_values)

                if epsilon > settings.MIN_EPSILON:
                    epsilon = epsilon * 0.999

                next_state, reward, next_end = env_model.action_and_reward(action)
                batch_module.add_data(current_state, next_state, action, reward)

                current_state = next_state
                current_end = next_end

                input_state, target_values = batch_module.get_batch(sess, q_network_model.get_target_value)
                summary, cost = q_network_model.optimize_step(sess, input_state, target_values, merged_summary)
                writer.add_summary(summary, train_step)

            train_info.current_epoch = index + 1
            print("epoch: " + str(train_info.current_epoch) + " 전체 step: " + str(train_step) + " 총 점수: " + str(round(env_model.tetris_model.score)) +
                  " 진행 턴 수: " + str(env_model.tetris_model.turns) + " 무작위 행동: " + str(round(epsilon * 100)))

            if train_info.current_epoch % SAVE_POINT == 0:
                print("모델 저장됨: " + tf.train.Saver().save(sess, os.getcwd() + "./train/saved_model/saved_model_DQN_TetrisXQ.ckpt"))

        writer.close()
        print("훈련 종료: " + str(settings.LEARNING_EPOCH) + " 게임 학습 완료")


if __name__ == '__main__':
    tf.app.run()