import os
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

os.environ['OPENAI_API_BASE'] = 'http://localhost:11434/v1'
os.environ["OPENAI_API_KEY"] = "EMPTY"
llm = ChatOpenAI(model="qwen3")

class ConversationState(BaseModel):
    messages: list = Field(default_factory=list)
    service_type: str = "quick"  # 'quick' 或 'expert'
    final_answer: str = ""

# 构建图
builder = StateGraph(ConversationState)

# 节点1：判断服务类型
def route_service(state: ConversationState):
    """判断使用快捷服务还是专家服务"""
    print("判断服务类型...")
    if not state.messages:
        state.service_type = "quick"
        return state
    user_content = state.messages[-1].get("content", "").lower()
    # 快捷服务的关键词
    quick_service_keywords = [
        '查询', '时间', '怎么'
    ]
    # 检查是否快捷服务
    if any(keyword in user_content for keyword in quick_service_keywords):
        state.service_type = "quick"
    else:
        # 其他情况都用专家服务
        state.service_type = "expert"
    print(f"服务类型: {state.service_type}")
    return state

# 节点2：处理问题
def process_question(state: ConversationState):
    """根据服务类型处理问题"""
    print(f"使用{state.service_type}服务处理...")
    user_content = state.messages[-1].get("content", "")
    if state.service_type == "quick":
        # 快捷服务：带上/nothink，直接回答
        prompt = f"{user_content}/nothink"
        response = llm.invoke([HumanMessage(content=prompt)])
        state.final_answer = response.content
    else:
        # 专家服务：正常思考过程
        response = llm.invoke([HumanMessage(content=user_content)])
        state.final_answer = response.content
    state.messages.append({"role": "assistant", "content": state.final_answer})
    return state

# 添加节点
builder.add_node("route", route_service)
builder.add_node("process", process_question)

# 设置工作流
builder.add_edge(START, "route")
builder.add_edge("route", "process")
builder.add_edge("process", END)

# 编译图
graph = builder.compile()

# 测试
def test_graph():
    test_cases = [
        "查询账户余额",              # 快捷服务
        "我要投诉服务质量问题",      # 专家服务
        "你们的营业时间是什么",      # 快捷服务
        "找人工客服",               # 专家服务
        "这个产品怎么用"            # 快捷服务
    ]
    for i, question in enumerate(test_cases, 1):
        print(f"\n=== 测试{i}: {question} ===")
        state = ConversationState(
            messages=[{"role": "user", "content": question}])
        result = graph.invoke(state)
        print(f"服务类型：{result['service_type']}")
        print(f"回答：{result['final_answer']}")

if __name__ == "__main__":
    test_graph()