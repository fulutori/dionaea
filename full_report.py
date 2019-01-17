#coding: utf-8
import os
import sys

csv_dir = './detail/'
csv_list = sorted(os.listdir(csv_dir))

ip_list = {} #IPアドレスごとの攻撃回数をカウント
port_list = {} #ポートごとの攻撃回数をカウント
country_list = {} #国ごとの攻撃回数をカウント
country_list_detail = {} #国ごとの攻撃詳細
csv_file_all = [] #1か月分の攻撃データを格納

"""
データ形式

月,日,時刻,ポート,ポート番号,IPアドレス,国
Sep,1,00:04,smbd,445,185.81.99.137,Iran
Sep,1,00:04,smbd,445,185.81.99.137,Iran

"""
print('csvファイル読み込み開始')
for csv_file in csv_list:
	with open(csv_dir+csv_file,'r') as f:
		data = f.read().split('\n')
		if data[-1] == "":
			data.pop()
		for i in range(len(data)):
			data[i] = data[i].split(',')
	csv_file_all.append(data)
print('csvファイル読み込み完了\n')

print('データ処理開始')


#day:一日分のデータ
#line:攻撃ごとのデータ
for day in csv_file_all:
	for line in day:
		#ポートの情報を処理
		if line[3]+'('+line[4]+')' in port_list:
			port_list[line[3]+'('+line[4]+')'] += 1
		else:
			port_list[line[3]+'('+line[4]+')'] = 1

		#IPアドレスの情報を処理
		if line[5]+'('+line[6]+')' in ip_list:
			ip_list[line[5]+'('+line[6]+')'] += 1
		else:
			ip_list[line[5]+'('+line[6]+')'] = 1

		#国情報を処理
		if line[6] in country_list:
			country_list[line[6]] += 1
		else:
			country_list[line[6]] = 1

		#国情報の詳細を取得
		if line[6] in country_list_detail:
			#port
			if line[3] in country_list_detail[line[6]]:
				country_list_detail[line[6]][line[3]] += 1
			else:
				country_list_detail[line[6]][line[3]] = 1
			#ip
			#if line[5] in country_list_detail[line[5]]:
			#	country_list_detail[line[6]][line[5]] += 1
			#else:
			#	country_list_detail[line[6]][line[5]] = 1
		else:
			country_list_detail[line[6]] = {}
			country_list_detail[line[6]][line[3]] = 1

print('データ処理終了\n')

print('データ保存開始')

#ポートごとの攻撃情報をファイルに書き出す
f = open('./port_list.csv','a')
for k, v in sorted(port_list.items(), key=lambda x: -x[1]):
	f.write(str(k)+','+str(v)+'\n')
f.close()

#IPアドレスごとの攻撃回数をファイルに書き出す
f = open('./ip_list.csv','a')
for k, v in sorted(ip_list.items(), key=lambda x: -x[1]):
	f.write(str(k)+','+str(v)+'\n')
f.close()

#国ごとの攻撃回数をファイルに書き出す
country_name = [] #国名を格納
f = open('./country_list.csv','a')
for k, v in sorted(country_list.items(), key=lambda x: -x[1]):
	country_name.append(str(k))
	f.write(str(k)+','+str(v)+'\n')
f.close()

#for k, v in sorted(country_list_detail.items(), key=lambda x: -x[1]):
#	print(str(k) + ": "+str(v))
#print(country_list_detail)

#国ごとの攻撃回数(ポート別)をファイルに書き出す
f = open('./country_list_detail.txt','a')
f.write('------------------------------------\n')
f.write('Total Country: '+str(len(country_list_detail))+'\n')
for country_dict in country_name:
	country_list_detail[country_dict] = sorted(country_list_detail[country_dict].items(), key=lambda x: -x[1])
	f.write('------------------------------------\n')
	f.write(country_dict+'  total: '+str(country_list[country_dict])+'\n')
	for k, v in country_list_detail[country_dict]:
		f.write(str(k) + ": "+str(v)+'\n')
f.close()
#print(country_list_detail)

print('データ保存終了\n')


print('malwareリスト作成開始')
try:
	malware_dict = {}

	#1か月分のマルウェアの検知情報を処理
	with open('malware_list.csv','r') as f:
		data = f.read().split('\n')
		if data[-1] == "": #データの末尾に何もないときは削除
			data.pop()
		for i in range(len(data)): #データを「,」で区切る
			data[i] = data[i].split(',')
	for mal in data:
		if mal[0] in malware_dict:
			malware_dict[mal[0]] += int(mal[1])
		else:
			malware_dict[mal[0]] = int(mal[1])

	#マルウェアの検知回数をファイルに書き出す
	f = open('./malware.csv','a')
	for k, v in sorted(malware_dict.items(), key=lambda x: -x[1]):
		f.write(str(k)+','+str(v)+'\n')
	f.close()
	print('malwareリスト作成完了\n')

except:
	print('malwareリストの作成に失敗しました\n')
print('全ての工程が完了しました')
