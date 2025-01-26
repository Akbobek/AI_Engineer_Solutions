import sqlite3
import pandas as pd
import pdfplumber

class DataHandler:
    def __init__(self, db_path, csv_path, pdf_path):
        self.db_path = db_path
        self.csv_path = csv_path
        self.pdf_path = pdf_path

    def query_database(self, query):
        """Execute a query on the SQLite database."""
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
        """Fetch workout data from the CSV for a specific user."""
        try:
            df = pd.read_csv(self.csv_path)
            user_workouts = df[df['user_id'] == user_id]
            return user_workouts.to_dict(orient='records') if not user_workouts.empty else "No data found."
        except Exception as e:
            return f"CSV error: {e}"

    def query_pdf(self):
        """Extract text from the PDF."""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text = "".join([page.extract_text() for page in pdf.pages])
            return text
        except Exception as e:
            return f"PDF error: {e}"
