# -*- coding: utf-8 -*-

#サザエさんのじゃんけんのパターンを学習するプログラム
#サザエさん→前2回の手によって確率で分岐して手を出す
#出す手をランダムで生成し、評価関数によって進化する
#1世代につき100回くらい勝負して、勝率がn割以上の遺伝子を選ぶ？

import numpy as numpy
import matplotlib.pyplot as pyplot
import random

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