# -*- coding: utf-8 -*-

#サザエさんのじゃんけんのパターンを学習するプログラム
#サザエさん→前2回の手によって確率で分岐して手を出す
#出す手をランダムで生成し、評価関数によって進化する
#1世代につき100回くらい勝負して、勝率がn割以上の遺伝子を選ぶ？

import numpy as np
import matplotlib.pyplot as plt
import random
from decimal import Decimal
import GeneticAlgorithm as ga

class bot(object): #サザエさん用クラス
	def __init__(self):
		#初期化
		self.result = None
		self.preResult = None
		self.prepreResult = None

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

def create_genom(length):
	genome_list = []
	for i in range(length):
		genome_list.append(random.choice(choice))
	#print(genome_list)
	return ga.genom(genome_list, 0)

def select(ga, elite_length):
	# 現行世代個体集団の評価を高い順番にソートする
    sort_result = sorted(ga, reverse=True, key=lambda u: u.evaluation)
    # 一定の上位を抽出する
    result = [sort_result.pop(0) for i in range(elite_length)]
    return result

def crossover(ga_one, ga_two):
	#子孫を格納するリストを生成
	genom_list = []

	#入れ替える2点を設定
	cross_one = random.randint(0, GENOM_LENGTH)
	cross_two = random.randint(cross_one, GENOM_LENGTH)

	#遺伝子を取り出す
	one = ga_one.getGenom()
	two = ga_two.getGenom()

	#交叉させる
	progeny_one = one[:cross_one] + two[cross_one:cross_two] + one[cross_two:]
	progeny_two = two[:cross_one] + one[cross_one:cross_two] + two[cross_two:]

	#genomクラスのインスタンスを生成して子孫をリストに格納
	genom_list.append(ga.genom(progeny_one, 0))
	genom_list.append(ga.genom(progeny_two, 0))

	return genom_list

def next_generation_gene_create(ga, ga_elite, ga_progeny):
	#現行世代個体集団の評価を低い順にソートする
	next_generation_genom = sorted(ga, reverse=False, key=lambda u: u.evaluation)

	# 追加するエリート集団と子孫集団の合計ぶんを取り除く
	for i in range(0, len(ga_elite) + len(ga_progeny)):
		next_generation_genom.pop(0)

	#エリート集団と子孫集団を次世代へ追加
	next_generation_genom.extend(ga_elite)
	next_generation_genom.extend(ga_progeny)
	
	return next_generation_genom

def mutation(ga, individual_mutaion, genom_mutation):
	ga_list = []
	for i in ga:
		#個体に対して一定の確率で突然変異が起きる
		if individual_mutaion > (random.randint(0, 100) / Decimal(100)):
			genom_list = []
			for j in i.getGenom():
				#個体の遺伝子情報一つ一つに対して突然変異が起こる
				if genom_mutation > (random.randint(0, 100) / Decimal(100)):
					genom_list.append(random.choice(choice))
				else:
					genom_list.append(j)
			i.setGenom(genom_list)
			ga_list.append(i)
		else:
			ga_list.append(i)

	return ga_list

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

def battle(player):
	win = 0
	lose = 0
	draw = 0
	sazae = bot()
	for count in range(100):
		#1回目と2回目はランダムで手を出す
		if count < 2:
			player.result = random.choice(choice)
			sazae.result = random.choice(choice)
		#3回目以降は直前の2つの手によって条件分岐
		else:
			if sazae.prepreResult == 'G':
				if sazae.preResult == 'G':
					player.result = player.genom_list[0]
					sazae.result = choose(choice, probGG)
				if sazae.preResult == 'C':
					player.result = player.genom_list[1]
					sazae.result = choose(choice, probGC)
				if sazae.preResult == 'P':
					player.result = player.genom_list[2]
					sazae.result = choose(choice, probGP)

			if sazae.prepreResult == 'C':
				if sazae.preResult == 'G':
					player.result = player.genom_list[3]
					sazae.result = choose(choice, probCG)
				if sazae.preResult == 'C':
					player.result = player.genom_list[4]
					sazae.result = choose(choice, probCC)
				if sazae.preResult == 'P':
					player.result = player.genom_list[5]
					sazae.result = choose(choice, probCP)

			if sazae.prepreResult == 'P':
				if sazae.preResult == 'G':
					player.result = player.genom_list[6]
					sazae.result = choose(choice, probPG)
				if sazae.preResult == 'C':
					player.result = player.genom_list[7]
					sazae.result = choose(choice, probPC)
				if sazae.preResult == 'P':
					player.result = player.genom_list[8]
					sazae.result = choose(choice, probPP)

		if judge(player.result, sazae.result) == 1:
			win += 1
		elif judge(player.result, sazae.result) == 2:
			lose += 1
		else:
			draw += 1
		sazae.updateResult()

	eval = float(win) / (float)(win + lose + draw) * 100
	return eval

