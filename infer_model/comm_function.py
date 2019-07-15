# -*- coding: utf-8 -*-
import json
import urllib2
import urllib
import re


def getJson(url):
	result = urllib2.urlopen(url).read()
	#result = result.strip('(')
	#result = result.strip(')')
	matchObj = re.search(r'\(({[\s\S]*})\)',result,re.M|re.I)
	result_json = json.loads(matchObj.group(1))
	return result_json

def praserJsonData(data):
	rootlist = data.keys()
	
def getPreReadTaoBaoData(itemId, sellerId):
	comments = []
	prefix = "https://rate.taobao.com/feedRateList.htm?auctionNumId=" + itemId + "&userNumId=" + sellerId
	for a in range(1, 6):
		url = prefix + "&siteID=&currentPageNum="+ str(a) + "&pageSize=20&rateType=1&orderType=sort_weight&showContent=1&attribute=&folded=0&ua="
		print url
		result_json = getJson(url)
		if result_json['comments']:
			for comment in result_json['comments']:
				item = {}
				item['comment'] = comment['content']
				if comment['append']:
					item['haveappend'] = 1
					item['appendDays'] = comment['appendList'][0]['dayAfterConfirm']
				else:
					item['haveappend'] = 0
					item['appendDays'] = 0;
				item['rate'] = 1
				if comment['photos']:
					item['havePic'] = 1
				else:
					item['havePic'] = 0
				comments.append(item)
		
	for a in range(1,5):
		url = prefix + "&siteID=&currentPageNum="+ str(a) + "&pageSize=20&rateType=0&orderType=sort_weight&showContent=1&attribute=&folded=0&ua="
		result_json = getJson(url)
		if result_json['comments']:
			for comment in result_json['comments']:
				item = {}
				item['comment'] = comment['content']
				if comment['append']:
					item['haveappend'] = 1
					item['appendDays'] = comment['appendList'][0]['dayAfterConfirm']
				else:
					item['haveappend'] = 0
					item['appendDays'] = 0;
				item['rate'] = 0
				if comment['photos']:
					item['havePic'] = 1
				else:
					item['havePic'] = 0
				comments.append(item)
	for a in range(1,4):
		url = prefix + "&siteID=&currentPageNum="+ str(a) + "&pageSize=20&rateType=0&orderType=sort_weight&showContent=1&attribute=&folded=0&ua="
		result_json = getJson(url)
		if result_json['comments']:
			for comment in result_json['comments']:
				item = {}
				item['comment'] = comment['content']
				if comment['append']:
					item['haveappend'] = 1
					item['appendDays'] = comment['appendList'][0]['dayAfterConfirm']
				else:
					item['haveappend'] = 0
					item['appendDays'] = 0;
				item['rate'] = 0
				if comment['photos']:
					item['havePic'] = 1
				else:
					item['havePic'] = 0
				comments.append(item)
	return comments


