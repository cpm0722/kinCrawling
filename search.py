#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

'a href html Tag에서 Url 주소 획득하는 함수'
def getUrlFromTag(href):
	url = str(href).split('href="')[1];
	url = url.split('" onclick')[0];
	url = url.replace("&amp;", "&");
	return url;

'Url에서 dirId, docId 획득하는 함수'
def getIdFromUrl(url):
	dirId = url.split('dirId=')[1].split('&docId')[0];
	docId = url.split('docId=')[1].split('&qb')[0];
	result = dirId + ',' + docId;
	return result;

'dirId, docId로 Url 복원하는 함수'
def getUrlFromId(id_string):
	dirId = id_string.split(',')[0];
	docId = id_string.split(',')[1];
	url = 'https://kin.naver.com/qna/detail.nhn?dirId=' + dirId + '&docId=' + docId;
	return url;

'네이버 지식인 검색 url 획득 위한 변수'
pre_url = 'https://search.naver.com/search.naver?where=kin&query='
mid_url = '&kin_sort=0&c_id=&c_name=&sm=tab_opt&sec=0&title=0&answer=0&grade=0&choice=0&nso=so:dd,a:all,p:from'
end_url = '&ie=utf8'

keyword = "분신"

'현재 시각 기준 어제의 날짜 받아옴 (검색 기간: 어제 하루)'
yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d');

'네이버 지식인 검색 최종 url'
full_url = pre_url + keyword + mid_url + yesterday + 'to' + yesterday + end_url;

'현재까지 얻은 dirId, docId 저장하는 list'
id_list = [];

'현재 검색 창 page url'
now_page = full_url;

'현재 검색 창 url 획득 위한 변수'
base_url = 'https://search.naver.com/search.naver';

'next_page String으로 선언'
next_page = "";

'다음 페이지 버튼이 없을 때까지 반복'
while True:
	print(now_page);
	'현재 page에서 resource 획득'
	res = requests.get(now_page);
	'resource를 html 문법 용해 parsing'
	soup = BeautifulSoup(res.content, 'html.parser');

	'게시글 list 들어있는 content 가져옴'
	content = soup.find(class_='type01');

	'게시글 list contet에서 question class들만 list로 뽑아옴'
	question_list = content.find_all(class_='question');

	'questin class에서 <a href> tag만 뽑아와 url 획득 후 Id로 변환해 id_list에 추가'
	for i in range(len(question_list)):
		id_list.append(getIdFromUrl((getUrlFromTag(question_list[i].find('a')))));

	'id_list 출력 및 url 출력'
	'''
	for i in range(len(id_list)):
		print(i);
		print(id_list[i]);
		print(getUrlFromId(id_list[i]));
	'''

	'현재 화면에서 다음 페이지 버튼의 url을 획득'
	next_page = soup.find(class_='paging').find(class_='next');

	'paging 하위 next class가 none이면 반복문 종료'
	if(str(next_page) == 'None'):
		print("Roop Finish!");
		break;

	next_page = base_url + getUrlFromTag(next_page);

	'Roop 위해 now_page를 next_page로 변경'
	now_page = next_page;
	'next_page 초기화'
	next_page = "";
