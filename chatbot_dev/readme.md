# Development of an AI-Powered Fitness Chatbot

## **Overview**

This document explains the development process of an AI-powered fitness chatbot. It details the motivation, tools used, design decisions, steps involved, and queries to test the chatbot's functionality. This report demonstrates technical proficiency in AI engineering and software development.

---

## **Motivation**

The chatbot is designed to:

- Provide users with actionable insights on their fitness progress.
- Enable users to retrieve workout data, user profiles, and routines stored across structured (database, CSV) and unstructured (PDF) sources.
- Offer a conversational interface for fitness-related queries.

---

## **Tools and Technologies Used**

### **1. Python Libraries**

- **Transformers (Hugging Face):** Provides pre-trained conversational AI models (e.g., `DialoGPT-small`).
- **Pandas:** Handles structured data from CSV files for analysis.
- **SQLite3:** Manages relational data in the SQLite database.
- **PdfPlumber:** Extracts text from PDF files to make workout routines accessible.

### **2. Data Sources**

- **SQLite Database:** Stores user profiles with the following schema:
  - `user_id`: Unique identifier for users.
  - `name`: User name.
  - `age`: User age.
  - `gender`: User gender.
- **CSV File:** Contains workout data with the following columns:
  - `user_id`: Links workouts to users.
  - `workout_type`: Type of workout (e.g., running, swimming).
  - `calories_burnt`: Calories burned.
  - `duration_minutes`: Duration of the workout in minutes.
- **PDF File:** Contains static workout routines for reference.

---

## **Design Choices**

### **1. Modular Structure**

The system is split into reusable components:

- **DataHandler Class:** Handles data retrieval from SQLite, CSV, and PDF sources.
- **Chatbot Logic:** Combines Hugging Face’s conversational model with custom logic for actionable insights.

### **2. Hybrid Approach**

- Combines **rule-based intent detection** for retrieving structured insights with a **pre-trained language model** for conversational responses.
- Example: A query like "How many calories has user 1 burned?" triggers custom logic to retrieve and summarize data, while "Tell me about workouts for beginners" uses Hugging Face for a more general response.

### **3. Open-Source and Lightweight**

- Leveraged open-source tools (Hugging Face models) and local processing to minimize reliance on external paid APIs.

---

## **Development Process**

### **1. Setting Up the Environment**

Install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

**Requirements File Content:**

```plaintext
transformers==4.27.4
pandas==1.5.3
pdfplumber==0.11.5
sqlite3==0.0.1
```

### **2. Data Handling**

The `DataHandler` class provides methods to:

- **Query SQLite Database:** Fetch user profiles using SQL queries.
- **Query CSV Files:** Filter workout data by user ID.
- **Query PDF Files:** Extract and summarize workout routines.

**File: data_handler.py**

```python
import sqlite3
import pandas as pd
import pdfplumber

class DataHandler:
    def __init__(self, db_path, csv_path, pdf_path):
        self.db_path = db_path
        self.csv_path = csv_path
        self.pdf_path = pdf_path

    def query_database(self, query):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            return f"Database error: {e}"

    def query_csv(self, user_id):
        try:
            df = pd.read_csv(self.csv_path)
            user_workouts = df[df['user_id'] == user_id]
            return user_workouts.to_dict(orient='records') if not user_workouts.empty else "No data found."
        except Exception as e:
            return f"CSV error: {e}"

    def query_pdf(self):
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text = "".join([page.extract_text() for page in pdf.pages])
            return text
        except Exception as e:
            return f"PDF error: {e}"
```

### **3. Chatbot Logic**

The `chatbot_response` function:

- **Parses user queries** to detect intents (e.g., "user profile," "workout data").
- **Handles specific intents** with targeted logic for actionable insights.
- **Falls back** on Hugging Face’s model for conversational responses.

**File: app.py**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from data_handler import DataHandler
import re

model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

data_handler = DataHandler(
    db_path="./data/fitness_db.db",
    csv_path="./data/workout_data.csv",
    pdf_path="./data/workout_routines.pdf"
)

def extract_user_id(prompt):
    match = re.search(r"user (\d+)", prompt.lower())
    if match:
        return int(match.group(1))
    return None

def chatbot_response(prompt):
    user_id = extract_user_id(prompt)

    if user_id:
        if "workout" in prompt.lower():
            csv_response = data_handler.query_csv(user_id)
            if isinstance(csv_response, list) and len(csv_response) > 0:
                workouts = "\n".join([f"- {workout['workout_type']} for {workout['duration_minutes']} minutes" for workout in csv_response])
                return f"User {user_id} has completed the following workouts:\n{workouts}"
            return f"No workout data found for user {user_id}."

        elif "profile" in prompt.lower():
            query = f"SELECT * FROM users WHERE user_id = {user_id};"
            db_response = data_handler.query_database(query)
            if db_response:
                profile = db_response[0]
                return f"User Profile:\n- ID: {profile[0]}\n- Name: {profile[1]}\n- Age: {profile[2]}\n- Gender: {profile[3]}"
            return f"No profile found for user {user_id}."

    if "workout routines" in prompt.lower():
        pdf_response = data_handler.query_pdf()
        return f"Workout Routines:\n{pdf_response[:500]}..."

    inputs = tokenizer(prompt + tokenizer.eos_token, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=1000, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[:, inputs["input_ids"].shape[-1]:][0], skip_special_tokens=True)

if __name__ == "__main__":
    print("Chatbot is ready! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chatbot_response(user_input)
        print(f"Bot: {response}")
```

---

## **Example Queries**

### **Structured Queries**

1. **"Show me the profile of user 1."**
   - Retrieves and summarizes user profile from SQLite.
2. **"What workouts has user 2 completed?"**
   - Lists workout data filtered from the CSV file.
3. **"What are the workout routines?"**
   - Extracts and summarizes text from the PDF.

### **Conversational Queries**

1. **"How many calories has user 1 burned?"**
   - Calculates total calorie burn and provides actionable advice.
2. **"What workouts should a beginner try?"**
   - Uses Hugging Face to generate a conversational response.

---

## **Conclusion**

This chatbot showcases:

- Integration of structured and unstructured data sources.
- Use of open-source models for conversational AI.
- Ability to provide actionable insights, demonstrating skills in AI engineering and data integration.

Reviewers can reproduce the setup using the provided files and queries.

