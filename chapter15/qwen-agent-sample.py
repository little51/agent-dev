import copy
from typing import Dict, Iterator, List, Optional, Union
from qwen_agent import Agent
from qwen_agent.tools import BaseTool
from qwen_agent.agents import Assistant
from qwen_agent.llm import BaseChatModel
from qwen_agent.llm.schema import Message
from qwen_agent.gui import WebUI

llm_config = {'model': 'qwenvl_oai',
              'model_server': 'http://127.0.0.1:8000/v1',
              'api_key': 'EMPTY'}


class Visual_solve_equations(Agent):
    def __init__(self,
                 function_list: Optional[
                     List[Union[str,
                                Dict, BaseTool]]] = None,
                 llm: Optional[Union[Dict, BaseChatModel]] = None):
        super().__init__(llm=llm)
        # 定义图片识别Agent
        self.image_agent = Assistant(llm=self.llm)
        # 定义数学计算Agent
        self.math_agent = Assistant(
            llm=self.llm,
            system_message='你扮演一个学生，' +
            '参考你学过的数学知识进行计算')

    def _run(self, messages: List[Message],
             lang: str = 'zh', **kwargs) -> Iterator[List[Message]]:
        # 校验WebUI传入的参数，必须为list，且包含图片
        assert isinstance(messages[-1]['content'], list)
        assert any([item.image for item in messages[-1]['content']]
                   ), '这个智体应用需要输入图片'
        response = []
        # 第1个Agent，将图片内容识别成文本
        new_messages = copy.deepcopy(messages)
        new_messages[-1].content[0]['text'] = str(
            [{"text": new_messages[-1].content[0]['text']}, {
                "image": new_messages[-1].content[1]['image'].
                replace("file://", "")}])
        for rsp in self.image_agent.run(new_messages,
                                        lang=lang, **kwargs):
            yield rsp
        # 第2个Agen，求解文本中的数学问题
        response = rsp
        new_messages.extend(rsp)
        new_messages.append(Message('user',
                                    '根据以上文本内容求解数学题'))
        for rsp in self.math_agent.run(new_messages,
                                       lang=lang, **kwargs):
            yield response + rsp


def app_gui():
    bot = Visual_solve_equations(llm=llm_config)
    WebUI(bot).run(server_name="0.0.0.0")


if __name__ == '__main__':
    app_gui()
