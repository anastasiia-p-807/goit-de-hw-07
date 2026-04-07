from __future__ import annotations
 
import random
import time
from datetime import datetime, timedelta
 
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.standard.sensors.python import PythonSensor
from airflow.utils.trigger_rule import TriggerRule
 
 
MYSQL_CONN_ID = "mysql_local"
RESULT_TABLE = "medal_counts"
EVENT_TABLE = "athlete_event_results"
 
 
def choose_medal() -> str:
    medals = ["Bronze", "Silver", "Gold"]
    selected_medal = random.choice(medals)
 
    if selected_medal == "Bronze":
        return "count_bronze"
    if selected_medal == "Silver":
        return "count_silver"
    return "count_gold"
 
 
def delay_function(seconds: int) -> None:
    time.sleep(seconds)
 
 
def check_latest_record() -> bool:
    hook = MySqlHook(mysql_conn_id=MYSQL_CONN_ID)
 
    query = f"""
        SELECT created_at
        FROM {RESULT_TABLE}
        ORDER BY created_at DESC
        LIMIT 1
    """
 
    result = hook.get_first(query)
 
    if result is None:
        return False
 
    latest_created_at = result[0]
    current_time = datetime.now()
    time_difference = current_time - latest_created_at
 
    return time_difference.total_seconds() <= 30
 
 
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
}
 
 
with DAG(
    dag_id="airflow_hw_medal_dag",
    default_args=default_args,
    description="Homework DAG for Apache Airflow with branching, MySQL and sensor",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    dagrun_timeout=timedelta(minutes=5),
    tags=["homework", "airflow", "mysql"],
) as dag:
 
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id=MYSQL_CONN_ID,
        sql=f"""
        CREATE TABLE IF NOT EXISTS {RESULT_TABLE} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            medal_type VARCHAR(20) NOT NULL,
            count INT NOT NULL,
            created_at DATETIME NOT NULL
        );
        """,
    )
 
    choose_medal_task = BranchPythonOperator(
        task_id="choose_medal_task",
        python_callable=choose_medal,
    )
 
    def build_insert_sql(medal: str) -> str:
        return f"""
        INSERT INTO {RESULT_TABLE} (medal_type, count, created_at)
        SELECT
            '{medal}' AS medal_type,
            COUNT(*) AS count,
            NOW() AS created_at
        FROM athlete_event_results
        WHERE medal = '{medal}';
        """
 
    count_bronze = SQLExecuteQueryOperator(
        task_id="count_bronze",
        conn_id=MYSQL_CONN_ID,
        sql=build_insert_sql("Bronze"),
    )
    
    count_silver = SQLExecuteQueryOperator(
        task_id="count_silver",
        conn_id=MYSQL_CONN_ID,
        sql=build_insert_sql("Silver"),
    )
    
    count_gold = SQLExecuteQueryOperator(
        task_id="count_gold",
        conn_id=MYSQL_CONN_ID,
        sql=build_insert_sql("Gold"),
    )
 
    join_after_branch = EmptyOperator(
        task_id="join_after_branch",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )
 
    delay_task = PythonOperator(
        task_id="delay_task",
        python_callable=delay_function,
        op_kwargs={"seconds": 10}, # success
        # op_kwargs={"seconds": 35}, # failure
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )
 
    check_latest_record_task = PythonSensor(
        task_id="check_latest_record_task",
        python_callable=check_latest_record,
        poke_interval=5,
        timeout=100,
        mode="poke",
    )
 
    create_table >> choose_medal_task
 
    choose_medal_task >> count_bronze >> join_after_branch
    choose_medal_task >> count_silver >> join_after_branch
    choose_medal_task >> count_gold >> join_after_branch
 
    join_after_branch >> delay_task >> check_latest_record_task