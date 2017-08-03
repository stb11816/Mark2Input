#coding='utf-8'
from Mark2CRF import Mark2CRF_CKIP_articles
from Mark2CRF import Mark2CRF_CKIP_seed
from Mark2CRF import Mark2CRF_match
from Mark2CRF import Mark2CRF_preprocess

def main():
	source=['ptt','mobile01']
	date_range=['2015-12','2017-07']
	raw_dir='./Data_db/(0)Data_mark/'
	output_raw      ='./Data_db/(1-1)Data_preprocess_raw/'
	output_label    ='./Data_db/(1-2)Data_preprocess_label/'
	output_seed     ='./Data_db/(1-3)Seeds/'
	output_raw_ckip ='./Data_db/(2-1)Data_ckip_articles/'
	output_seed_ckip='./Data_db/(2-2)Data_ckip_seeds/'
	output_match    ='./Data_db/(3-1)Data_match/'
	output_match_n  ='./Data_db/(3-2)Data_match_n/'

	# Mark2CRF_preprocess.main(source,date_range,raw_dir,output_raw,output_seed,output_label)

	# Mark2CRF_CKIP_articles.process_Articles(output_raw,output_raw_ckip)

	# Mark2CRF_CKIP_seed.process_Seeds(output_seed,output_seed_ckip)

	Mark2CRF_match.match(output_raw_ckip,output_label,output_match,space=output_match_n)



if __name__ == '__main__':
	main()
