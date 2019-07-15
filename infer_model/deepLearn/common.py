#!/usr/bin/python
#coding:utf-8
import jieba
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

def load_word_dict(dict_path):
    word_dict = {}
    with open(dict_path,'r') as f:
        for line in f:
            line_split = line.strip().split("\t")
            word_dict[line_split[0]] = int(line_split[1])
    return word_dict