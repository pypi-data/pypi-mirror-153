from airflow.models import DAG
from airflow.operators.python import PythonOperator


def first_func():
    print("first_func execution")


def second_func():
    print("second_func execution")


dag_task_series = DAG(dag_id="dag_task_series", schedule_interval=None)


first_func_task = PythonOperator(
    task_id="first_func",
    provide_context=True,
    python_callable=first_func,
    dag=dag_task_series,
)

second_func_task = PythonOperator(
    task_id="second_func",
    provide_context=True,
    python_callable=second_func,
    dag=dag_task_series,
)


first_func_task >> second_func_task
