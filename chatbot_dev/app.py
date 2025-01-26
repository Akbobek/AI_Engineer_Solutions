from transformers import AutoModelForCausalLM, AutoTokenizer
from data_handler import DataHandler
import re

# Initialize Hugging Face model
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Fix for missing pad_token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Initialize data handler
data_handler = DataHandler(
    db_path="./data/fitness_db.db",
    csv_path="./data/workout_data.csv",
    pdf_path="./data/workout_routines.pdf"
)

def extract_user_id(prompt):
    """Extract user ID from the prompt using regex."""
    match = re.search(r"user (\d+)", prompt.lower())
    if match:
        return int(match.group(1))
    return None

def chatbot_response(prompt):
    """Generate chatbot response based on user prompt."""
    user_id = extract_user_id(prompt)  # Extract user ID from the prompt

    # If user ID is found, handle data-specific queries
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

    # Handle workout routines query
    if "workout routines" in prompt.lower():
        pdf_response = data_handler.query_pdf()
        return f"Workout Routines:\n{pdf_response[:500]}..."  # First 500 characters

    # Default to model-based response
    inputs = tokenizer(prompt + tokenizer.eos_token, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[:, inputs["input_ids"].shape[-1]:][0], skip_special_tokens=True)
    return response

# Run chatbot
if __name__ == "__main__":
    print("Chatbot is ready! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chatbot_response(user_input)
        print(f"Bot: {response}")
