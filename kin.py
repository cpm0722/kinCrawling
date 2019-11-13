#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


url_input = 'https://kin.naver.com/qna/detail.nhn?d1id=10&dirId=100504&docId=339127700&qb=7JWE7J207Y+wIDEx&enc=utf8&section=kin&rank=5&search_sort=0&spq=1'
res = requests.get(url_input);


soup = BeautifulSoup(res.content, 'html.parser');
question_title = soup.find(class_='c-heading__title-inner');
print(question_title);
question_content = soup.find(class_='c-heading__content');
print(question_content);

answer_list = soup.find_all(class_='se-module se-module-text');

for answer in answer_list:
    print(answer);
