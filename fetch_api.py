from airflow.providers.http.hooks.http import HttpHook
import json
from datetime import datetime


def fetch_data_from_api():
    http = HttpHook(method='GET', http_conn_id='fake_store_api')

    # http.run: send a GET request to the endpoint 'products'
    response = http.run(endpoint='products')
    products = response.json()

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_path = f'/tmp/fake_store_products_{timestamp}.json'

    # open the file in the container and write the Json data
    with open(output_path, 'w') as file:
        # products is a list of dictionaries
        json.dump(products, file, indent=2)

    # Just return the path; Airflow will push this return value to XCom automatically
    return output_path
