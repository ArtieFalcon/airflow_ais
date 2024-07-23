from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests

def print_welcome():
    print('AIS! Welcome to Airflow!')

def print_date():
    print('Today is {}'.format(datetime.today().date()))

def print_random_quote():
    response = requests.get('https://api.quotable.io/random')
    quote = response.json()['content']
    author = response.json()['author']
    print('Quote of the day: "{}"'.format(quote) + f' by {author}' )

def print_weather():
    API_key = '1d91c38465f45fd37bd5d673da5439f4'
    url_api = f'https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&appid={API_key}'
    response = requests.get(url_api)
    timezone = response.json() #['timezone']
    #author = response.json()['author']
    print(timezone)
    #print('Weather in {}'.format(timezone))

dag = DAG(
    'welcome_ais_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 11 * * *',
    catchup=False
)

print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag
)

print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag
)

print_random_quote = PythonOperator(
    task_id='print_random_quote',
    python_callable=print_random_quote,
    dag=dag
)

print_weather = PythonOperator(
    task_id='print_weather',
    python_callable=print_weather,
    dag=dag
)

# Set the dependencies between the tasks
print_welcome_task >> print_date_task >> print_random_quote
print_date_task >> print_weather

