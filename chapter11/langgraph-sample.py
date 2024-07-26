import os
import sqlite3
from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.checkpoint import MemorySaver
from langchain_openai import ChatOpenAI


def init_db():
    """初始化数据库信息"""
    if not os.path.exists('test.db'):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('''create table users
                 (id int primary key not null,
                 name varchar not null,
                 mail varchar not null);''')
        c.execute("insert into users (id, name, mail) " +
                  "values (1, 'John', 'john@test.com')")
        c.execute("insert into users (id, name, mail) " +
                  "values (2, 'Tom', 'tom@test.com')")
        conn.commit()
        conn.close()


def query_from_db(sql: str):
    """使用SQL语句从数据库查询信息"""
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    conn.close()
    return rows


@tool
def search(query: str):
    """从数据库查询用户信息"""
    return str(query_from_db(query))


tools = [search]
tool_node = ToolNode(tools)
model = ChatOpenAI(model="glm-4-9b-chat",
                   base_url="http://172.16.62.167:8000/v1/",
                   api_key="EMPTY", temperature=0).bind_tools(tools)


def should_continue(state: MessagesState) -> Literal["tools", END]:
    '''定义继续条件'''
    messages = state['messages']
    last_message = messages[-1]
    # 如果LLM命中了tool call, 则路由到tools节点
    if last_message.tool_calls:
        return "tools"
    # 否则以LLM的返回回复用户，结束对话
    return END


def call_model(state: MessagesState):
    '''Agent调用LLM的方法'''
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}


def init_workflow():
    # 创建状态图以管理消息状态和流程控制
    workflow = StateGraph(MessagesState)
    # 定义将循环运行的两个节点
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    # 定义工作流的入口点为agent节点
    workflow.set_entry_point("agent")
    # 添加条件边，当agent被调用时判断是否继续流转
    workflow.add_conditional_edges(
        "agent",
        should_continue,
    )
    # 添加两个普通边，tools被调用完后，继续调用agent
    workflow.add_edge("tools", 'agent')
    # 初始化内存以在状态图运行过程中保持状态
    checkpointer = MemorySaver()
    # 将工作流编译成一个可执行的App
    app = workflow.compile(checkpointer=checkpointer)
    return app


if __name__ == "__main__":
    init_db()
    app = init_workflow()
    inputs = {"messages": [HumanMessage(
        content="从数据库查询一下id=1的用户信息？")]}
    i = 0
    for output in app.stream(
            inputs,
            config={"configurable": {"thread_id": 42}}):
        for key, value in output.items():
            i = i + 1
            print(f"\n===========\n{i}、从'{key}'输出:")
            print(value)
