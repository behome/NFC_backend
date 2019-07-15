# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
import json
from deepLearn.common import load_word_dict
from deepLearn.paddle_init import paddlev2_init
from deepLearn.infer import get_predict
from deepLearn.infer import get_Sum_by_preRead
from deepLearn.reader import test_reader
from deepLearn.reader import pre_reader
from . import comm_function
word_dict = load_word_dict("/var/www/html/NFC_v1.1/infer_model/deepLearn/dict/word_dict.txt")
inferer = paddlev2_init()
# Create your views here.
@csrf_exempt
def index(request):
	websiteId = request.POST.get('websiteId')
	#print websiteId
	itemId = request.POST.get('itemId')
	#print itemId
	sellerId = request.POST.get('sellerId')
	summ = 0
	if websiteId == '1':
		comments = comm_function.getPreReadTaoBaoData(itemId, sellerId)
		#print comments
		batch = pre_reader(comments, word_dict)
		#print batch
		summ = get_Sum_by_preRead(inferer, batch)
	return_json = {'result':summ}
	return HttpResponse(json.dumps(return_json), content_type='application/json')

@csrf_exempt
def comAnaly(request):
	comments = json.loads(request.POST.get('comments'))
	#print comments
	indexs, batch = test_reader(comments, word_dict)
	result = get_predict(inferer, batch, indexs)
	return HttpResponse(json.dumps(result), content_type='application/json')




