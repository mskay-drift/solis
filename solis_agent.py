from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage
from dotenv import load_dotenv
from tools import check_weather, get_plant_watering_info, get_user_location_tool, log_watering_event, add_plant_tool, get_user_plants_tool
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Load API key
load_dotenv()

SYSTEM_PROMPT = """
You are Solis, an AI gardening assistant.
Your job is to help users manage their plants, track watering, and give gardening advice.

🔧 **Tools you can use**:
- 'check_weather': Get weather-based watering recommendations.
- 'get_plant_watering_info': Retrieve when a plant was last watered.
- 'log_watering_event': Log a new watering event.
- 'add_plant_tool': Add a plant to the user's tracking list.
- 'get_user_plants': Get the list of plants the user is tracking.
- 'get_user_location_tool': Retrieve the user's location.

🎯 **Rules**:
1. If a user asks to "add" a plant, use the 'add_plant_tool' function.
2. Always confirm when a plant is added.
3. When checking the weather, first get the user's location using 'get_user_location_tool' and then use 'check_weather' with the retrieved location.
4. If a user asks what plants they are tracking, use the 'get_user_plants' function.
5. If a user asks a question that requires location-specific information (e.g., weather-based recommendations), use the 'get_user_location_tool' to retrieve the user's location.
6. When providing advice, use the user's location to give specific recommendations.

Be friendly, clear, and helpful! 🌻
"""

# Initialize the LLM
llm = ChatOpenAI(temperature=0.7)

# Initialize the Agent with the new tool
solis_agent = initialize_agent(
    tools=[check_weather, get_plant_watering_info, log_watering_event, add_plant_tool, get_user_location_tool, get_user_plants_tool],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    system_message=SystemMessage(content=SYSTEM_PROMPT),
    max_iterations=4,
    memory=memory
)

def ask_solis(user_input: str):
    """Pass user input to Solis and return the response, including user location."""
    return solis_agent.run(user_input)
