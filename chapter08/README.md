# GLM-4 Function-calling应用开发

## 一、创建虚拟环境

```shell
# 创建虚拟环境
conda create -n functioncalling python=3.10 -y
# 激活虚拟环境
conda activate functioncalling
# 安装依赖库openai
pip install openai==1.35.12 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装依赖库sympy
pip install sympy==1.13.1 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 降级httpx
pip install httpx==0.27.2 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、大语言模型服务安装配置

```shell
# Ollama
ollama run glm4
# openai_api_server
MODEL_PATH=dataroot/models/THUDM/glm-4-9b-chat \
EMBEDDING_PATH=dataroot/models/BAAI/bge-m3 \
python openai_api_server.py
```

## 三、运行程序

```shell
conda activate functioncalling
python glm4-functioncalling.py
```
