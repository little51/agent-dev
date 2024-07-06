# AutoGPT应用

## 1、大语言模型服务安装配置

### （1）建立虚拟环境

```shell
# 创建虚拟环境
conda create -n vllm python=3.10 -y
conda activate vllm
# 安装vllm及依赖库
pip install vllm==0.4.3 modelscope==1.15.0 numpy==1.24.2 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 验证是否安装成功
python -c "import torch; print(torch.cuda.is_available())"
```

### （2）下载模型

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载模型到以下目录
# dataroot/models/Trelis/Meta-Llama-3-8B-Instruct-function-calling
python model_download.py --e \
--repo_id Trelis/Meta-Llama-3-8B-Instruct-function-calling \
--token YPY8KHDQ2NAHQ2SG
```

### （3）运行API服务

```shell
# 使用vLLM的api_server装载模型
# 指定模型的别名为gpt-3.5-turbo，在AutoGPT配置LLM时
# 就将本模型服务当作gpt-3.5-turbo的兼容服务来使用
python -m vllm.entrypoints.openai.api_server \
--model \
dataroot/models/Trelis/Meta-Llama-3-8B-Instruct-function-calling \
--served-model-name gpt-3.5-turbo
```

## 2、AutoGPT安装配置

### （1）创建虚拟环境

```shell
conda create -n autogpt python=3.10 -y
conda activate autogpt
```

### （2）下载源码

```shell
git clone https://github.com/Significant-Gravitas/AutoGPT
cd AutoGPT
git checkout 227cf41
```

### （3）安装依赖库

```shell
# 安装基础依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装forge组件
cd forge
pip install -e . -i https://pypi.mirrors.ustc.edu.cn/simple
cd ..
```

## 3、AutoGPT智体应用

### （1）配置

```shell
cp ./autogpt/.env.template ./autogpt/.env
vi ./autogpt/.env
# 配置OPENAI_API_KEY，满足AutoGPT对key的校验规则
OPENAI_API_KEY=sk-proj-000000000000000000000000000000000000000000000000
# 配置OpenAI兼容接口服务的URL
OPENAI_API_BASE_URL=http://llm-server:8000/v1
# 禁用web搜索命令
DISABLED_COMMANDS=web_search
```

### （2）运行

```shell
cd autogpt
python -m autogpt run --skip-news
```

