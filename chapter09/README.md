# 基于Agentscope的应用开发

## 一、安装Agentscope

```shell
# 创建虚拟环境
conda create -n agentscope python=3.10 -y
# 激活虚拟环境
conda activate agentscope
# 安装依赖库
pip install agentscope==0.0.6a2 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、大语言模型服务安装配置

### （1）建立vLLM虚拟环境

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
--max-model-len 8192 \
--trust-remote-code \
--disable-log-stats
```

## 三、运行程序

```shell
# 激活虚拟环境
conda activate agentscope
# 运行程序
python agentscope-sample.py
# 测试问题1
使用python编程，实现递归列出当前目录下的所有文件，包含子目录，并执行程序
# 测试问题2
使用python编程，实现随机生成10个100以内的数字，并进行从小到大排序，并执行程序
```


