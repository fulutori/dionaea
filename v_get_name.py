#!/usr/bin/env python
import sys
import json
import os
import requests

vt_path = '/opt/dionaea/var/dionaea/vt/'
files = os.listdir(vt_path)
company = ['Symantec','TrendMicro','Kaspersky','Microsoft','McAfee']

for vt_result in files:
	f = open(vt_path + vt_result, 'r')
	json_dict = json.load(f)
	if json_dict['response_code'] == 1: #処理続行
		pass
	else: #vtの結果が無いときは次のファイルへ
		print(vt_result + ' -> failue')
		f.close()
		continue

	scan_result = json_dict['scans'] #スキャン結果を取得
	for company_name in company:
		if company_name in scan_result:
			company_result = scan_result[company_name]
			break

	v_name = json.dumps(company_result['result']) #ウィルス名を取得
	print(vt_result+' -> '+v_name+' / '+company_name)
	f.close()
