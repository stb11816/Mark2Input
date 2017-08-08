#coding='utf-8'
from Mark2CRF import Mark2CRF_CKIP_articles
from Mark2CRF import Mark2CRF_CKIP_seed
from Mark2CRF import Mark2CRF_match
from Mark2CRF import Mark2CRF_preprocess

def main():
	source=['ptt','mobile01']
	date_range=['2015-12','2017-07']
	data_raw      ='./Data_db/(0)Data_mark/'
	data_pre      ='./Data_db/(1-1)Data_preprocess_raw/'
	data_label    ='./Data_db/(1-2)Data_preprocess_label/'
	data_seed     ='./Data_db/(1-3)Seeds/'
	data_pre_ckip ='./Data_db/(2-1)Data_ckip_articles/'
	data_seed_ckip='./Data_db/(2-2)Data_ckip_seeds/'
	data_match    ='./Data_db/(3-1)Data_match/'
	data_match_n  ='./Data_db/(3-2)Data_match_n/'

	Mark2CRF_preprocess.main(source, date_range, data_raw, data_pre, data_seed, data_label)
	Mark2CRF_CKIP_articles.process_Articles(data_pre, data_pre_ckip)
	Mark2CRF_CKIP_seed.process_Seeds(data_seed, data_seed_ckip)
	Mark2CRF_match.match(data_pre_ckip, data_label, data_match, space=data_match_n)



if __name__ == '__main__':
	main()
