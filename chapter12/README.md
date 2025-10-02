# 基于Autogen的应用开发

## 一、安装Autogen

```shell
# 创建虚拟环境
conda create -n autogen python=3.10 -y
# 激活虚拟环境
conda activate autogen
# 安装依赖库ag2
pip install ag2==0.2.18 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装依赖库gradio
pip install gradio==4.37.2 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、大语言模型服务安装配置

```shell
ollama run llama3:8b-instruct-fp16
```

## 三、运行程序

```shell
# 激活虚拟环境
conda activate autogen
# 运行程序
python autogen-sample.py
# 测试问题：生成格式为：{"instruction":"指令","input":"","output":"指令的答案"}的10条人工智能训练集，并进行JSON格式校验
```
