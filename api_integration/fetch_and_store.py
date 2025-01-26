"""
Author: Akbobek Abilkaiyrkyzy
Purpose: Fetch fitness data from the simulated API and store it in a CSV file.
"""

import requests
import csv
import time

# File name for the CSV
CSV_FILE = "fitness_data.csv"

# Initialize CSV file with headers if it doesn't exist
def initialize_csv():
    try:
        with open(CSV_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "timestamp", "steps", "heart_rate"])  # CSV headers
    except FileExistsError:
        pass  # File already exists

# Fetch data from API and append to CSV
def fetch_and_store_data():
    """
    Fetch data from the simulated API and append it to the CSV file.
    """
    url = 'http://127.0.0.1:5000/fitness-data'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([data['user_id'], data['timestamp'], data['steps'], data['heart_rate']])
            print(f"Data inserted: {data}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == '__main__':
    initialize_csv()  # Ensure CSV is initialized
    for _ in range(10):  # Simulate fetching data 10 times
        fetch_and_store_data()
        time.sleep(1)  # Delay between fetches (1 second)
