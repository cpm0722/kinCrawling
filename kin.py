#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

'공백 및 코드 제거 후 제목만 남김'
def getTitle(code):
	if str(code) <> 'None':
		title = str(code).split('title">')[1].split('</div>')[0].strip();
		'제목이 여러 줄일 경우 개행'
		title = title.replace("<br/>", "\n");
	else :
		title = 'None';
	return title;

'질문의 내용에서 코드 제거 후 내용만 남김'
def getQuestionContent(content):
	'질문의 내용이 있을 경우'
	if str(content) <> 'None':
		'공백 및 태그 제거'
		question_content = str(content).split('content">')[1].lstrip().split('</div>')[0].rstrip();
		question_content = question_content.replace("<br/>", "\n");

		'질문의 내용이 여러 문단일 경우 코드 제거 및 개행 추가'
		question_content = question_content.replace("<span style="">", "");
		question_content = question_content.replace("<div>", "");
		question_content = question_content.replace("</span>", "\n");

		'개행문자 변환 및 제거'
		question_content = question_content.replace("" + chr(10), "\n");
		question_content = question_content.replace("" + chr(9), "\n");
		while question_content.find("\n\n") <> -1:
			question_content = question_content.replace("\n\n", "\n");
		while question_content.find("\n \n") <> -1:
			question_content = question_content.replace("\n \n", "\n");
	else:
		question_content = 'None';
	return question_content;

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
	return answer + '\n';

yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d');
key_number = 0;
f = open(yesterday + '_keyword' + str(key_number) + '_data', 'w');

keyword_file = open(yesterday+'_keyword1_id', 'r');
id_string = keyword_file.readline();
n = 0;
while id_string <> "":
	print(str(n) + "번째 페이지 로딩중\n");
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
	question_content = getQuestionContent(question_content);
	if question_content <> 'None':
		f.write("\n<===Question Content===>\n");
		f.write(question_content);

	'답변 갯수 획득'
	answer_list_len_str = str(soup.find(class_='_answerCount num'));
	answer_list_len_str = answer_list_len_str.split('num">')[1].split('</em')[0];
	answer_list_len = int(answer_list_len_str);
	if answer_list_len > 5:
		answer_list_len = 5;

	'답변 list 획득'
	answer_content_list = [];
	for i in range(answer_list_len):
		while str(soup.find(id='answer_' + str(i+1))) == 'None':
			i = i + 1;
		answer_content_list.append((soup.find(id='answer_' + str(i+1))));
	for i in range(answer_list_len):
		f.write('\n<===Answer ' + str(i) + '===>\n');
		'답변 내용 중 image 등 제외하고 text data만 추출'
		'답변 내용 중 image가 삽입되어 text가 여러 문단으로 구분되었을 수 있으므로 2차원 list로 사용'
		answer_content_list[i] = answer_content_list[i].find_all(class_='se-module se-module-text');
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
