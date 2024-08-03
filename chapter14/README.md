# crewAI案例

## 一、安装crewAI

```shell
# 创建虚拟环境
conda create -n crewai python=3.10 -y
# 激活虚拟环境
conda activate crewai
# 安装crewai库
pip install crewai==0.36.0 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装gradio库
pip install gradio==4.37.2 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、大语言模型服务安装配置

```shell
# Ollama
ollama run llama3:8b-instruct-fp16
# vLLM
python -m vllm.entrypoints.openai.api_server \
--model dataroot/models/THUDM/glm-4-9b-chat \
--served-model-name glm-4-9b-chat \
--max-model-len 8192 \
--trust-remote-code \
--disable-log-stats

```

## 三、运行程序

```shell
# 激活虚拟环境
conda activate crewai
# 运行程序
python crewai-sample.py
#测试问题：设计一个AI Agent应用，辅助开发人员完成开发任务
```

