import os
from dotenv import load_dotenv
from database import set_user, get_user_location, user_exists
from solis_agent import ask_solis

# Load API key
load_dotenv()

def chat_with_solis(user_name, user_input):
    """
    Handles user input and delegates tasks to the Solis agent.
    """
    if "set location" in user_input.lower():
        location = user_input.split("set location")[-1].strip()
        set_user(user_name, location)
        return f"📍 Location set to {location}. Now I can provide weather-based reminders!"

    # Let Solis handle everything else dynamically
    return ask_solis(user_name, user_input)

# ✅ Modify main() to ensure user exists in the database
def main():
    user_name = input("Enter your name: ")  # Identify user

    # ✅ Check if the user exists, if not, add them
    if not user_exists(user_name):
        location = input("Where do you live (City, State)? ")
        set_user(user_name, location=location)  # Add user with no location set yet
        print(f"👋 Hello {user_name}, I've saved your profile!")

    print(f"🌿 Welcome to Solis, {user_name}! Ask me anything about gardening.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Happy gardening! 🌱")
            break

        response = chat_with_solis(user_name, user_input)
        print(f"Solis: {response}\n")

if __name__ == "__main__":
    main()