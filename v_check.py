#!/usr/bin/env python
import sys
import json
import urllib
import urllib2
import os
import time

files = os.listdir('/opt/dionaea/var/dionaea/binaries/')

for hash_data in files:
	url = "https://www.virustotal.com/vtapi/v2/file/report"
	params = {"resource": hash_data, "apikey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

	data = urllib.urlencode(params)
	request = urllib2.Request(url, data)
	response = urllib2.urlopen(request)
	json = response.read()

	#スキャン結果をjsonで保存
	with open("/opt/dionaea/var/dionaea/vt/"+"{}.json".format(hash_data), "w") as result:
		result.write(json)

	print ("..processing")
	time.sleep(20) #APIの使用制限に当たらないように20秒待機させる
