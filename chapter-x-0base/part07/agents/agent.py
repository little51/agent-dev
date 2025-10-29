import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
os.environ['OPENAI_API_BASE'] = 'http://localhost:11434/v1'
os.environ["OPENAI_API_KEY"] = "EMPTY"
root_agent = Agent(
    model=LiteLlm(model="openai/qwen3"),
    name='root_agent',description="你是一个优秀的AI Agent",
    instruction="请开始你的表演！",
)