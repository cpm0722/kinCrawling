#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

'공백 및 코드 제거 후 제목만 남김'
def getTitle(code):
	title = str(code).split('title">')[1].split('</div>')[0].strip();
	return title;

'문장 코드에서 문장만 남김'
def getAnswerContent(code):
	answer = str(code).split('">')[1].split('</span>')[0];
	'문장이 아닌 개행 일 경우, 링크일 경우'
	if len(answer) < 4:
		return "";
	elif 'http' in answer:
		return "";
	elif 'www' in answer:
		return "";
	return answer;

yesterday = datetime.strftime(datetime.now() - timedelta(2), '%Y%m%d');
key_number = 1;
f = open(yesterday + '_keyword' + str(key_number) + '_data', 'w');

keyword_file = open('20191119_keyword1_id', 'r');
id_string = keyword_file.readline();
n = 0;
while id_string <> "":
	n = n + 1;
	dirId = id_string.split(',')[0];
	docId = id_string.split(',')[1].split('\n')[0];
	id_string = keyword_file.readline();

	base_url = 'https://kin.naver.com/qna/detail.nhn?dirId='
	mid_url = '&docId='
	url_input = base_url + dirId + mid_url + docId;
	f.write('\n<==========URL' + str(n) + ': ' + url_input + '==========>\n');
	res = requests.get(url_input);
	soup = BeautifulSoup(res.content, 'html.parser');

	'질문의 제목 획득'
	question_title = soup.find(class_='c-heading__title-inner').find(class_='title');
	f.write("\n<===Question Title===>\n");
	f.write(getTitle(question_title));

	'질문의 내용 획득'
	question_content = soup.find(class_='c-heading__content');
	'공백 및 태그 제거'
	question_content = str(question_content).split('content">')[1].lstrip().split('</div>')[0].rstrip();
	question_content = question_content.replace("<br/>", "\n");

	'개행문자 변환 및 제거'
	question_content = question_content.replace("" + chr(10), "\n");
	question_content = question_content.replace("" + chr(9), "\n");
	while question_content.find("\n\n") <> -1:
		question_content = question_content.replace("\n\n", "\n");
	while question_content.find("\n \n") <> -1:
		question_content = question_content.replace("\n \n", "\n");
	f.write("\n<===Question Content===>\n");
	f.write(question_content);

	'답변 list 획득'
	answer_content_list = soup.find(class_='answer-content__list _answerList').find_all(class_='answer-content__item _contentWrap _answer');
	for i in range(len(answer_content_list)):
		f.write('\n<===Answer ' + str(i) + '===>\n');
		'답변 내용 중 image 등 제외하고 text data만 추출'
		'답변 내용 중 image가 삽입되어 text가 여러 문단으로 구분되었을 수 있으므로 2차원 list로 사용'
		answer_content_list[i] = answer_content_list[i].find_all(class_='se-module se-module-text');
	for i in range(len(answer_content_list)):
		'각 답변마다 문장 list 획득'
		answer_sentence_list = [];
		answer_sentence_list_processed = [];
		for j in range(len(answer_content_list[i])):
			answer_sentence_list = answer_content_list[i][j].find_all('span');
			'문장 list를 실제 문장 내용만 남게 처리'
			for k in range(len(answer_sentence_list)):
				tmpStr = getAnswerContent(answer_sentence_list[k]);
				'공백일 경우 list에 추가 X'
				if tmpStr <> "":
					answer_sentence_list_processed.append(tmpStr);

		for l in range(len(answer_sentence_list_processed)):
			f.write(answer_sentence_list_processed[l]);
keyword_file.close();
f.close();
