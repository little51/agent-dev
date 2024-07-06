# DB-GPT实践

## 一、大语言模型服务安装配置

```shell
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen:0.5b
ollama pull nomic-embed-text
```

## 二、DB-GPT安装

```shell
# 下载源码
git clone https://github.com/eosphoros-ai/DB-GPT
cd DB-GPT
git checkout 374b6ad
# 创建虚拟环境
conda create -n dbgpt_env python=3.10 -y
conda activate dbgpt_env
# 安装依赖库
pip install -e ".[default]" --use-pep517 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装mysql驱动
pip intall pymysql -i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、配置模型

```shell
cp .env.template  .env
vi .env
# 在文件的结尾处增加以下配置内容
LLM_MODEL=ollama_proxyllm
PROXY_SERVER_URL=http://127.0.0.1:11434
PROXYLLM_BACKEND="qwen:0.5b"
PROXY_API_KEY=not_used
EMBEDDING_MODEL=proxy_ollama
proxy_ollama_proxy_server_url=http://127.0.0.1:11434
proxy_ollama_proxy_backend="nomic-embed-text:latest"
```

## 四、DB-GPT运行

```shell
python dbgpt/app/dbgpt_server.py
```
