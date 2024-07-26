# LangGraph案例

## 一、创建虚拟环境

```shell
# 创建虚拟环境
conda create -n langgraph python=3.10 -y
# 激活虚拟环境
conda activate langgraph
# 安装依赖库langgraph
pip install langgraph==0.1.6 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装依赖库httpx
pip install httpx==0.27.0 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装依赖库langchain-openai
pip install langchain-openai==0.1.17 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、大语言模型服务安装配置

```shell
# openai_api_server
MODEL_PATH=dataroot/models/THUDM/glm-4-9b-chat \
EMBEDDING_PATH=dataroot/models/BAAI/bge-m3 \
python openai_api_server.py
```

## 三、运行程序

```shell
conda activate langgraph
python langgraph-sample.py
```