choice = ['G', 'C', 'P']

#probMN 2つ前がM,1つ前がNの時、サザエさんが次に[G,C,P]のそれぞれを出す確率
probGG = [7.52688172, 51.61290323, 40.86021505]
probGC = [23.42857143, 22.85714286, 53.71428571]
probGP = [17.8343949, 55.41401274, 26.75159236]

probCG = [21.54696133, 28.72928177, 49.72375691]
probCC = [42.85714286, 4.761904762, 52.38095238]
probCP = [47.89473684, 29.47368421, 22.63157895]

probPG = [31.12582781, 49.66887417, 19.20529801]
probPC = [53.06122449, 20.40816327, 26.53061224]
probPP = [37.07865169, 59.5505618, 3.370786517]

# 遺伝子情報の長さ
GENOM_LENGTH = 9
# 遺伝子集団の大きさ
MAX_GENOM_LIST = 300
# 遺伝子選択数
SELECT_GENOM = 15
# 個体突然変異確率
INDIVIDUAL_MUTATION = 0.1
# 遺伝子突然変異確率
GENOM_MUTATION = 0.1
# 繰り返す世代数
MAX_GENERATION = 50

if __name__ == '__main__':
	current_generation_individual_group = []
	graph_max = []
	graph_min = []
	graph_ave = []
	highest_max = 0

	for i in range(MAX_GENOM_LIST):
		current_generation_individual_group.append(create_genom(GENOM_LENGTH))

	for i in range(MAX_GENERATION):
		#遺伝子を評価し、評価値を代入
		for j in range(MAX_GENOM_LIST):
			evaluation_result = battle(current_generation_individual_group[j])
			current_generation_individual_group[j].setEvaluation(evaluation_result)
		#エリート個体を選択
		elite_genes = select(current_generation_individual_group, SELECT_GENOM)
		#エリート遺伝子を交叉させリストに格納
		progeny_gene = []
		for j in range(1, SELECT_GENOM):
			progeny_gene.extend(crossover(elite_genes[j-1], elite_genes[j]))
		#次世代個体集団を現行世代、エリート集団、子孫集団から作成
		next_generation_individual_group = next_generation_gene_create(current_generation_individual_group, elite_genes, progeny_gene)
		#次世代個体集団全ての個体に突然変異を施す
		next_generation_individual_group = mutation(next_generation_individual_group, INDIVIDUAL_MUTATION, GENOM_MUTATION)

		#1世代の進化計算終了。評価に移る。

		#各個体適用度を配列化
		fits = [j.getEvaluation() for j in current_generation_individual_group]

		#進化結果を評価
		min_ = min(fits)
		max_ = max(fits)
		ave_ = sum(fits) / len(fits)

		if max_ > highest_max:
			highest_max = max_

		#グラフ用に最大値を保存
		graph_max.append(max_)
		graph_min.append(min_)
		graph_ave.append(ave_)

		#現行世代の進化結果を出力
		print "-----第{}世代の結果-----".format(i+1)
		print "  Min: {}".format(min_)
		print "  Max: {}".format(max_)
		print "  Ave: {}".format(ave_)

		#現行世代と次世代を入れ替える
		current_generation_individual_group = next_generation_individual_group

	#最終結果の出力
	print "最も優れた個体は{}".format(elite_genes[0].getGenom())
	print "勝率の最高値は{}%". format(highest_max)

	#グラフを表示
	x = np.arange(MAX_GENERATION)
	y_max = np.array(graph_max)
	y_min = np.array(graph_min)
	y_ave = np.array(graph_ave)
	plt.plot(x, y_max, label='max')
	plt.plot(x, y_min, label='min')
	plt.plot(x, y_ave, label='ave')
	plt.legend()
	plt.grid()
	plt.ylim(0,100)
	plt.show()