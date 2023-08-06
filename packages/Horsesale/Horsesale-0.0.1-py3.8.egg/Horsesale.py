import requests,re
import pandas as pd
import subprocess as sp
import timeit

def main():
	url = input('JBISのセール上場馬の一覧ページのURLをここに記入してください。: ')
	print('scraping  horse list...')
	page=requests.get(url)
	page.encoding = 'Shift_jis'
	df = pd.read_html(page.text)[0]
	df.columns.values[0]='上場番号'
	df.columns.values[1]='父馬名'
	df.columns.values[2]='母馬名'
	df.columns.values[3]='性別'
	df.columns.values[4]='毛色'
	df.columns.values[5]='販売申込者'
	df.to_csv('horse.csv')
	print('horse.csv was created!')
	df2 = pd.read_csv('horse.csv')
	pd.set_option('display.max_rows', 1000)
	#print(df2)
	fhorse_list = df2.父馬名.unique()
	dd=pd.DataFrame(
	{
		"Sire_horse_list":fhorse_list,
		"number_of_sale_horse":range(len(fhorse_list))
	})
	for i in fhorse_list:
		dd.loc[dd.Sire_horse_list==i, 'number_of_sale_horse']=int(len(df2.loc[df2.父馬名==i]))
	dd=dd.sort_values(by=['number_of_sale_horse'],ascending=False)
	pd.set_option('display.max_rows', 1000)
	print(dd)
	dd.to_csv('number_of_horse_bysire.csv')
	sp.call('rm horse.csv*', shell=True)	

if __name__ == "__main__":
	main()
