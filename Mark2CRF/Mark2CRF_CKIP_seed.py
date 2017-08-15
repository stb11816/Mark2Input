#coding='utf-8'
#讀取seed，進行傳至ckip
import glob,os,json,sys
from ckip import CKIPSegmenter

def checkGlob(result,path):
	if len(result)==0:
		print('Please check path :'+path)
		sys.exit()

def to_ckip(inp):
	segmenter = CKIPSegmenter('Bolin', 'Bolin') #ckip連線帳戶
	try:
		result = segmenter.process(inp) #斷詞結果
		if result['status_code'] != '0': #若斷詞失敗
			print('Process Failure: ' + result['status'])
		SaveList=[]
		SaveSeg=[]
		sen_all=[]
		for sentence in result['result']:
			for term in sentence:
				SaveList.append(term['term']) #詞陣列
				SaveSeg.append(term['pos']) #詞性陣列
		for word,pos in zip(SaveList,SaveSeg):
			wp=word+'('+pos+')'
			sen_all.append(wp)
		combine=' '.join(sen_all)

		return [SaveList,SaveSeg,combine]
	except:
		print('error :',inp)
		return False

def process_Seeds(input_path, output_path):
	# print('Seed2CKIP start')
	seed_path=glob.glob(input_path+r'*_seed.json')
	checkGlob(seed_path,input_path+r'*_seed.json')

	if not os.path.exists(output_path):
		os.mkdir(output_path)
	if not os.path.exists(input_path+'/seed_integrate.json'):
		print(input_path+'/seed_integrate.json not exists')
		seed_dic={}
	else:
		with open(input_path+'/seed_integrate.json','r',encoding='utf-8') as raw_i:
			seed_dic=json.load(raw_i)
	
	if not os.path.exists(output_path+'/seed_integrate_ckip.json'):
		print(output_path+'/seed_integrate_ckip.json not exists')
		seed_dic_ckip={}
	else:
		with open(output_path+'/seed_integrate_ckip.json','r',encoding='utf-8') as raw_c:
			seed_dic_ckip=json.load(raw_c)

	
	for spath in seed_path: #所有文章的seed黨
		with open(spath,'r',encoding='utf-8') as raw:
			contents=json.load(raw)
		
		output_content={}
		for aID in contents:
			output_content.update({str(aID):[]})
			for seed in contents[aID]: #某文章的所有seed
				result=to_ckip(seed)
				output_content[aID].append(result[2])
				
				if seed not in seed_dic:
					seed_dic_ckip.update({result[2]:[]})
				else:

					seed_dic_ckip.update({result[2]:seed_dic[seed]})
				# if seed_dic=={}:
				# 	seed_dic.update({seed:{result}})
				# elif seed in :
				# 	seed_dic.update({seed:result})
					# seed_dic.update({str(result[2]).replace(' ',''):[]})
					

		output_name=os.path.basename(spath).replace('.json','')+'_ckip'
		with open(output_path+output_name+'.json','w',encoding='utf-8') as out:
			json.dump(output_content,out,indent=2,ensure_ascii=False)
		with open(output_path+'seed_integrate_ckip.json','w',encoding='utf-8') as out_i:
			json.dump(seed_dic_ckip,out_i,indent=2,ensure_ascii=False)
	print('Seed2CKIP finish')

def main():
	input_path ='Data_db/(1-3)Seeds/'
	output_path='Data_db/(2-2)Data_ckip_seeds/'
	process_Seeds(input_path, output_path)

if __name__ == '__main__':
	main()
