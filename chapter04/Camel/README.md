# Camel实践

## 一、大语言模型服务安装配置

```shell
# 获取模型
ollama pull llama3:8b-instruct-fp16
# 修改模型名称为gpt-3.5-turbo
ollama cp llama3:8b-instruct-fp16 gpt-3.5-turbo
# 删除原始模型以节省空间
ollama rm llama3:8b-instruct-fp16
# 运行模型（模型将在http://server-dev:11434/v1提供服务）
ollama run gpt-3.5-turbo
```

## 二、Camel安装

```shell
# clone源码
git clone https://github.com/camel-ai/camel.git
# 切换到源码目录
cd camel
# 检出历史版本
git checkout a42d029
# 创建虚拟环境
conda create -n camel python=3.10 -y
# 激活虚拟环境
conda activate camel
# 安装依赖库
pip install -e .[all] --use-pep517 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、Camel配置

```shell
# Windows
set OPENAI_API_KEY=EMPTY
set OPENAI_API_BASE_URL=http://server-dev:11434/v1
# Linux
export OPENAI_API_KEY=EMPTY
export OPENAI_API_BASE_URL=http://server-dev:11434/v1
```

## 四、Camel运行

```shell
# 激活虚拟环境
conda activate camel
# 运行程序
python examples/ai_society/role_playing.py
# 汉化
prompt加OUTPUT IN CHINESE
```

