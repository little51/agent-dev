# DB-GPT实践

## 一、大语言模型服务安装配置

```shell
# 从Ollama镜像库获取qwen-0.5b模型
ollama pull qwen:0.5b
# 从Ollama镜像库获取nomic-embed-text模型
ollama pull nomic-embed-text
```

## 二、DB-GPT安装

```shell
# clone源码
git clone https://github.com/eosphoros-ai/DB-GPT
# 切换到源码目录
cd DB-GPT
# 检出历史版本
git checkout 374b6ad
# 创建虚拟环境
conda create -n dbgpt python=3.10 -y
# 激活虚拟环境
conda activate dbgpt
# 安装依赖库
pip install -e ".[default]" --use-pep517 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装mysql驱动
pip install pymysql==1.1.1 -i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、配置模型

```shell
# 复制配置文件
cp .env.template  .env
# 修改配置文件
vi .env
# 在文件的结尾处增加以下配置内容
LLM_MODEL=ollama_proxyllm
PROXY_SERVER_URL=http://server-dev:11434
PROXYLLM_BACKEND="qwen:0.5b"
PROXY_API_KEY=not_used
EMBEDDING_MODEL=proxy_ollama
proxy_ollama_proxy_server_url=http://server-dev:11434
proxy_ollama_proxy_backend="nomic-embed-text:latest"
```

## 四、DB-GPT运行

```shell
# 激活虚拟环境
conda activate dbgpt
# 运行程序
python dbgpt/app/dbgpt_server.py
```
