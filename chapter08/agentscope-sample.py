import sys
import io
import subprocess
import agentscope
from agentscope.agents import UserAgent
from agentscope.agents.react_agent import ReActAgent
from agentscope.service import (
    ServiceToolkit,
    ServiceResponse,
    ServiceExecStatus,
)

MODEL_CONFIG_NAME = "openai_chat"

MODEL_CONFIG = {
    "config_name": MODEL_CONFIG_NAME,
    "model_type": "openai_chat",
    "model_name": "glm-4-9b-chat",
    "api_key": "EMPTY",
    "organization": "EMPTY"
}


def execute_python_code(code: str) -> ServiceResponse:
    with open("generated-code.py", 'w', encoding='utf-8') as file:
        file.write(code)
    result = subprocess.run(['python', 'generated-code.py'],
                            stdout=subprocess.PIPE, text=True)
    if result.returncode == 0:
        output = result.stdout
        status = ServiceExecStatus.SUCCESS
    else:
        output = result.stderr
        status = ServiceExecStatus.ERROR
    return ServiceResponse(status, output)


def init_toolkit():
    service_toolkit = ServiceToolkit()
    service_toolkit.add(execute_python_code)
    agentscope.init(
        model_configs=MODEL_CONFIG,
        project="ReActAgent",
    )
    return service_toolkit


def init_ReActAgent():
    reActAgent = ReActAgent(
        name="assistant",
        model_config_name=MODEL_CONFIG_NAME,
        verbose=True,
        service_toolkit=init_toolkit(),
    )
    return reActAgent


def init_UserAgent():
    userAgent = UserAgent(name="User")
    return userAgent


if __name__ == "__main__":
    reActAgent = init_ReActAgent()
    userAgent = init_UserAgent()
    user_response = userAgent(None)
    for _ in range(3):
        try:
            reActAgent(user_response)
            break
        except:
            pass
