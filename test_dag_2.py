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
import ssl


def crawl_ck():
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
    return True

def email():
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
    out_csv_file_path = 'drive/MyDriver/My_data/data_crawl/data_crawl.csv'
    import base64
    message = Mail(
        from_email='thanhnb@ftech.ai',
        to_emails='baothanh1371997@gmail.com',
        subject='Your file is here!',
        html_content='thanhnb_test_crawl'
    )

    with open(out_csv_file_path, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('data_crawl.csv'),
        FileType('text/csv'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

dag = DAG(
    'mail_dag',
    default_args= {
        'email' : ['thanhnb@ftech.ai'],
        'email_on_failure': True,
        'retries' : 1,
        'retry_delay' : timedelta(minutes=3),
    },
    description='crawl_data_ck',
    schedule_interval= timedelta(days=1),
    start_date= datetime.today() - timedelta(days=1),
    tags=['thanhnb_crawl']
)
crawl_data = PythonOperator(
    task_id ='crawl_data',
    python_callable=crawl_ck,
    dag = dag
)
email_operator = PythonOperator(
    task_id='email_operator',
    python_callable=email,
    dag=dag
)

crawl_data >> email_operator