# 基于Langchain的应用开发

## 一、安装Langchain

```shell
# 创建虚拟环境
conda create -n langchain python=3.10 -y
# 激活虚拟环境
conda activate langchain
# 安装依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、大语言模型服务安装配置

### （1）创建vLLM虚拟环境

```shell
# 创建虚拟环境
conda create -n vllm python=3.10 -y
# 源活虚拟环境
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
# dataroot/models/THUDM/glm-4-9b-chat 
python model_download.py --e \
--repo_id THUDM/glm-4-9b-chat \
--token YPY8KHDQ2NAHQ2SG
```

### （3）运行API服务

```shell
python -m vllm.entrypoints.openai.api_server \
--model \
dataroot/models/THUDM/glm-4-9b-chat \
--served-model-name glm-4-9b-chat \
--trust-remote-code \
--disable-log-stats
```

## 三、运行程序

```shell
# 激活虚拟环境
conda activate langchain
# 运行程序
python langchain-plan-execute.py
# 测试问题：圆周率的概念，圆周率保留到小数点后6位是多少？它的2次方是多少？
```


