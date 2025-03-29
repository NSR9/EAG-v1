from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
from telegram import Bot
from langchain.agents import initialize_agent

# Initialize LLM and Memory
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)  # Slightly increased creativity
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Tool 1: Get OTT shows

def get_ott_shows(query: str):
    search = SerpAPIWrapper()
    result = search.run(query)
    return f"Mass recommendations just for you: {result}"

# Tool 2: Send to Telegram

def send_telegram_message(message: str):
    bot = Bot(token="8033504648:AAEy-2isKltQevWorNSvJFra5nPEraEKNMw")
    bot.send_message(chat_id="6620452499", text=message)
    return "Message sent to your Telegram like a boss!"

# Tools list

tools = [
    Tool(
        name="OTT Search",
        func=get_ott_shows,
        description="Use this to fetch trending OTT content when user asks for movies or shows."
    ),
    Tool(
        name="Send Telegram",
        func=send_telegram_message,
        description="Use this to send your final answer to Telegram with style."
    ),
]

# # Initialize the LangChain agent

# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent="chat-conversational-react-description",
#     memory=memory,
#     verbose=True,
#     handle_parsing_errors=True
# )

# def run_agentic_query(query: str):
#     pushpa_prompt = (
#         f"Act like Pushpa Raj. Give a confident, massy answer to the following question: '{query}'. "
#         "Once you are confident that you have the correct and full answer, send it to Telegram. "
#         "End your answer with 'Thaggede Le!'"
#     )
#     result = agent.run(pushpa_prompt)
#     return result, memory.buffer

def run_agentic_query(query: str, memory):
    # Reuse the existing llm and tools setup
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="chat-conversational-react-description",
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
    pushpa_prompt = (
        f"Act like Pushpa Raj. Answer confidently: '{query}'. "
        "Remember the conversation context. End with 'Thaggede Le!'"
        "Once you are confident that you have the correct and full answer, send it to Telegram. "   
    )
    result = agent.run(pushpa_prompt)
    print(f"\n\n MEMORY: {memory.buffer}\n\n")
    return result, memory.buffer