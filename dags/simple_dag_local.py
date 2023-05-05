from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG(
'thanhnb_dag01',
default_args={
    'email': ['thanhnb@ftech.ai'],
    'email_on_failure' : True,
    'retries' : 1,
    'retry_delay' : timedelta(minutes=3),
},
description= "this is test sample",
schedule_interval= timedelta(days=1), #set up time run
start_date = datetime(2023,5,6),
tags =['thanhnb'],
)
t1 = BashOperator(
    task_id = 'print_date',
    bash_command = 'date',
    dag = dag
)

t2 = BashOperator(
     task_id ='sleep',
     bash_command='sleep 3',
     retries = 3,
     dag = dag
 )
 
t3 = BashOperator(
     task_id ='echo',
     bash_command='echo t3 runing',
     dag = dag
 )

t1 >> t3
t2 >> t3 
