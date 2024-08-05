from langchain_openai import OpenAI
from langchain.agents.tools import Tool, BaseTool
from langchain_core.tools import ToolException
from langchain.chains import LLMMathChain
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_core.prompts import PromptTemplate
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import gradio as gr


openai_params = {
    "base_url": "http://server-dev:8000/v1",
    "api_key": "EMPTY",
    "model_name": "glm-4-9b-chat",
    "max_tokens": 2048,
    "verbose": True,
    "temperature": 0.9
}


def search_with_bing(query):
    url = f'https://cn.bing.com/search?q={quote(query)}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 ' +
        'Safari/537.36'
    }
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    result_elements = soup.select('#b_results > li')
    data = []
    for parent in result_elements:
        if parent.select_one('h2') is None:
            continue
        data.append({
            'title': parent.select_one('h2').text,
            'snippet': parent.select_one('div.b_caption > p').text,
            'link': parent.select_one('div.b_tpcn > a').get('href')
        })
    return data


class BingSearchTool(BaseTool):
    name = "Bing搜索工具"
    description = "当您需要回答有关当前事件或世界当前状态的问题时很有用"

    def _run(self, query):
        print("\n*****langchain传入*****\n")
        print(query)
        print("\n***************\n")
        data = search_with_bing(query)
        return data


def _handle_tool_error(error: ToolException) -> str:
    return (
        "调用工具发生错误：\n" + error.args[0]
    )


def init_agent():
    llm = OpenAI(**openai_params)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    tools = [BingSearchTool(),
             Tool(
        name="计算器",
        func=llm_math_chain.run,
        description="在需要回答数学问题时很有用",
        handle_tool_error=_handle_tool_error
    ),]
    agent_chain = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent_chain


def chat_langchain(query: str, history: list):
    # 构建提示词
    prompt_template = PromptTemplate.from_template(
        "使用Bing搜索一下以下问题：{query}，如果问题中含有数学计算，请用计算器工具计算"
    )
    prompt = prompt_template.format(query=query)
    answer = "### 提示词：\n" + prompt
    yield answer
    # 运行链
    agent_chain = init_agent()
    response = agent_chain.invoke(input=query)
    answer = answer + "\n### 结果：\n" + response["output"]
    yield answer


def chat_bot():
    chatbot = gr.Chatbot(height=450, label='langchain')
    with gr.Blocks(fill_height=True) as demo:
        gr.ChatInterface(
            fn=chat_langchain,
            chatbot=chatbot,
            fill_height=True
        )
    return demo


if __name__ == "__main__":
    demo = chat_bot()
    demo.launch(server_name="0.0.0.0", server_port=6006)
