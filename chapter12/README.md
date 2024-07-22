# crewAI案例

## 一、安装crewAI

```shell
# 创建虚拟环境
conda create -n crewai python=3.10 -y
# 激活虚拟环境
conda activate crewai
# 安装依赖库
pip install crewai 'crewai[tools]' \
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
conda activate crewai
python crewai-sample.py
```





https://github.com/gradio-app/gradio/issues/5345