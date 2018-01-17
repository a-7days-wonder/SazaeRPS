# -*- coding: utf-8 -*-

#サザエさんのじゃんけんのパターンを学習するプログラム
#サザエさん→前2回の手によって確率で分岐して手を出す
#出す手をランダムで生成し、評価関数によって進化する
#1世代につき100回くらい勝負して、勝率がn割以上の遺伝子を選ぶ？

import numpy as numpy
import matplotlib.pyplot as pyplot
import random

class RPS():
	def __init__(self):
		#初期化
		self.result = ''
		self.preResult = ''
		self.prepreResult = ''

	def updateResult(self):
		#対戦履歴の更新
		self.prepreResult = self.preResult
		self.preResult = self.result

def choose(candidates, probabilities):
    probabilities = [sum(probabilities[:x+1]) for x in range(len(probabilities))]
    if probabilities[-1] > 1.0:
        #確率の合計が100%を超えていた場合は100％になるように調整する
        probabilities = [x/probabilities[-1] for x in probabilities]
    rand = random.random()
    for candidate, probability in zip(candidates, probabilities):
        if rand < probability:
            return candidate
    #どれにも当てはまらなかった場合はNoneを返す
    return None


def judge(player, bot):
	#勝ち:1 負け:2 あいこ:3
	if player == 'G':
		if bot == 'C':
			return 1
		elif bot == 'P':
			return 2

	if player == 'C':
		if bot == 'P':
			return 1
		elif bot == 'G':
			return 2

	if player == 'P':
		if bot == 'G':
			return 1
		elif bot == 'C':
			return 2

def battle(player, bot):
	win = 0
	lose = 0
	draw = 0
	print('----------')
	for count in range(100):
		player.result = random.choice(choice)
		#1回目と2回目はサザエさんはランダムで手を出す
		if count < 2:
			bot.result = random.choice(choice)
		#3回目以降は直前の2つの手によって条件分岐
		else:
			if bot.prepreResult == 'G':
				if bot.preResult == 'G':
					bot.result = choose(choice, probGG)
				if bot.preResult == 'C':
					bot.result = choose(choice, probGC)
				if bot.preResult == 'P':
					bot.result = choose(choice, probGP)

			if bot.prepreResult == 'C':
				if bot.preResult == 'G':
					bot.result = choose(choice, probCG)
				if bot.preResult == 'C':
					bot.result = choose(choice, probCC)
				if bot.preResult == 'P':
					bot.result = choose(choice, probCP)

			if bot.prepreResult == 'P':
				if bot.preResult == 'G':
					bot.result = choose(choice, probPG)
				if bot.preResult == 'C':
					bot.result = choose(choice, probPC)
				if bot.preResult == 'P':
					bot.result = choose(choice, probPP)

		#ジャッジ
		print('ga: '+player.result+'')
		print('sazae: '+bot.result+'')
		if judge(player.result, bot.result) == 1:
			print('Win')
			win += 1
		elif judge(player.result, bot.result) == 2:
			print('Lose')
			lose += 1
		else:
			print('Draw')
			draw += 1
		print('----------')
		bot.updateResult()

	result = float(win) / (float)(win + lose + draw) * 100
	print('勝率: '+str(result)+'%')

ga = RPS()
sazae = RPS()
choice = ['G', 'C', 'P']

probGG = [7.52688172, 51.61290323, 40.86021505]
probGC = [23.42857143, 22.85714286, 53.71428571]
probGP = [17.8343949, 55.41401274, 26.75159236]

probCG = [21.54696133, 28.72928177, 49.72375691]
probCC = [42.85714286, 4.761904762, 52.38095238]
probCP = [47.89473684, 29.47368421, 22.63157895]

probPG = [31.12582781, 49.66887417, 19.20529801]
probPC = [53.06122449, 20.40816327, 26.53061224]
probPP = [37.07865169, 59.5505618, 3.370786517]

battle(ga, sazae)
