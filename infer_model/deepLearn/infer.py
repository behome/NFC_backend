#!/usr/bin/python
#coding:utf-8
import sys
import os
import gzip

import paddle.v2 as paddle
import gzip
import reader
from net_config import stacked_lstm_net
from common import load_word_dict

#恢复网络拓扑
def re_topology(dict_dim, class_dim, model_path):
    prob_layer = stacked_lstm_net(input_dim = dict_dim, is_infer = True)
    # load the trained models
    parameters = paddle.parameters.Parameters.from_tar(
        open(model_path, "r"))
    inferer = paddle.inference.Inference(
        output_layer=prob_layer, parameters=parameters)
    return inferer
#取得预测结果
def get_predict(inferer, batch, indexs):
    final_result={}
    result = inferer.infer(input = batch, field=["value"])
    assert len(result) == len(batch)
    for index, prob in zip(indexs, result):
        final_result[index] = prob.argmax()
    return final_result

def get_Sum_by_preRead(inferer, batch):
    good = 0
    result = inferer.infer(input = batch, field=['value'])
    assert len(result) == len(batch)
    for prob in result:
        if prob.argmax() == 2:
            good = good+1
    return good*100/len(batch)
