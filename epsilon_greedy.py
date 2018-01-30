#!/usr/bin/env python2
#!-*- coding:utf-8 -*-

import math
import numpy as np

N = 10 #菜品个数
true_rewards = np.random.uniform(low=0,high=1,size=N) #N道菜好吃的概率
estimated_rewards = np.zeros(N)
number_of_trials = np.zeros(N)
total_trails = [0]


def get_reward_from_customer(good_prob):
	"""
	客户觉得好不好吃？有菜品的客观好吃概率,主观是否好吃就是一个伯努利分布了（投硬币)
	因此是一个伯努利过程
	param : good_prob,float type,客观好吃概率
	return : int type , 客户主观感觉是否好吃
 		     True : 好吃 False : 不好吃
	"""
	reward = np.random.binomial(1,good_prob)
	if reward == 0:
		return False
	return True
	

def epsilon_greedy(epsilon = 0.1):
	"""
		以epsilon概率去exploration(探索) 未知
		以1-epsilon概率去exploitation(利用) 当前数据
	"""
	r = np.random.uniform()
	pick_item = None
	if r < epsilon:
		pick_item = np.random.randint(low = 0,high=N)
	else:
		pick_item = np.argmax(estimated_rewards)
	
	#客户觉得好不好吃？
	reword = get_reward_from_customer(true_rewards[pick_item])
	number_of_trials[pick_item] += 1				
	total_trails[0] += 1

	is_good = 0
	if reword:
		is_good = 1
	estimated_rewards[pick_item] = math.ceil(estimated_rewards[pick_item] * (number_of_trials[pick_item]-1) + is_good) / number_of_trials[pick_item]
	print "pick",pick_item
	print "cur_estimated_rewards",estimated_rewards
	print "true_rewards",true_rewards



p_n = 100000
for i in range(p_n):
	epsilon_greedy()

			

	


