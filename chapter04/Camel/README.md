# Camel实践

## 一、大语言模型服务安装配置

```shell
# 获取模型
ollama pull llama3:8b-instruct-fp16
# 修改模型名称为gpt-3.5-turbo
ollama cp llama3:8b-instruct-fp16 gpt-3.5-turbo
ollama rm llama3:8b-instruct-fp16
# 运行模型（模型在http://llm-server:11434/v1提供服务）
ollama run gpt-3.5-turbo
```

## 二、Camel安装

```shell
# 下载源码
git clone https://github.com/camel-ai/camel.git
cd camel
git checkout a42d029
# 建立python3.10虚拟环境并激活
conda create -n camel python=3.10 -y
conda activate camel
# 安装依赖库
pip install -e .[all] --use-pep517 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、Camel配置

```shell
# Windows
set OPENAI_API_KEY=EMPTY
set OPENAI_API_BASE_URL=http://llm-server:11434/v1
# Linux
export OPENAI_API_KEY=EMPTY
export OPENAI_API_BASE_URL=http://llm-server:11434/v1
```

## 四、Camel运行

```shell
# run
python examples/ai_society/role_playing.py
# 汉化
prompt加OUTPUT IN CHINESE
```

