# Mark2Input


將平台標記結果轉換成CRF格式
==========
資料夾(Mark2CRF)：轉換流程所需要的模組
資料夾(Data_db) ：轉換CRF的輸入、輸出以及中間輸出


執行檔：Mark2CRF_start.py
參數source和date_range：可用來篩選欲處理的資料
參數date_raw：標記結果資料夾位置，底下包含不同來源或不同月份的json檔(ex. Data_mark/ptt/MobileComm/2017-08.json)
其餘路徑參數皆為轉換流程的中間輸出位置


轉換流程：
1. Mark2CRF_preprocess.py
- input ：(0)Data_mark
- output：(1-1)Data_preprocess_raw, (1-2)Data_preprocess_label, (1-3)Seeds
先依據來源和時間挑選標記結果json檔，再分別處理成三個輸出檔案(原始文章, 原始文章label, Seed)  
原始文章label是將原始文章以0,1方式表達字元，以1表達term的位置，不包含空格(ex. 我買了一台iphone7 --> [0,0,0,0,0,1,1,1,1,1,1,1])<br />
Seed的json檔包含篩選條件下每篇文章所出現的seed，可使用文章ID查找；seed_integrate.json則會累積每次轉換流程所有的seed

2. Mark2CRF_CKIP_articles.py
- input ：(1-1)Data_preprocess_raw
- output：(2-1)Data_ckip_articles
- 讀取前處理完成的文章並進行斷詞
  
3. Mark2CRF_CKIP_seed.py
  input ：(1-3)Seeds
  output：(2-2)Data_ckip_seeds
  讀取前處理完成的seed並進行斷詞，seed斷詞結果同樣有統整檔(seed_integrate_ckip.json)，統整檔包含完整的斷詞結果

4. Mark2CRF_match.py
  input ：(1-2)Data_preprocess_label, (2-1)Data_ckip_articles
  output：(3-1)Data_match, (3-2)Data_match_n
  不採用原先Term Extraction用seed的比對方法，而是以label與斷詞結果位置產生CRF格式
  space參數預設為False，表示輸出結果中文章之間不新增斷行，若給予space路徑則輸出具有斷行的內容



將平台標記結果轉換成RNN格式
=========================

執行檔：Mark2RNN.py
input ：(0)Data_mark
output：Data_RNN

可依據來源與日期篩選文章，輸出檔案皆為json
allLabel表示內容包含所有label
label+數字則表示只顯示特定label，其餘label皆為0，若整篇文章皆該label(也就是整篇皆為0)則不輸出
json檔內容包含來源資訊，以及兩個list

