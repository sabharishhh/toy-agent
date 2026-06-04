from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

ollama_api_key = os.getenv("OLLAMA_API_KEY")

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["/Users/sabharishhh/Developer/Langgraph Project/src/mathserver.py"],
                "transport": "stdio",
            },
            
            "weather": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable-http"
            }
        } # type: ignore
    )

    tools = await client.get_tools()
    model = ChatOpenAI(
        model="qwen3-coder:480b-cloud",
        base_url="https://ollama.com/v1",
        api_key=ollama_api_key,
        temperature=0.2
    )

    agent = create_react_agent(
        model = model,
        tools=tools
    )

    math_response = await agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": "What is (3 + 5) * 12 ? provide step-bystep answer"
        }]
    })

    print("Math repsosne:", math_response["messages"][-1].content)

    weather_response = await agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": "What is the weather in California ?"
        }]
    })

    print("Weather repsosne:", weather_response["messages"][-1].content)

asyncio.run(main())