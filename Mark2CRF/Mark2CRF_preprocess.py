#coding='utf-8'
#將標記結果輸出三個檔案：原始文章、seed、原始文章的label陣列
from datetime import datetime,date
from pprint import pprint
import glob,json,os,re,sys
# import date

def checkGlob(result,path):
	if len(result)==0:
		print('Please check path :'+path)
		sys.exit()


def main(allSource,date_range,raw_dir,output_dir,out_dir_seed,out_dir_label):
	# print('Preprocess start')
	if len(date_range[0].split('-')) != len(date_range[1].split('-')):
		print('Datetime format error')
		sys.exit()

	if len(date_range[0].split('-'))==2 and len(date_range[1].split('-'))==2:
		DATETIME_FORMAT = "%Y-%m"
	elif len(date_range[0].split('-'))==3 and len(date_range[1].split('-'))==3:
		DATETIME_FORMAT = "%Y-%m-%d"
	s_date=datetime.strptime(date_range[0],DATETIME_FORMAT)
	e_date=datetime.strptime(date_range[1],DATETIME_FORMAT)

	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	if not os.path.exists(out_dir_seed):
		os.mkdir(out_dir_seed)
	if not os.path.exists(out_dir_label):
		os.mkdir(out_dir_label)
	if not os.path.exists(out_dir_seed+'/seed_integrate.json'):
		seed_dic={}
	else:
		with open(out_dir_seed+'/seed_integrate.json','r',encoding='utf-8') as raw:
			seed_dic=json.load(raw)


	for source in allSource:
		file_paths=glob.glob(r''+raw_dir+source+r'/*/*.json')
		checkGlob(file_paths,r''+raw_dir+source+r'/*/*.json')

		for file_path in file_paths:
			with open(file_path,'r',encoding='utf-8') as raw:
				mark_content=json.load(raw)
			
			output_content=''
			output_seed ={}
			output_label={}
			for aID in mark_content['Articles']:
				article_date=datetime.strptime(mark_content['Articles'][aID]['Date'],'%Y-%m-%d')
				article_board  =mark_content['Board_name']
				article_title  =mark_content['Articles'][aID]['Title']
				article_seeds  =mark_content['Articles'][aID]['Summary']
				article_content=mark_content['Articles'][aID]['Mark']
				article_content=article_content.replace('／／ｎ',' ').replace('\t',' ')#換行用空格代替
				
				if s_date<=article_date<=e_date: #在篩選日期範圍內
					article_label=[]
					label_position={}
					gogo=True
					while gogo:
						pat=re.compile(r'＜＊\w*＊＞(.+?)＜／＊\w*＊＞')
						result=pat.search(article_content)
						if result !=None:
							term=result.group()
							position=result.span()[0]
							word=term.split('＜／＊')[0].split('＊＞')[1]
							concept=term.split('＜＊')[1].split('＊＞')[0]
							article_content=article_content.replace(term,word,1)
							# print(word,concept,position)
							# status=[concept,'type','2017-08-15','mark']
							# if word not in 

							for p in range(position,len(word)+position):
								# label_position.update({str(p):'1'}) #被標記部分為1
								if p==position:
									label_position.update({str(p):'B'})
								else:
									label_position.update({str(p):'I'})
						else:
							gogo=False

					for idx in range(len(article_content)): #產生label
						if article_content[idx]==' ': #忽略空格
							pass
							# article_label.append('O')
						elif str(idx) in label_position:
							# article_label.append('1')
							article_label.append(label_position[str(idx)])
						else:
							# article_label.append('0')
							article_label.append('O')
					output_label.update({str(aID):article_label})
					

					output_seed.update({str(aID):[]})
					for seed in article_seeds: #文章中出現的seed
						output_seed[aID].append(seed)

						for concept in article_seeds[seed]['concept']:
							date_str=(date.today()).strftime('%Y-%m-%d')
							status=[concept,'type',date_str,'mark']
							print(status)
							if seed not in seed_dic:
								seed_dic.update({seed:[status]})
							else:
								if status not in seed_dic[seed]:
									seed_dic[seed].append(status)
						# seed_dic.update({seed:[]}) #更新至整合檔

					# output_content+=article_board+'\t'+str(aID)+'\t'+article_title+'\n'
					output_content+=article_board+'\t'+str(aID)+'\t'+article_content+'\n'
					

			output_file_name='_'.join([date_range[0],date_range[1]])
			if output_content != '': #輸出原文 包含空格
				with open(output_dir+source+'('+mark_content['Board_name']+')_'+output_file_name+'.txt','w',encoding='utf-8') as out:
					out.write(output_content)

			if output_seed != {}: #輸出文章的seed
				with open(out_dir_seed+source+'('+mark_content['Board_name']+')_'+output_file_name+'_seed.json','w',encoding='utf-8') as out_j:
					json.dump(output_seed,out_j,indent=2,ensure_ascii=False)
				with open(out_dir_seed+'/seed_integrate.json','w',encoding='utf-8') as out_i:
					json.dump(seed_dic,out_i,indent=2,ensure_ascii=False)

			if output_label != {}: #輸出文章的label，不含空格
				with open(out_dir_label+source+'('+mark_content['Board_name']+')_'+output_file_name+'_label.json','w',encoding='utf-8') as out_l:
					json.dump(output_label,out_l,indent=2,ensure_ascii=False)
	print('Preprocess finish')


if __name__ == '__main__':
	source=['ptt','mobile01']
	date_range=['2015-12','2017-07']
	raw_dir='D:/Term_Extraction/Mark2Input/Data_db/(0)Data_mark/'
	out_dir='D:/Term_Extraction/Mark2Input/Data_db/(1-1)Data_preprocess_raw/'
	out_dir_label='D:/Term_Extraction/Mark2Input/Data_db/(1-2)Data_preprocess_label/'
	out_dir_seed ='D:/Term_Extraction/Mark2Input/Data_db/(1-3)Seeds/'
	main(source, date_range, raw_dir, out_dir, out_dir_seed, out_dir_label)

