"""
Author: Akbobek Abilkaiyrkyzy
Purpose: This script simulates an API that provides real-time fitness data for multiple users.
         It generates random steps and heart rate values for users and returns JSON responses.
Features:
- Supports multiple users.
- Adds timestamps with time zones for added realism.
- Encapsulates data generation in a reusable function.
- Includes error handling for invalid user IDs.
"""

from flask import Flask, jsonify, request
from datetime import datetime
import random
import pytz

# Initialize Flask app
app = Flask(__name__)

# Function to generate user fitness data
def generate_user_data(user_id):
    """
    Generate simulated fitness data for a given user.
    
    Args:
        user_id (int): The ID of the user.
    
    Returns:
        dict: Simulated fitness data containing user_id, timestamp, steps, and heart rate.
    """
    current_time = datetime.now(pytz.timezone('Asia/Dubai'))  # Use Dubai timezone
    return {
        "user_id": user_id,
        "timestamp": current_time.isoformat(),  # ISO 8601 format with timezone
        "steps": random.randint(1000, 10000),  # Random steps between 1000 and 10000
        "heart_rate": random.randint(60, 120)  # Random heart rate between 60 and 120
    }

# API endpoint to fetch fitness data
@app.route('/fitness-data', methods=['GET'])
def get_fitness_data():
    """
    Handle GET requests to fetch fitness data.
    
    Query Parameters:
        user_id (int): Optional. Specify the user ID for which to generate data. 
                       If not provided, a random user ID between 1 and 10 is used.
    
    Returns:
        JSON: Simulated fitness data for the user.
    """
    user_id = request.args.get('user_id', default=random.randint(1, 10), type=int)

    # Validate user ID
    if user_id < 1 or user_id > 10:
        return jsonify({"error": "Invalid user_id. Must be between 1 and 10."}), 400

    # Generate and return user data
    data = generate_user_data(user_id)
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000)  # Run locally on port 5000
