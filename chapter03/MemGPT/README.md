# MemGPT应用

## 1、大语言模型服务安装配置

### （1）建立虚拟环境

```shell
# 创建虚拟环境
conda create -n vllm python=3.10 -y
# 激活虚拟环境
conda activate vllm
# 安装vllm及其他依赖库
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
# dataroot/models/THUDM/glm-4-9b-chat
python model_download.py --e --repo_id THUDM/glm-4-9b-chat \
--token YPY8KHDQ2NAHQ2SG
```

### （3）运行API服务

```shell
# 使用vLLM的api_server装载模型
python -m vllm.entrypoints.openai.api_server \
--model dataroot/models/THUDM/glm-4-9b-chat \
--served-model-name glm-4-9b-chat \
--max-model-len 8192 \
--trust-remote-code
```

## 2、MemGPT安装配置  

### （1）建立虚拟环境

```shell
# 创建虚拟环境
conda create -n memgpt python=3.10 -y
# 激活虚拟环境
conda activate memgpt
# 安装pymemgpt
pip install 'pymemgpt[local]' -i https://pypi.mirrors.ustc.edu.cn/simple
```

### （2）下载向量模型

```shell
# 建立工作目录
mkdir memgpt
# 切换到工作目录
cd memgpt
# 下载模型
wget https://e.aliendao.cn/model_download.py
python model_download.py --e \
--repo_id BAAI/bge-small-en-v1.5 \
--token YPY8KHDQ2NAHQ2SG
# 移动模型文件到./BAAI/bge-small-en-v1.5
# 建目录
mkdir -p BAAI/bge-small-en-v1.5
# 批量复制
cp -R ./dataroot/models/BAAI/bge-small-en-v1.5/* \
./BAAI/bge-small-en-v1.5/
# 删除原目录
rm -fr ./dataroot/models/BAAI
```

## 3、AutoGPT智体应用

### （1）配置

```shell
# 执行以下命令进行配置
memgpt configure
# 以下为选项
Select LLM inference provider: local
Select LLM backend: vllm
Enter default endpoint: http://server-dev:8000
Is your LLM endpoint authenticated? N
Enter HuggingFace model tag: glm-4-9b-chat
Select default model wrapper: chatml
Select your model's context window: 8192
Select embedding provider: local
Select storage backend for archival data: chroma
Select chroma backend: persistent
Select storage backend for recall data:sqlite
# 如果选用vllm做为LLM backend，配置时先不要开启LLM服务
# 否则调用到vllm的/v1/models时，memgpt会报错
# 如果需要重新配置，请删除~/.memgpt目录后重新配置
rm -fr ~/.memgpt/
memgpt configure
```

### （2）运行

```shell
memgpt run --agent agent_test
# 如果需要更改LLM服务地址，增加以下参数
--model-endpoint 新URL
https://memgpt.readme.io/docs/local_llm
```

