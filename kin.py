#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

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

url_input = 'https://kin.naver.com/qna/detail.nhn?d1id=1&dirId=1070402&docId=340713730&qb=7Zy064yA7Y+w&enc=utf8&section=kin&rank=1&search_sort=0&spq=0';
res = requests.get(url_input);
soup = BeautifulSoup(res.content, 'html.parser');

'질문의 제목 획득'
question_title = soup.find(class_='c-heading__title-inner').find(class_='title');
print(getTitle(question_title));

'답변 list 획득'
answer_content_list = soup.find(class_='answer-content__list _answerList').find_all(class_='se-module se-module-text');
for i in range(len(answer_content_list)):
	print(i);
	'각 답변마다 문장 list 획득'
	answer_sentence_list = [];
	answer_sentence_list = answer_content_list[i].find_all('span');
	answer_sentence_list_processed = [];
	'문장 list를 실제 문장 내용만 남게 처리'
	for j in range(len(answer_sentence_list)):
		tmpStr = getAnswerContent(answer_sentence_list[j]);
		'공백일 경우 list에 추가 X'
		if tmpStr <> "":
			answer_sentence_list_processed.append(tmpStr);

	for k in range(len(answer_sentence_list_processed)):
			print(answer_sentence_list_processed[k]);
