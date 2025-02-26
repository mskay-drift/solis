from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage
from dotenv import load_dotenv
from tools import check_weather, get_plant_watering_info, get_user_location_tool, log_watering_event, add_plant_tool
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
- 'get_user_location_tool': Retrieve the user's location.

🎯 **Rules**:
1. If a user asks to "add" a plant, use the 'add_plant_tool' function.
2. Always confirm when a plant is added.
3. If a user asks what plants they are tracking, return the list.
4. If a user asks a question that requires location-specific information, use the 'get_user_location_tool' to retrieve the user's location.

Be friendly, clear, and helpful! 🌻
"""

# Initialize the LLM
llm = ChatOpenAI(temperature=0.7)

# Initialize the Agent with the new tool
solis_agent = initialize_agent(
    tools=[check_weather, get_plant_watering_info, log_watering_event, add_plant_tool, get_user_location_tool],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    system_message=SystemMessage(content=SYSTEM_PROMPT),
    max_iterations=2,
    memory=memory
)

def ask_solis(user_name: str, user_input: str):
    """Pass user input to Solis and return the response, including user location."""
    location = get_user_location(user_name)
    if location:
        user_input = f"{user_input} (Location: {location})"
    return solis_agent.run(user_input)
