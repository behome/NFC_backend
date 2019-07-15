#!/usr/bin/python
#coding:utf-8
import jieba
import sys, os
import paddle.v2 as paddle
reload(sys)
sys.setdefaultencoding('utf-8')

def pre_reader(comments, word_dict):
    batch=[]
    for comment in comments:
        doc = comment['comment']
        doc_ids = []
        for sent in doc.strip().split('。'):
            sent_ids = [
            word_dict.get(w.encode('utf-8'), 2000)
            for w in jieba.lcut(sent, cut_all=False)]
            if sent_ids:
                doc_ids.append(sent_ids)
        others = [int(comment['haveappend']), int(comment['appendDays']), int(comment['rate']), int(comment['havePic'])]
        batch.append([doc_ids, others])
    return batch

def test_reader(comments, word_dict):
    indexs=[]
    batch=[]
    for comment in comments:
        indexs.append(comment['index'])
        doc = comment['comment']
        doc_ids = []
        for sent in doc.strip().split('。'):
            sent_ids = [
            word_dict.get(w.encode('utf-8'), 2000)
            for w in jieba.lcut(sent, cut_all=False)]
            if sent_ids:
                doc_ids.append(sent_ids)
        others = [int(comment['haveappend']), int(comment['appendDays']), int(comment['rate']), int(comment['havePic'])]
        batch.append([doc_ids, others])
    return indexs, batch

def train_reader(data_dir, word_dict):
    

    def reader():
        for file_name in os.listdir(data_dir):
            file_path = os.path.join(data_dir, file_name)
            if not os.path.isfile(file_path):
                continue
            with open(file_path, "r") as f:
                for line in f:
                    line_split = line.strip().split("\t")
                    doc = line_split[1]
                    doc_ids = []
                    for sent in doc.strip().split('。'):
                        sent_ids = [
                        word_dict.get(w.encode('utf-8'), 2000)
                        for w in jieba.lcut(sent, cut_all=False)]
                        if sent_ids:
                            doc_ids.append(sent_ids)
                    others = [int(line_split[2]), int(line_split[3]), int(line_split[4]), int(line_split[5])]

                    yield doc_ids, others, int(line_split[0])
    return reader
