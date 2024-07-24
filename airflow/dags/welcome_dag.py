from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests
import base64
from operators.hello_operator import HelloOperator

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
    # how to decode - in file secrets.txt
    YOUR_API_KEY = base64.b64decode("MjM2ZmIzNDM3NzBkNDI3ZmFiODEyNTk1OTI0MjMwNw==").decode("utf-8")
    url_api = f'http://api.weatherapi.com/v1/current.json?key={YOUR_API_KEY}&q=bulk'
    response = requests.get(url_api)
    print('json full: ' + str(response)) 
    json_full = response.json() #['location']
    print(str(json_full))
    location = json_full['location']['tz_id']
    temp_c = json_full['current']['temp_c']
    print('AIS location' + str(location) + f'and temperature = {temp_c} C')

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

hello_task = HelloOperator(task_id="hello_task", name="Arti")

# Set the dependencies between the tasks
print_welcome_task >> print_date_task >> print_random_quote
print_date_task >> print_weather
print_date_task >> hello_task
