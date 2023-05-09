from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
import numpy as np
from selenium import webdriver
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
from airflow.operators.python import PythonOperator
from airflow.operators.python import PythonOperator
import numpy as np
from datetime import date
from sqlalchemy import create_engine
# from clickhouse_driver import Client


def crawl_ck():
    driver = webdriver.Chrome()
    driver.get('http://s.cafef.vn/screener.aspx')
    table_id = driver.find_element(By.XPATH,'//*[@id="myTable"]/tbody')


    dfx=[]
    rows = table_id.find_elements(By.TAG_NAME, 'tr')
    for row in rows[:50]:
        # col = [row.find_elements(By.TAG_NAME, "td")[i].text for i in range(11)]
        col = [col.text for col in row.find_elements(By.TAG_NAME, "td")]
        df = pd.DataFrame([col],columns=['stt','ten_cong_ty','ma_co_phieu','san_chung_khoan','thay_doi_5_phien_truoc','von_hoa_thi_truong','klgd','eps','p/e','he_so_beta','gia'])
        dfx.append(df)
    df = pd.concat(dfx, ignore_index=True)
    # df = df.sort_values(by='gia',ascending = False)
    df['date'] = [date.today()] * len(df.index)
    df = df[['date','ten_cong_ty','ma_co_phieu','san_chung_khoan','thay_doi_5_phien_truoc','von_hoa_thi_truong','klgd','eps','p_e','he_so_beta','gia']]
    
    print(df.head(5))
    time.sleep(5)
    driver.close()
    return df

clickhouse_info = {
    "host": "localhost",
    "user": "default",
    "password": ""
}
# client = Client(host=clickhouse_info['host'], user=clickhouse_info['user'],
#                 password=clickhouse_info['password'], settings={'use_numpy': True})
# client.insert_dataframe('insert into test.data_ck values', crawl_ck())

dag = DAG(
    'crawl_dag',
    default_args= {
        'email' : ['thanhnb@ftech.ai'],
        'email_on_failure': True,
        'retries' : 1,
        'retry_delay' : timedelta(minutes=3),
    },
    description='time_crawl',
    schedule_interval= "0 0 * * 1-5",
    start_date= datetime.today() - timedelta(days=1),
    tags=['thanhnb_crawl']
)
crawl_data = PythonOperator(
    task_id ='crawl_data',
    python_callable=crawl_ck,
    dag = dag
)

crawl_data