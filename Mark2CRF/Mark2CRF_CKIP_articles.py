#coding='utf-8'
#讀取文章，進行傳至ckip
import glob,os,sys
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

def process_Articles(input_path, output_path):
	# print('Article2CKIP start')
	articles_path=glob.glob(input_path+r'*.txt')
	checkGlob(articles_path,input_path+r'*.txt')

	if not os.path.exists(output_path):
		os.mkdir(output_path)

	for path in articles_path:
		output_name=os.path.basename(path).replace('.txt','')+'_ckip'
		if os.path.exists(output_path+output_name+'.txt'):
			print(output_path+output_name+'.txt exists!!')
			continue
		else:
			with open(path,'r',encoding='utf-8') as raw:
				contents=raw.readlines()

			output_content=''
			seq=1
			for content in contents:
				article=content.split('\t')[2].replace('\n','')
				result=to_ckip(article)
				
				board_id='\t'.join(content.split('\t')[:2])
				output_content+=board_id+'\t'+str(seq)+'\t'+str(result[0]).replace(' ','')+'\t'+str(result[1]).replace(' ','')+'\n'
				seq+=1

			
			with open(output_path+output_name+'.txt','w',encoding='utf-8') as out:
				out.write(output_content)
	print('Article2CKIP finish')

def main():
	input_path ='Data_db/(1-1)Data_preprocess_raw/'
	output_path='Data_db/(2-1)Data_ckip_articles/'
	process_Articles(input_path, output_path)

if __name__ == '__main__':
	main()
