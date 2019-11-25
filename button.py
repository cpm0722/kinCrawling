from selenium import webdriver

url = 'https://kin.naver.com/qna/detail.nhn?dirId=60901&docId=341123209';

def get_value():
	driver = webdriver.Chrome()
	driver.get(url)
	driver.find_element_by_id('nextPageButton').click()
	val = driver.find_element_by_id('answer_6').text;
	driver.quit()
	return val

print(get_value())
