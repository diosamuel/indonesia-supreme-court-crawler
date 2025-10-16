from datetime import datetime, timedelta
import os
import subprocess
import logging
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# Default arguments for the DAG
default_args = {
    'owner': 'putusan-ma',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the latest crawler DAG
dag = DAG(
    'latest_crawler_pipeline',
    default_args=default_args,
    description='Latest crawler pipeline that runs daily at 00:00',
    schedule_interval='0 0 * * *',  # Daily at 00:00 (midnight)
    catchup=False,
    tags=['crawler', 'scrapy', 'putusan-ma', 'daily'],
)

# Function to run latest spider
def run_latest_spider():
    """
    Run the latest scrapy spider
    """
    try:
        # Change to the direktori directory
        direktori_path = "/opt/airflow/project/direktori"
        
        # Run scrapy crawl command for latest spider
        cmd = f"cd {direktori_path} && scrapy crawl latest"
        
        logging.info(f"Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=direktori_path)
        
        if result.returncode != 0:
            logging.error(f"Latest spider failed with error: {result.stderr}")
            raise Exception(f"Latest spider execution failed: {result.stderr}")
        
        logging.info("Latest spider completed successfully")
        logging.info(f"Output: {result.stdout}")
        return "Latest spider completed successfully"
        
    except Exception as e:
        logging.error(f"Error running latest spider: {str(e)}")
        raise

# Task: Latest Spider
latest_task = PythonOperator(
    task_id='latest_crawler',
    python_callable=run_latest_spider,
    dag=dag,
)

# Since there's only one task, no dependencies needed
