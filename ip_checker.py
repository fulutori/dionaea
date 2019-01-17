#!/usr/bin/python
#coding: utf-8
#import os
import sys
import geoip2.database
import datetime

f = open('bis_2018-08-26','r')
files = f.readlines()
f.close()

reader = geoip2.database.Reader('/usr/local/share/GeoIP/GeoLite2-Country.mmdb')

data = []
attack_dict = {} #攻撃に使用されたIPアドレスの検知回数を格納
country_dict = {} #IPアドレスに紐づけられている国の検知回数を格納
for f in files:
	f = f.split(',')
	month = f[5] #月
	day = f[6] #日
	time = f[7] #時刻
	file_name = f[8].replace('\n','').split('-')
	port_name = file_name[0] #ポート名
	port_number = file_name[1] #ポート番号
	ip = file_name[2] #IPアドレス
	record = reader.country(ip) #IPアドレスに紐づけられているデータを取得
	country = record.country.name #国名を抽出
	if port_name in attack_dict:
		attack_dict[port_name] += 1
	else:
		attack_dict[port_name] = 1
	if country in country_dict:
		country_dict[country] += 1
	else:
		country_dict[country] = 1
	data.append(month+','+day+','+time+','+port_name+','+port_number+','+ip+','+country+'\n')

#1日分の攻撃情報をファイルに書き出す
now = datetime.datetime.now()
f_name = 'report_{0:%Y%m%d}'.format(now)
print (f_name)
with open(f_name,'a') as f:
	f.write('[Number of attacks on port]\n')
	for k, v in sorted(attack_dict.items(), key=lambda x: -x[1]):
		f.write(str(k) + ': ' + str(v)+'\n')
	f.write('\n[Number of access by country]\n')
	for k, v in sorted(country_dict.items(), key=lambda x: -x[1]):
		f.write(str(k) + ': ' + str(v)+'\n')
	f.write('\n[detail]\n')
	for i in data:
		f.write(i)
	f.close()
