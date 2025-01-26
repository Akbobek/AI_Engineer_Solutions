```markdown
# Fitness Data Simulation and Storage

## Overview
This project simulates an API that provides real-time fitness data for multiple users and stores the data in a structured format (CSV). It demonstrates API development, data fetching, and storage with error handling and testing.

## Features
- Simulated API using Flask.
- Fitness data generation for multiple users.
- Timezone-aware timestamps for accurate tracking.
- Data storage in CSV format.
- Automated test cases to validate API functionality.

## Requirements
To run the project, ensure you have the following dependencies installed:
- Python 3.7+
- Flask
- requests
- pytz

## Setup Instructions

### Step 1: Clone the Repository
Clone or download the project files to your local machine.

### Step 2: Install Dependencies
Install the required Python libraries by running:
```bash
pip install -r requirements.txt
```

### Step 3: Run the API Simulation
Start the simulated API by running:
```bash
python api_simulation.py
```
The API will be accessible at `http://127.0.0.1:5000`.

### Step 4: Fetch and Store Data
Run the script to fetch data from the API and store it in a CSV file:
```bash
python fetch_and_store.py
```
The fitness data will be saved to `fitness_data.csv`.

### Step 5: Run Tests
Run the automated test suite to verify the API functionality:
```bash
python -m unittest test_api_simulation.py
```

## Project Structure
- **`api_simulation.py`**: Simulates the API for generating fitness data.
- **`fetch_and_store.py`**: Fetches data from the API and stores it in a CSV file.
- **`test_api_simulation.py`**: Contains automated test cases for the API.
- **`fitness_data.csv`**: CSV file that stores the fetched fitness data.
- **`requirements.txt`**: Lists the required Python dependencies.

## Example API Response
Here’s an example JSON response from the simulated API:
```json
{
  "user_id": 5,
  "timestamp": "2025-01-26T01:13:15+04:00",
  "steps": 4523,
  "heart_rate": 78
}
```

## Example CSV Output
The stored data in `fitness_data.csv` will look like this:
```csv
user_id,timestamp,steps,heart_rate
10,2025-01-26T00:13:17.216850+04:00,3635,78
4,2025-01-26T00:13:18.227596+04:00,8485,77
2,2025-01-26T00:13:19.234808+04:00,4664,112
```

## Notes
- The API simulates random data for user IDs between 1 and 10.
- Timestamps include timezone information for better accuracy.

## Contact
For questions or feedback, please reach out to **abilbobek@gmail.com**.
```