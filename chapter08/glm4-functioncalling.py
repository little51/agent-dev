import json
from openai import OpenAI
import sympy as sp

client = OpenAI(
    base_url="http://172.16.62.167:8000/v1",
    api_key="EMPTY"
)

model_name = "glm-4-9b-chat"

tools = [
    {
        "type": "function",
        "function": {
            "name": "solve",
            "description": "求解方程",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbols": {
                        "description": "符号",
                        "type": "string"
                    },
                    "equation": {
                        "description": "方程",
                        "type": "string"
                    }
                },
                "required": ["symbols", "equation"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "计算大数字乘积",
            "parameters": {
                "type": "object",
                "properties": {
                    "multiplicand": {
                        "description": "被乘数",
                        "type": "float"
                    },
                    "multiplier": {
                        "description": "乘数",
                        "type": "float",
                    }
                },
                "required": ["multiplicand", "multiplier"]
            },
        }
    },
]


def solve(symbols: str, equation: str):
    print("function: {} \nsymbols: {} \nequation: {}".format(
        'solve', symbols, equation))
    x = sp.symbols('x')
    _equation = sp.sympify(equation.split('=')[0])
    _equation = sp.Eq(_equation, 0)
    solutions = sp.solve(_equation, x)
    result = {"symbols": symbols, "equation": equation,
              "solutions": str(solutions)}
    return result


def multiply(multiplicand: float, multiplier: float):
    print(
        "function: {} \nmultiplicand: {} \nmultiplier: {}".format(
            'multiply', multiplicand, multiplier))
    result = {"value": multiplicand * multiplier}
    return result


def parse_function_calling(model_response, messages):
    if model_response.choices[0].message.tool_calls:
        tool_call = model_response.choices[0].message.tool_calls[0]
        args = tool_call.function.arguments
        if tool_call.function.name == "solve":
            function_result = solve(**json.loads(args))
        elif tool_call.function.name == "multiply":
            function_result = multiply(**json.loads(args))
        else:
            function_result = {}
        messages.append({
            "role": "tool",
            "content": f"{json.dumps(function_result)}",
            "tool_call_id": tool_call.id
        })
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
            temperature=0.9
        )
        return response.choices[0].message.content
    else:
        return model_response.choices[0].message.content


def llm_call(message: str):
    messages = []
    messages.append({"role": "system", "content":
                     "你是一个精通数学计算的人工智能助理"})
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.9
    )
    messages.append(response.choices[0].message.model_dump())
    return parse_function_calling(response, messages)


if __name__ == "__main__":
    print("============求解方程============")
    print(llm_call("求方程 x**2 - 4 = 0 的解"))
    print("============大数相乘============")
    print(llm_call("计算2024乘2025的积"))
    print("============其他问题============")
    print(llm_call("介绍一下sympy库的功能"))
    print("============传统方法============")
    print(llm_call("计算2024乘2025的积，注意，" +
                   "请不要使用大模型的function-calling"))
