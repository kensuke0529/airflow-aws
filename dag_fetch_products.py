from airflow.decorators import dag, task
from datetime import datetime
from fake_store_pipeline import fetch_api, transform, load
import os

BUCKET_NAME = "airflow-project-ken"


@dag(
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["fake_store", "api", "aws"],
)
def fake_store_products_dag():

    @task()
    def fetch():
        return fetch_api.fetch_data_from_api()

    @task()
    def transform_task(json_path: str):
        return transform.transform_json_to_csv(json_path)

    @task()
    def upload_task(csv_path: str):
        date_folder = datetime.now().strftime('%Y-%m-%d')
        s3_key = f"fake_store/{date_folder}/products.csv"
        load.upload_to_s3(csv_path, BUCKET_NAME, s3_key)
        return s3_key

    json_file = fetch()
    csv_file = transform_task(json_file)
    upload_task(csv_file)


fake_store_products_dag = fake_store_products_dag()
