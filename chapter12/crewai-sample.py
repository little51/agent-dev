import os
from crewai import Agent, Task, Crew, Process
from langchain_core.agents import AgentAction
from typing import Generator
from queue import Queue
from threading import Thread
from time import sleep
import gradio as gr

os.environ["OPENAI_API_BASE"] = "http://172.16.62.167:8000/v1"
os.environ["OPENAI_MODEL_NAME"] = "glm-4-9b-chat"
os.environ["OPENAI_API_KEY"] = "EMPTY"


def stream_chat(query: str) -> Generator:
    q = Queue()
    job_done = object()

    def agent_step_callback(step_output):
        for step in step_output:
            if isinstance(step, tuple) and len(step) == 2:
                if isinstance(step[0], AgentAction):
                    if not step[0].tool == "_Exception":
                        q.put("## " + step[0].tool)
                        q.put("### 执行过程")
                        q.put(step[0].log)
                        q.put("### 执行结果")
                        q.put(step[1])

    def init_Crew():
        Systems_Analyst = Agent(
            role="系统分析师",
            goal="按照用户提出的任务，进行需求分析，撰写系统需求报告",
            backstory="""您在一家专业设计企业工作。
                您的专长在于掌握各种专业系统分析的原则。
                您具有需求分析、任务分解等技能。""",
            verbose=False,
            allow_delegation=True,
            step_callback=agent_step_callback,
        )

        Designer = Agent(
            role="系统设计师",
            goal="按照系统分析师撰写的系统需求报告，撰写的系统详细设计说明书",
            backstory="""您在一家专业设计企业工作。
                您的专长在于掌握各种专业系统的设计原则。
                您具有系统模块设计、数据计算、公式推导等技能。""",
            verbose=False,
            allow_delegation=True,
            step_callback=agent_step_callback,
        )

        Systems_Analyst_task = Task(
            description=query,
            expected_output="系统需求报告，OUT IN CHINESE",
            agent=Systems_Analyst,
        )

        Designer_task = Task(
            description=query,
            expected_output="系统详细设计说明书，OUT IN CHINESE",
            agent=Designer,
        )

        crew = Crew(
            agents=[Systems_Analyst, Designer],
            tasks=[Systems_Analyst_task, Designer_task],
            verbose=1,
            process=Process.sequential,
            max_iter=5,
        )
        return crew

    def start_Task():
        crew = init_Crew()
        try:
            result = crew.kickoff()
            q.put("## 完成结果")
            q.put(result)
        except Exception as e:
            q.put("## 系统发生异常")
            q.put(str(e))
            pass
        q.put(job_done)

    t = Thread(target=start_Task)
    t.start()
    sleep(1)
    content = ""
    while True:
        try:
            next_token = q.get(True, timeout=1)
            if next_token is job_done:
                break
            content += "\n" + next_token
            yield next_token, content
        except KeyboardInterrupt:
            exit()
        except:
            continue


def ask_from_crew(query: str, history: list):
    for next_token, content in stream_chat(query):
        yield (content)


def chat_bot():
    chatbot = gr.Chatbot(height=600, label="crewAI")
    with gr.Blocks(fill_height=True) as demo:
        gr.ChatInterface(
            fn=ask_from_crew,
            chatbot=chatbot,
            fill_height=True)
    return demo


if __name__ == "__main__":
    demo = chat_bot()
    demo.launch(server_name="0.0.0.0", server_port=6006)
