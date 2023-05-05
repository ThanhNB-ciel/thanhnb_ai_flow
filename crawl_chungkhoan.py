import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import os,time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# '//*[@id="data"]'


driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('http://s.cafef.vn/screener.aspx')
table_id = driver.find_element(By.XPATH,'//*[@id="myTable"]/tbody')


dfx=[]
rows = table_id.find_elements(By.TAG_NAME, 'tr')
for row in rows[:101]:
    # col = [row.find_elements(By.TAG_NAME, "td")[i].text for i in range(11)]
    col = [col.text for col in row.find_elements(By.TAG_NAME, "td")]
    df = pd.DataFrame([col],columns=['stt','ten_cong_ty','ma_co_phieu','san_chung_khoan','thay_doi_5_phien_truoc','von_hoa_thi_truong','klgd','eps','p/e','he_so_beta','gia'])
    dfx.append(df)
df = pd.concat(dfx, ignore_index=True)
df = df.sort_values(by='gia',ascending = False)
# df.to_csv('ck.csv')

print(df.head(10))
time.sleep(5)
driver.close()






    
    
# url = 'https://s.cafef.vn/screener.aspx#data'
# response  = requests.get(url)
# html = response.content
# soup = BeautifulSoup(html,'html.parser')
# table = soup.find('table')
# data = []
# for row in table.finall('li'):
#     cols = row.find_all('td')
#     cols = [col.text.strip() for col in cols]
#     data.append(cols)
# print(data)


# import pandas as pd
# from selenium import webdriver

# # Khởi tạo webdriver
# # driver = webdriver.Chrome(executable_path='chromedriver.exe')
# # driver.get('http://s.cafef.vn/screener.aspx')

# # Đợi cho trang tải xong
# driver.implicitly_wait(10)

# # Tìm thẻ chứa bảng dữ liệu
# # table_id = driver.find_element(By.XPATH,'//*[@id="data"]')

# # Đọc bảng dữ liệu bằng phương thức read_html của pandas
# df_list = pd.read_html(table_id.get_attribute('class'))

# # Lấy bảng đầu tiên
# df = df_list[0]

# # In kết quả
# print(df.head())


# tables = pd.read_html('http://s.cafef.vn/screener.aspx')

# # Chọn bảng thứ nhất (có thể có nhiều bảng trên một trang web)
# df = tables[1]

# # In kết quả
# print(df.head())