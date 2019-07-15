#!/usr/bin/python
#coding:utf-8
import sys
import math
import gzip

from paddle.v2.layer import parse_network
import paddle.v2 as paddle

__all__ = ["stacked_lstm_net"]


def stacked_lstm_net(input_dim,
                     class_dim=3,
                     emb_dim=128,
                     hid_dim=512,
                     stacked_num=5,
                     is_infer=False):
    """
    A Wrapper for sentiment classification task.
    This network uses bi-directional recurrent network,
    consisting three LSTM layers. This configure is referred to
    the paper as following url, but use fewer layrs.
        http://www.aclweb.org/anthology/P15-1109
    input_dim: here is word dictionary dimension.
    class_dim: number of categories.
    emb_dim: dimension of word embedding.
    hid_dim: dimension of hidden layer.
    stacked_num: number of stacked lstm-hidden layer.
    """
    assert stacked_num % 2 == 1

    fc_para_attr = paddle.attr.Param(learning_rate=1e-3)
    lstm_para_attr = paddle.attr.Param(initial_std=0., learning_rate=1.)
    para_attr = [fc_para_attr, lstm_para_attr]
    bias_attr = paddle.attr.Param(initial_std=0., l2_rate=0.)
    relu = paddle.activation.Relu()
    linear = paddle.activation.Linear()

    #文字输入层
    data = paddle.layer.data("word",
                             paddle.data_type.integer_value_sub_sequence(input_dim))
    #other数据输入层，包含是否有追评、追评间隔天数、是否好评、是否有图片
    #利用other与word分析结果构成最后的输出网络结果
    data1 = paddle.layer.data("other", paddle.data_type.dense_vector(4))
    #词向量层
    emb = paddle.layer.embedding(input=data, size=emb_dim)

    fc1 = paddle.layer.fc(
        input=emb, size=hid_dim, act=linear, bias_attr=bias_attr)
    lstm1 = paddle.layer.lstmemory(input=fc1, act=relu, bias_attr=bias_attr)

    inputs = [fc1, lstm1]
    for i in range(2, stacked_num + 1):
        fc = paddle.layer.fc(
            input=inputs,
            size=hid_dim,
            act=linear,
            param_attr=para_attr,
            bias_attr=bias_attr)
        lstm = paddle.layer.lstmemory(
            input=fc, reverse=(i % 2) == 0, act=relu, bias_attr=bias_attr)
        inputs = [fc, lstm]

    fc_last = paddle.layer.pooling(
        input=inputs[0], pooling_type=paddle.pooling.Max())
    lstm_last = paddle.layer.pooling(
        input=inputs[1], pooling_type=paddle.pooling.Max())
    output1 = paddle.layer.fc(
        input=[fc_last, lstm_last],
        size=4,
        act=linear,
        bias_attr=bias_attr,
        param_attr=para_attr)
    fc_other1 = paddle.layer.fc(input=data1, size=4, act=linear, bias_attr=bias_attr)
    fc_other2 = paddle.layer.fc(input=fc_other1, size=2, act=linear, bias_attr=bias_attr)
    output = paddle.layer.fc(
        input=[output1, fc_other2],
        size = class_dim,
        act =paddle.activation.Softmax(),
        bias_attr = bias_attr,
        param_attr = para_attr

        )

    #标签输入层
    if not is_infer:
        lbl = paddle.layer.data("label", paddle.data_type.integer_value(2))
        cost = paddle.layer.classification_cost(input=output, label=lbl)
    
    #误差
    if is_infer:
        return output
    else:
        return cost, output
    
