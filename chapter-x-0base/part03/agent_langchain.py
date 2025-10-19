import os
from langchain.agents import create_agent
os.environ['OPENAI_API_BASE'] = 'http://localhost:11434/v1'
os.environ["OPENAI_API_KEY"] = "EMPTY"


def calculator(expression: str) -> str:
    """用于执行数学计算。输入是一个数学表达式，例如：'15 ** 2 + 28 / 4'"""
    try:
        print("\n======调用到工具=======\n")
        print(expression)
        print("\n======================\n")
        return str(eval(expression))
    except Exception as e:
        return f"计算错误: {e}"


agent = create_agent(
    model="openai:qwen3", tools=[calculator],
    system_prompt="你是一个用于执行数学计算的Agent",
)
response = agent.invoke(
    {"messages": [{"role": "user", "content": "计算15的平方加上32除以4的结果是多少？"}]}
)
print(response)
