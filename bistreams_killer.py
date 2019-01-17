#!/usr/bin/env python
import sys
import os

bistreams_path = '/opt/dionaea/var/dionaea/bistreams/'
files = os.listdir(bistreams_path) #bistreams内のファイル一覧を取得
files_dir = [f for f in files if os.path.isdir(os.path.join(bistreams_path, f))] #名前が日付になっているディレクトリの存在確認をしてリストに格納
files_dir.sort() #昇順ソート

day_path = bistreams_path + files_dir[-1] + '/' #一番新しい日付のpathを作成
day_files = os.listdir(day_path) #一番新しい日付のディレクトリのファイル一覧を取得

for day_file in day_files: #全ファイルを処理
	if os.path.getsize(day_path+day_file) == 0: #ファイルサイズが0のときは次のファイルへ
		continue
	f=open(day_path+day_file, 'w') #書き込みモードで開いて中身を空にする
	f.close()
