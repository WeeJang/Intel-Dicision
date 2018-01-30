#!/usr/bin/env python2
#-*- coding:utf-8 -*-



"""
epsilion-greedy 是简单暴力的直接要么随机的去exploration(不考虑之前尝试的结果);
		要么是利用之前的结果继续max推荐

那如何利用历史上已经尝试过的信息呢？

ucb: upper confidence bound。

对于某个菜（选择），真实的good概率为p, 当前尝试过n次，reward list为[reward_0,reward_1,...,reward_i-1] 其中reward 为{0,1}(0为bad,1为good)
因此 可以用均值p~ = sum(reward list) / n 来近似p.
从上面可以看到,当n 趋紧于∞大时，p~趋近于p;
但n代表尝试次数，不可能为无穷大，因此有一个置信区间： p~ - deta <= p <= p~ + delta

因此ucb就是用p~+delta来代替p, 这里p~好计算，关键是delta如何计算？

[Chernoff-Hoeffding Bound]
P{|p~ - p| < a} >= 1 - 2*exp(-2 * n * a^2)
当a = sqart(2* ln(T) / n)时,上式有:(这里T表示有T个客人,n表示菜被吃过的次数),可以得到
P{ |p~ - p| <  sqart(2* ln(T) / n) } >= 1 - 2 / T^4
也就是说 p~ -  sqart(2* ln(T) / n) <= p <= p~ +  sqart(2* ln(T) / n) 以 1 - 2/T^4 的概率成立。
当T=2时，成立概率位0.875；
T=4，成立概率为0.992

可以看出，delta = sqrt(2 * ln T / n)是个不错的选择

"""

import math
import numpy as np

N = 10
total_trials = [0]
true_rewards_prob = np.random.uniform(low = 0,high = 1,size = N)
estimate_reward_prob = np.zeros(N)
reward_counter = np.zeros(N) #访问次数
print true_rewards_prob


def cal_delta(t,pick_item):
	#if t == 0 or reward_counter[pick_item] == 0:
	if reward_counter[pick_item] == 0:
		return 1
	return (2.0 * math.log(t) / (reward_counter[pick_item])) ** 0.5


def UCB(t):
	upper_confidence_bounds =  np.add(estimate_reward_prob,[cal_delta(t,i) for i in range(N)])
	pick_item = np.argmax(upper_confidence_bounds)
	print "pick_item",pick_item
	reward = np.random.binomial(1,true_rewards_prob[pick_item])
	#update
	total_trials[0] += 1
	reward_counter[pick_item] += 1
	estimate_reward_prob[pick_item] = (math.ceil(estimate_reward_prob[pick_item] * (reward_counter[pick_item]-1)) + reward) / (reward_counter[pick_item])	
	

T = 1000000
for i in range(T):
	UCB(i)
	print "estimate_reward_prob",estimate_reward_prob
	print "true",true_rewards_prob
	







