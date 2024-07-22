import os
from crewai import Agent, Task, Crew, Process
from langchain_core.agents import AgentAction
from typing import Generator
from queue import Queue
from threading import Thread
from time import sleep

os.environ["OPENAI_API_BASE"] = "http://172.16.62.167:8000/v1"
os.environ["OPENAI_MODEL_NAME"] = "glm-4-9b-chat"
os.environ["OPENAI_API_KEY"] = "EMPTY"


def stream_chat(message) -> Generator:
    q = Queue()
    job_done = object()

    def agent_step_callback(step_output):
        for step in step_output:
            if isinstance(step, tuple) and len(step) == 2:
                if isinstance(step[0], AgentAction):
                    q.put("### " + step[0].tool)
                    q.put("## step")
                    q.put(step[0].log)
                    q.put("## result")
                    q.put(step[1])

    def init_Crew():
        Designer = Agent(
            role="系统设计师",
            goal="按照系统分析师的撰写的需求说明书，进行系统设计，形成系统详细设计说明书",
            backstory="""您在一家专业设计企业工作。
                您的专长在于掌握各种专业系统的设计原则。
                您具有系统模块设计、数据计算等技能。""",
            verbose=False,
            allow_delegation=True,
            step_callback=agent_step_callback,
        )

        Quality_controler = Agent(
            role="质量控制师",
            goal="按照系统设计师撰写的系统详细设计说明书，进行质量控制，形成系统设计评估报告",
            backstory="""您在一家专业设计企业工作。
                您的专长在于掌握各种专业系统的质量控制原则。
                您具有系统质量控制、数据计算核对等技能。""",
            verbose=False,
            allow_delegation=True,
            step_callback=agent_step_callback,
        )

        System_Analyst_task = Task(
            description=message,
            expected_output="完整的需求说明书，OUT IN CHINESE",
            agent=System_Analyst,
        )

        Designer_task = Task(
            description=message,
            expected_output="完整的系统详细设计说明书，OUT IN CHINESE",
            agent=Designer,
        )

        Quality_controler_task = Task(
            description=message,
            expected_output="完整的系统质量评估报告，OUT IN CHINESE",
            agent=Quality_controler,
        )

        crew = Crew(
            agents=[System_Analyst, Designer, Quality_controler],
            tasks=[System_Analyst_task, Designer_task, Quality_controler_task],
            verbose=1,
            process=Process.sequential,
            max_iter=1,
        )
        return crew

    def kickoff_Crew():
        crew = init_Crew()
        result = crew.kickoff()
        q.put(result)
        q.put(job_done)

    t = Thread(target=kickoff_Crew)
    t.start()
    content = ""
    sleep(1)
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


def ask_from_crew(message, history):
    for next_token, content in stream_chat(message):
        print("######################")
        print(content)
        print("######################")
        # yield(content)


if __name__ == "__main__":
    message = """按以下已知需求设计一款专用变压器，要求有计算过程和公式：
            50Hz250W变压器，输入电压Vin=115V；输出电压Vo=115V；输出电流Io=2.17A；
            输出功率Po=250W；频率f=50Hz；效率ȵ=95%；电压调整率Ƌ=5%；温升目标Tu=30k
            """
    ask_from_crew(message, [])
