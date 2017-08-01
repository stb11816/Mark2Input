#coding='utf-8'
from datetime import datetime
from pprint import pprint
import glob,json,os,re

# def saveSeed()


def main(allSource,date_range,raw_dir,output_dir):
	s_date=datetime.strptime(date_range[0],'%Y-%m')
	e_date=datetime.strptime(date_range[1],'%Y-%m')
	print('range :',s_date,e_date)

	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	if not os.path.exists('Data_db/Seeds/'):
		os.mkdir('Data_db/Seeds/')

	for source in allSource:
		file_paths=glob.glob(r''+raw_dir+source+r'/*/*.json')
		for file_path in file_paths:
			with open(file_path,'r',encoding='utf-8') as raw:
				mark_content=json.load(raw)
			print(file_path)
			output_content=''
			for aID in mark_content['Articles']:
				article_date=datetime.strptime(mark_content['Articles'][aID]['Date'],'%Y-%m-%d')
				article_board  =mark_content['Board_name']
				article_title  =mark_content['Articles'][aID]['Title']
				article_seeds  =mark_content['Articles'][aID]['Summary']
				article_content=mark_content['Articles'][aID]['Mark']
				article_content=article_content.replace('／／ｎ','')
				pat=re.compile(r'＜／?＊.+?＊＞')
				result=pat.findall(article_content)
				for r in result:
					print(r)
					article_content=article_content.replace(r,'')
				# pprint(article_seeds)

				if s_date<=article_date<=e_date:
					print(article_date)
					output_content+=article_board+'\t'+str(aID)+'\t'+article_title+'\n'
					output_content+=article_board+'\t'+str(aID)+'\t'+article_content+'\n'
			
				seeds_output=''
				for seed in article_seeds:
					seeds_output+=seed+'\n'
				with open('Data_db/Seeds/'+aID+'.txt','w',encoding='utf-8') as out_s:
					out_s.write(seeds_output)

			# print(output_content)
			if output_content != '':
				output_file_name='_'.join([date_range[0],date_range[1]])
				with open(out_dir+source+'('+mark_content['Board_name']+')_'+output_file_name+'.txt','w',encoding='utf-8') as out:
					out.write(output_content)			



if __name__ == '__main__':
	source=['ptt','mobile01']
	date_range=['2015-12','2017-07']
	raw_dir='./Data_db/Data_mark/'
	out_dir='Data_db/Data_preprocess/'
	main(source, date_range, raw_dir, out_dir)

