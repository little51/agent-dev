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


def stream_chat(input_text) -> Generator:
    q = Queue()
    job_done = object()

    def agent_step_callback(step_output):
        for step in step_output:
            if isinstance(step, tuple) and len(step) == 2:
                if isinstance(step[0], AgentAction):
                    print("==========agent step begin==========")
                    # print(step[0].tool)
                    # print(step[0].tool_input)
                    # print(step[0].log)
                    # print(step[1])
                    q.put(step[0].tool)
                    print("==========agent step end============")

    def init_Crew():
        researcher = Agent(
            role="变压器设计师",
            goal="了解电器和变压器设计的前沿发展",
            backstory="""您在一家领先的变压器设计企业工作。
            您的专长在于掌握各种变压器的设计原则。
            您具有剖析复杂数据和提供可操作见解的诀窍。""",
            verbose=False,
            allow_delegation=True,
            step_callback=agent_step_callback,
        )

        writer = Agent(
            role="变压器工艺师",
            goal="了解电器和变压器制造的前沿发展",
            backstory="""您在一家领先的变压器设计企业工作。
            您的专长在于掌握各种变压器的制造工艺原则。
            您具有剖析复杂数据和提供可操作见解的诀窍。""",
            verbose=False,
            allow_delegation=True,
            step_callback=agent_step_callback,
        )

        task1 = Task(
            description="""按以下已知需求设计一款专用变压器，要求有计算过程和公式：
            50Hz250W变压器，输入电压Vin=115V；输出电压Vo=115V；输出电流Io=2.17A；
            输出功率Po=250W；频率f=50Hz；效率ȵ=95%；电压调整率Ƌ=5%；温升目标Tu=30k
            """,
            expected_output="完整的设计报告，要求1000字，OUT IN CHINESE",
            agent=researcher,
        )

        task2 = Task(
            description="""按以下已知需求设计一款专用变压器，并制定制造工艺，要求有计算过程和公式：
            50Hz250W变压器，输入电压Vin=115V；输出电压Vo=115V；输出电流Io=2.17A；
            输出功率Po=250W；频率f=50Hz；效率ȵ=95%；电压调整率Ƌ=5%；温升目标Tu=30k
            """,
            expected_output="完整的设计报告，要求1000字，OUT IN CHINESE",
            agent=writer,
        )

        crew = Crew(
            agents=[researcher, writer],
            tasks=[task1, task2],
            verbose=1,
            process=Process.sequential,
            max_iter=3,
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


def ask_llm(message, history):
    for next_token, content in stream_chat(message):
        print("######################")
        print(content)
        print("######################")
        # yield(content)


if __name__ == "__main__":
    message = """按以下已知需求设计一款专用变压器，要求有计算过程和公式：
            50Hz250W变压器，输入电压Vin=115V；输出电压Vo=115V；输出电流Io=2.17A；
            输出功率Po=250W；频率f=50Hz；效率ȵ=95%；电压调整率Ƌ=5%；温升目标Tu=30k
            """,
    ask_llm("123", [])
