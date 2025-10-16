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

# Define the main crawler DAG
dag = DAG(
    'main_crawler_pipeline',
    default_args=default_args,
    description='Main crawler pipeline for generate_tree, scrape_details, and scrape_list',
    schedule_interval=None,  # On-demand execution
    catchup=False,
    tags=['crawler', 'scrapy', 'putusan-ma'],
)

# Function to run scrapy spider
def run_scrapy_spider(spider_name):
    """
    Run a specific scrapy spider
    """
    try:
        # Change to the direktori directory
        direktori_path = "/opt/airflow/project/direktori"
        
        # Run scrapy crawl command
        cmd = f"cd {direktori_path} && scrapy crawl {spider_name}"
        
        logging.info(f"Running command: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=direktori_path)
        
        if result.returncode != 0:
            logging.error(f"Spider {spider_name} failed with error: {result.stderr}")
            raise Exception(f"Spider {spider_name} execution failed: {result.stderr}")
        
        logging.info(f"Spider {spider_name} completed successfully")
        logging.info(f"Output: {result.stdout}")
        return f"Spider {spider_name} completed successfully"
        
    except Exception as e:
        logging.error(f"Error running spider {spider_name}: {str(e)}")
        raise

# Task 1: Generate Tree Spider
generate_tree_task = PythonOperator(
    task_id='generate_tree',
    python_callable=run_scrapy_spider,
    op_args=['generate_tree'],
    dag=dag,
)

# Task 2: Scrape List Spider
scrape_list_task = PythonOperator(
    task_id='scrape_list',
    python_callable=run_scrapy_spider,
    op_args=['scrape_list'],
    dag=dag,
)

# Task 3: Scrape Details Spider
scrape_details_task = PythonOperator(
    task_id='scrape_details',
    python_callable=run_scrapy_spider,
    op_args=['scrape_details'],
    dag=dag,
)

# Set task dependencies
# generate_tree should run first, then scrape_list, then scrape_details
generate_tree_task >> scrape_list_task >> scrape_details_task
