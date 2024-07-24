import autogen
import gradio as gr

config_list = [
    {"model": "glm-4-9b-chat",
     "base_url": "http://172.16.62.167:8000/v1",
     "api_key": "EMPTY",
     "stream": True,
     "cache_seed": None
     }
]


def reflection_message(recipient, messages, sender, config):
    return f"reviewer对programer的工作进行审核。\n\n " \
        f"{recipient.chat_messages_for_summary(sender)[-1]['content']}"


def init_agents():
    programer = autogen.AssistantAgent(
        name="programer",
        llm_config={"config_list": config_list},
        system_message="""
            你是一个优秀的人工智能编程助手。
            能够编写Python程序或编写JSON格式的文件
        """,
    )

    reviewer = autogen.AssistantAgent(
        name="reviewer",
        llm_config={"config_list": config_list},
        system_message="""
        你是一个软件审核人员，能够阅读Python代码和JSON结构的文件，
        你的任务是发现代码的问题和检查JSON的结构是否合规
        """,
    )

    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        is_termination_msg=lambda x: x.get(
            "content", "").find("TERMINATE") >= 0,
        code_execution_config=False
    )

    user_proxy.register_nested_chats(
        [{"recipient": reviewer, "message": reflection_message,
            "summary_method": "last_msg", "max_turns": 1}],
        trigger=programer,
    )
    return user_proxy, programer


user_proxy, programer = init_agents()


def chat_with_agent(query: str, history: list):
    response = user_proxy.initiate_chat(
        recipient=programer, message=query, max_turns=2,
        summary_method="last_msg")
    answer = ""
    for _content in response.chat_history:
        answer = answer + "***\n# To " + _content['role'] + ":\n"
        answer = answer + _content['content'] + "\n"
        yield answer


def chat_bot():
    chatbot = gr.Chatbot(height=600, label='autogen')
    with gr.Blocks(fill_height=True) as demo:
        gr.ChatInterface(
            fn=chat_with_agent,
            chatbot=chatbot,
            fill_height=True
        )
    return demo


if __name__ == "__main__":
    demo = chat_bot()
    demo.launch(server_name="0.0.0.0", server_port=6006)
