#!/usr/bin/python
#coding:utf-8
import sys
import os

from common import load_word_dict
from net_config import stacked_lstm_net
import paddle.v2 as paddle
reload(sys)
sys.setdefaultencoding('utf-8')
with_gpu = os.getenv('WITH_GPU', '0') != '0'

def paddlev2_init():
	word_dict = load_word_dict("/var/www/html/NFC_v1.1/infer_model/deepLearn/dict/word_dict.txt")
	dict_dim = len(word_dict)
	prob_layer = stacked_lstm_net(dict_dim, stacked_num=5, class_dim = 3, is_infer=True)
	paddle.init(use_gpu = with_gpu, trainer_count=1)

	parameters = paddle.parameters.Parameters.from_tar(
		open("/var/www/html/NFC_v1.1/infer_model/deepLearn/model/params_pass_35.tar","r"))
	inferer = paddle.inference.Inference(
		output_layer=prob_layer, parameters=parameters)
	return inferer
