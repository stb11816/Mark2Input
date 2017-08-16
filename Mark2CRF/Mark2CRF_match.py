#coding='utf-8'
#輸出crf格式
import glob,os,re,sys
import json
from pprint import pprint

def checkGlob(result,path):
	if len(result)==0:
		print('Please check path :'+path)
		sys.exit()

def match(article_paths,label_paths,output_path,mod,space=False): #若輸入space路徑可輸出斷行格式
	# article_paths=glob.glob(r'Data_db/(2-1)Data_ckip_articles/*.txt')
	json_paths=glob.glob(label_paths+r'*_label.json')
	checkGlob(json_paths,label_paths+r'*_label.json')

	if not os.path.exists(output_path):
		os.mkdir(output_path)
	if space != False:
		if not os.path.exists(space):
			os.mkdir(space)

	
	for path_l in json_paths:
		file_name=os.path.basename(path_l).replace('_label.json','')
		with open(path_l,'r',encoding='utf-8') as raw_l:
			label_dic=json.load(raw_l)

		with open(article_paths+file_name+'_ckip.txt','r',encoding='utf-8') as raw_ckip:
			articles=raw_ckip.readlines()
		
		output_content=[]
		for article in articles:
			board_name=article.split('\t')[0]
			aID=article.split('\t')[1]
			seq=article.split('\t')[2]
			article_seg=eval(article.split('\t')[3])
			article_pos=eval(article.split('\t')[4].replace('\n',''))
			labels=label_dic[aID]
			# print(len(''.join(article_seg)),len(labels))

			position=0
			article_content=''
			for seg,pos in zip(article_seg,article_pos):
				if len(seg)==1: #分詞結果比對label範圍
					term_range =[position]
					match_label=labels[term_range[0]]
				else:
					term_range =[position,position+len(seg)-1]
					match_label=labels[term_range[0]:term_range[1]+1]
				position+=len(seg)
				# if '0' not in match_label: #根據label範圍值判斷true or false
				# 	tf='true'
				# else:
				# 	tf='false'

				if mod=='bio':
					if match_label[0]=='B': #開頭為b
						tf='B'
					elif 'O' not in match_label and 'B' not in match_label: #皆為I
						tf='I'
					elif 'I' not in match_label and 'B' not in match_label: #皆為O
						tf='O'
					elif 'I' in match_label and 'O' in match_label: #有I也有O
						tf='I'
					elif 'B' in match_label and 'O' in match_label: #有I也有O
						tf='B'

				elif mod=='tf':
					if match_label[0]=='B': #開頭為b
						tf='true'
					elif 'O' not in match_label and 'B' not in match_label: #皆為I
						tf='true'
					elif 'I' not in match_label and 'B' not in match_label: #皆為O
						tf='false'
					elif 'I' in match_label and 'O' in match_label: #有I也有O
						tf='true'
					elif 'B' in match_label and 'O' in match_label: #有I也有O
						tf='true'
				# print(seg,match_label,tf)

				#輸出格式 PTT_mark M.1496853071.A.F2A 1 預算(Na) 預算 Na false
				content=' '.join([board_name,aID,seq,seg+'('+pos+')',pos,tf])+'\n'
				article_content+=content

				
			if output_content==[]:
				output_content.append(article_content)
			else:
				output_content.append('\n')
				output_content.append(article_content)
		# article loop end
		
		#預設輸出無斷航版
		with open(output_path+file_name+'_'+mod+'.data','w',encoding='utf-8') as out:
			for con in output_content:
				if con !='\n':
					out.write(con)

		if space != False: #是否輸出斷行版
			with open(space+file_name+'_'+mod+'.data','w',encoding='utf-8') as out_s:
				for con in output_content:
					out_s.write(con)

	print('Match finish')


def main():
	article_paths='D:/Term_Extraction/Mark2Input/Data_db/(2-1)Data_ckip_articles/'
	label_paths  ='D:/Term_Extraction/Mark2Input/Data_db/(1-2)Data_preprocess_label/'
	output_path  ='D:/Term_Extraction/Mark2Input/Data_db/(3-1)Data_match/'
	match(article_paths,label_paths,output_path,'bio')

if __name__ == '__main__':
	main()
