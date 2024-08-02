# BabyAGI实践

## 1、大语言模型服务安装配置

### （1）建立虚拟环境

```shell
# 创建虚拟环境
conda create -n vllm python=3.10 -y
# 激活虚拟环境
conda activate vllm
# 安装vllm及依赖库
pip install vllm==0.4.3 modelscope==1.15.0 numpy==1.24.2 \
sentence-transformers==3.0.1 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 验证是否安装成功
python -c "import torch; print(torch.cuda.is_available())"
```

### （2）下载模型

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载模型大语言模型
# 模型下载到以下目录：dataroot/models/THUDM/glm-4-9b-chat
python model_download.py --e \
--repo_id THUDM/glm-4-9b-chat \
--token YPY8KHDQ2NAHQ2SG
# 下载向量模型
# 模型下载到以下目录：dataroot/models/BAAI/bge-small-en-v1.5
python model_download.py --e \
--repo_id BAAI/bge-small-en-v1.5  \
--token YPY8KHDQ2NAHQ2SG
```

### （3）运行API服务

```shell
# 使用vllm改进版的api_server装载模型
# 支持/v1/embeddings
EMBEDDING_PATH=dataroot/models/BAAI/bge-small-en-v1.5 \
python api_server.py \
--model dataroot/models/THUDM/glm-4-9b-chat \
--served-model-name glm-4-9b-chat \
--max-model-len 8192 \
--trust-remote-code
```

## 2、BabyAGI安装

```shell
# 下载源码
git clone https://github.com/git-cloner/babyagi.git
# 切换到源码目录
cd babyagi
# 建立虚拟环境
conda create -n babyagi python=3.10 -y
# 激活虚拟环境
conda activate babyagi
# 确认是否安装了编译环境
g++ --version
# 如果未安装编译环境，则用以下命令安装
sudo apt-get install build-essential
# 安装依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 3、BabyAGI配置

```shell
cp .env.example .env
vi .env
# 修改以下三个大模型相关参数
LLM_MODEL=glm-4-9b-chat
OPENAI_API_KEY= EMPTY
OPENAI_API_BASE= http://server-dev:8000/v1
# 目标任务在OBJECTIVE参数中设置
```

## 4、BabyAGI运行

```shell
TABLE_NAME=test python babyagi.py
```

