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
    YOUR_API_KEY = '236fb343770d427fab8125959242307' 
    url_api = f'http://api.weatherapi.com/v1/current.json?key={YOUR_API_KEY}&q=bulk'
    response = requests.get(url_api)
    print('json full: ' + str(response))
    json_full = response.json() #['location']
    tz_id = json_full['location'].tz_id
    print(json_full)
    print('AIS location' + str(tz_id))


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

