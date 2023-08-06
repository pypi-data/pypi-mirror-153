#    This file is part of NEORL.

#    Copyright (c) 2021 Exelon Corporation and MIT Nuclear Science and Engineering
#    NEORL is free software: you can redistribute it and/or modify
#    it under the terms of the MIT LICENSE

#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 09:33:45 2020

@author: majdi
"""

def evaluate_policy(model, env, log_dir, n_eval_episodes=10, render=False):
    """
    test policy for `n_eval_episodes` episodes and returns reward.
    This is made to work only with one env and single core.
    :param model: The RL agent you want to evaluate.
    :param env: The gym environment.
    :param n_eval_episodes: (int) Number of episode to evaluate the agent
    :param render: (bool) Whether to render the environment or not
    """
    
    """
    if video_record:
        ffmpeg_code=os.system('which ffmpeg')
        if ffmpeg_code == 0: 
            print('--debug: ffmpeg is detected on the machine')
            ffmpeg=subprocess.check_output(['which', 'ffmpeg'])
            ffmpeg.decode('utf-8').strip()
        else:
            raise('The user activated video recording but ffmpeg is not installed on the machine')
    """
    
    episode_rewards, episode_lengths = [], []
    for _ in range(n_eval_episodes):
        obs = env.reset()
        done, state = False, None
        episode_reward = 0.0
        episode_length = 0
        while not done:
            action, state = model.predict(obs, state=state)
            obs, reward, done, _info = env.step(action)
            episode_reward += reward
            episode_length += 1
            #if render:
            #    env.render()
            
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)