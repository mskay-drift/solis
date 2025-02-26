# Solis - AI Gardening Assistant

Solis is an AI gardening assistant designed to help users manage their plants, track watering schedules, and provide gardening advice. Solis uses various tools to interact with users and provide personalized recommendations based on their location and plant types.

## Features

- **Check Weather**: Get weather-based watering recommendations.
- **Get Plant Watering Info**: Retrieve the last watered date for a plant.
- **Log Watering Event**: Log a new watering event for a plant.
- **Add Plant**: Add a plant to the user's tracking list.
- **Get User Plants**: Retrieve the list of plants the user is tracking.
- **Get User Location**: Retrieve the user's location for location-specific recommendations.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/mskay-drift/solis.git
    cd solis
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the project root.
    - Add your WeatherAPI key to the `.env` file:
        ```env
        WEATHER_API_KEY=your_weather_api_key
        ```

## Usage

1. Run the main script:
    ```sh
    python chatbot.py
    ```

2. Follow the prompts to interact with Solis. You can set your location, add plants, log watering events, and get weather-based watering recommendations.
