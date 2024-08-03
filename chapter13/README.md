# LlamaIndex案例

## 一、安装LlamaIndex

```shell
# 创建虚拟环境
conda create -n llamaindex python=3.10 -y
# 激活虚拟环境
conda activate llamaindex
# 安装依赖库llama_index
pip install llama_index==0.10.53 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装依赖库llama-index-embeddings-huggingface
pip install llama-index-embeddings-huggingface==0.2.2 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、大语言模型服务安装配置

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载BAAI/bge-small-en-v1.5
# 下载后的模型文件保存在dataroot/models/BAAI/bge-small-en-v1.5
python model_download.py --e \
--repo_id BAAI/bge-small-en-v1.5 \
--token YPY8KHDQ2NAHQ2SG
```

## 三、运行程序

```shell
# 激活虚拟环境
conda activate llamaindex
# 运行程序
python llamaindex-sample.py
# 测试问题：LlamaIndex案例
```

