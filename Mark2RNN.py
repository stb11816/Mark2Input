#coding='utf-8'
from datetime import datetime
from pprint import pprint
import glob,json,os,re,sys,copy

def checkGlob(result,path):
	if len(result)==0:
		print('Please check path :'+path)
		sys.exit()

def textIdfChiEngReturnList(text):
	charList=[]
	eng=''
	mark_s=''
	mark_e=''
	for i in range(0,len(text)):
		currentChr=text[i:i+1] 
		# pat=re.compile(r'＜／?＊.+?＊＞')
		other =re.match('[0-9a-zA-Z.,%]', currentChr)
		tag_s =re.match(r'[＜,＊,／]',currentChr)
		tag_e =re.match(r'[＊,＞]',currentChr)
		if other != None: #等於數字或英文
			eng=eng+currentChr
		elif text[i:i+1]=='＊' and text[i+1:i+2]=='＞':
			pass
		elif text[i:i+1]=='＞' and text[i-1:i]=='＊':
			charList.append('＊＞')
		elif tag_s != None:
			mark_s+=currentChr
		else:
			if eng!='':
				charList.append(eng)
				eng=''
				
			if mark_s !='':
				charList.append(mark_s)
				mark_s=''

			if currentChr != ' ':    
				chi=text[i:i+1]
				charList.append(chi)
	return charList


def RNNOuntput(allSource,date_range,raw_dir,output_dir):
	concept_dic = {'商品種類':'1','品牌':'2','型號':'3','規格':'4','規格(硬體)':'4','描述':'5','描述(描述規格)':'5','評論':'6','評論!':'6','功能':'7','功能(用途)':'7','功能(可以做到什麼)':'7','衍生商品':'8','解決方案':'9','金額':'10','正面':'11'}
	print('source :'+str(allSource))
	print('date range :'+str(date_range))
	if len(date_range[0].split('-')) != len(date_range[1].split('-')):
		print('Datetime format error')
		sys.exit()

	if len(date_range[0].split('-'))==2:
		s_date=datetime.strptime(date_range[0],'%Y-%m')
		e_date=datetime.strptime(date_range[1],'%Y-%m')
	elif len(date_range[0].split('-'))==3:
		s_date=datetime.strptime(date_range[0],'%Y-%m-%d')
		e_date=datetime.strptime(date_range[1],'%Y-%m-%d')
	# print('range :',s_date,e_date)
	
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	

	for source in allSource:
		file_paths=glob.glob(r''+raw_dir+source+r'/*/*.json')
		checkGlob(file_paths,r''+raw_dir+source+r'/*/*.json')
		for file_path in file_paths: #某來源下所有檔案
			# print('processing file :',os.path.basename(file_path))
			with open(file_path,'r',encoding='utf-8') as raw:
				mark_content=json.load(raw)

			output_dic={
				'Board_name':mark_content['Board_name'],
				'Source_name':mark_content['Source_name'],
				'Source_type':mark_content['Source_type'],
				'Date_range':[date_range[0],date_range[1]],
				'Articles':{}
			}
			for aID in mark_content['Articles']:
				article_date=datetime.strptime(mark_content['Articles'][aID]['Date'],'%Y-%m-%d')
				article_board  =mark_content['Board_name']
				article_title  =mark_content['Articles'][aID]['Title']
				article_seeds  =mark_content['Articles'][aID]['Summary']
				article_content=mark_content['Articles'][aID]['Mark']
				article_content=article_content.replace('／／ｎ','')
				article_content=textIdfChiEngReturnList(article_content)


				raw_sentence=[]
				label=[]
				concept=False
				term_1=False
				term_2=False
				concept_name=''
				for idx in range(len(article_content)):
					if article_content[idx]=='＜＊' or article_content[idx]=='＜／＊':
						concept=True
					elif article_content[idx-1] =='＊＞':
						concept=False

					if not concept:
						raw_sentence.append(article_content[idx])  #去除tag 還原成原始格式

					if article_content[idx]=='＜＊':
						term_1=True
					elif article_content[idx]=='＊＞' and term_1:
						term_2=True
					elif article_content[idx]=='＜／＊':
						term_1=False
					elif article_content[idx]=='＊＞' and term_2:
						term_2=False
						concept_name=''

					if term_1 and not term_2:
						if article_content[idx]!='＜＊':
							concept_name+=article_content[idx] #判斷concept name

					if term_1 and term_2:
						if article_content[idx]!='＊＞':
							concept_num=concept_dic[concept_name]
							label.append(str(concept_num)) #添加concept數字
					elif not concept:
						label.append('0')

				if s_date<=article_date<=e_date: #文章日期是否在範圍內
					output_dic['Articles'].update({str(aID):{'sentence':raw_sentence,'label':label}})
					

			if output_dic != {}:
				output_file_name='_'.join([date_range[0],date_range[1]])
				output_file_name=output_dir+source+'('+mark_content['Board_name']+')_'+output_file_name

				#輸出完整label檔
				with open(output_file_name+'_allLabel.json','w',encoding='utf-8') as out:
					json.dump(output_dic,out,indent=2,ensure_ascii=False)

				#輸出單一label檔
				for c in range(1,12):
					# copy_dic=copy.copy(output_dic)
					c_id=str(c)
					singleLabel_dic={
						'Board_name':output_dic['Board_name'],
						'Source_name':output_dic['Source_name'],
						'Source_type':output_dic['Source_type'],
						'Date_range':[date_range[0],date_range[1]],
						'Articles':{}
					}

					for aID in output_dic['Articles']:
						article_label=output_dic['Articles'][aID]['label']
						single_label=[]
						get_label=False
						for idx in range(len(article_label)):
							if article_label[idx]!=c_id:
								single_label.append('0')
							elif article_label[idx]==c_id:
								single_label.append(c_id)
								get_label=True

						if get_label: #如果有比對到label才輸出
							singleLabel_dic['Articles'].update({aID:{'sentence':output_dic['Articles'][aID]['sentence'],'label':single_label}})
					
						# print(aID,c_id,output_dic['Articles'][aID]['label'],len(output_dic['Articles'][aID]['label']))
						# print(aID,c_id,single_label,len(single_label))
						# print('-'*50)
						
					if len(singleLabel_dic['Articles'].keys())!=0: #有文章才輸出
						with open(output_file_name+'_label'+c_id+'.json','w',encoding='utf-8') as out:
							json.dump(singleLabel_dic,out,indent=2,ensure_ascii=False)


def main():
	source=['ptt','mobile01']
	date_range=['2015-12','2017-07']
	raw_dir='./Data_db/(0)Data_mark/'
	output_dir='./Data_db/Data_RNN/'
	RNNOuntput(source,date_range,raw_dir,output_dir)


if __name__ == '__main__':
	main()

