import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="gpt-3.5-turbo",
        base_url="http://localhost:11434/v1",
        api_key="EMPTY"
    )
    # 创建数学专家助手
    math_agent = AssistantAgent(
        "math_expert",
        model_client=model_client,
        system_message="你是一名数学专家。",
        description="数学专家助手。",
        model_client_stream=True,
    )
    math_agent_tool = AgentTool(math_agent, 
                                return_value_as_last_message=True)
    # 创建化学专家助手
    chemistry_agent = AssistantAgent(
        "chemistry_expert",
        model_client=model_client,
        system_message="你是一名化学专家。",
        description="化学专家助手。",
        model_client_stream=True,
    )
    chemistry_agent_tool = AgentTool(
        chemistry_agent, return_value_as_last_message=True)
    # 创建主助手，可使用专家工具
    agent = AssistantAgent(
        "assistant",
        system_message="你是一个通用助手。需要时请使用专家工具。",
        model_client=model_client,
        model_client_stream=True,
        tools=[math_agent_tool, chemistry_agent_tool],
        max_tool_iterations=10,
    )
    # 运行任务
    await Console(agent.run_stream(task="x^2的积分是什么？"))
    await Console(agent.run_stream(task="水的分子量是多少？"))

asyncio.run(main())
