#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sys
import os

'현재 시각 기준 어제의 날짜 받아옴 (검색 기간: 어제 하루)'
def getYesterday():
	return datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d');

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

def makeIdFile(keyword_file):
	'keyword 파일 열어 한 줄 씩 읽어들어 keyword_list에 입력'
	keyword_list = [];
	with open(keyword_file) as f:
		read_data = f.readline().split('\n')[0];
		while read_data <> '':
			keyword_list.append(read_data);
			read_data = f.readline().split('\n')[0];
		f.close();

	'네이버 지식인 검색 url 획득 위한 변수'
	pre_url = 'https://search.naver.com/search.naver?where=kin&query='
	mid_url = '&kin_sort=0&c_id=&c_name=&sm=tab_opt&sec=0&title=0&answer=0&grade=0&choice=0&nso=so:dd,a:all,p:from'
	end_url = '&ie=utf8'


	'현재까지 얻은 dirId, docId 저장하는 list'
	id_list = [];

	'현재 검색 창 url 획득 위한 변수'
	base_url = 'https://search.naver.com/search.naver';

	'next_page String으로 선언'
	next_page = "";

	yesterday = getYesterday();

	'keyword_list만큼 반복'
	for i in range(len(keyword_list)):
		id_list = [];
		id_list_filename = yesterday + '_keyword' + str(i) + '_id';
		if os.path.isfile(os.getcwd() + '/' + id_list_filename):
			print("이미 " + id_list_filename + "파일이 존재합니다.\n");
			continue;
		print(str(i) + "번째 IdFile 생성 시작\n");
		keyword = keyword_list[i];
		'네이버 지식인 검색 최종 url'
		full_url = pre_url + keyword + mid_url + yesterday + 'to' + yesterday + end_url;
		'현재 검색 창 page url'
		now_page = full_url;

		'다음 페이지 버튼이 없을 때까지 반복'
		while True:
			'현재 page에서 resource 획득'
			res = requests.get(now_page);
			'resource를 html 문법 용해 parsing'
			soup = BeautifulSoup(res.content, 'html.parser');

			'게시글 list 들어있는 content 가져옴'
			content = soup.find(class_='type01');

			'게시글 list contet에서 question class들만 list로 뽑아옴'
			question_list = content.find_all(class_='question');

			'questin class에서 <a href> tag만 뽑아와 url 획득 후 Id로 변환해 id_list에 추가'
			id_string = "";
			for j in range(len(question_list)):
				id_string = getIdFromUrl((getUrlFromTag(question_list[j].find('a'))));
				id_list.append(id_string);

			'현재 화면에서 다음 페이지 버튼의 url을 획득'
			next_page = soup.find(class_='paging').find(class_='next');

			'paging 하위 next class가 none이면 반복문 종료'
			if(str(next_page) == 'None'):
				break;

			'다음 페이지 url 획득'
			next_page = base_url + getUrlFromTag(next_page);

			'Roop 위해 now_page를 next_page로 변경'
			now_page = next_page;
			'next_page 초기화'
			next_page = "";

		'id_list 저장'
		f = open(id_list_filename, 'w');
		for j in range(len(id_list)):
			f.write(id_list[j] + '\n');
		f.close();
		print(str(i) + "번째 IdFile 생성 완료\n");
	return len(keyword_list);

if __name__ == '__main__':
	makeIdFile(sys.argv[1])

