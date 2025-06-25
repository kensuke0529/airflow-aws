import json
import csv
from typing import Optional


def transform_json_to_csv(input_path: str, output_path: Optional[str] = None) -> str:
    """
    Transform raw products JSON to a simplified CSV file.

    Args:
        input_path (str): Path to the input JSON file - data from the API
        output_path (str, optional): Path to save the transformed CSV file. 
            If None, saves next to input file with suffix '_transformed.csv'.
    """

    if output_path is None:
        output_path = input_path.replace('.json', '_transformed.csv')

    with open(input_path, 'r') as file:
        products = json.load(file)

    # Define which fields you want to keep
    fields = ['id', 'title', 'price', 'category']

    # Open output CSV file and write rows
    with open(output_path, 'w', newline='') as csvfile:

        # csv.DictWriter: writes CSV from python dictionaries
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # Write header row
        writer.writeheader()

        # Write data rows
        for product in products:
            # Extract only needed fields; if field missing, default to None
            row = {field: product.get(field, None) for field in fields}
            writer.writerow(row)

    return output_path
