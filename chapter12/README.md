# crewAI案例

## 一、安装crewAI

```shell
# 创建虚拟环境
conda create -n crewai python=3.10 -y
# 激活虚拟环境
conda activate crewai
# 安装crewai库
pip install crewai==0.36.0 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装gradio库
pip install gradio==4.37.2 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、大语言模型服务安装配置

```shell
ollama run llama3:8b-instruct-fp16
```

## 三、运行程序

```shell
conda activate crewai
python crewai-sample.py
#测试问题：按以下已知需求设计一款专用变压器，完成详尽的系统设计说明书，要求有计算过程和公式：50Hz250W变压器，输入电压Vin=115V；输出电压Vo=115V；输出电流Io=2.17A；输出功率Po=250W；频率f=50Hz；效率ȵ=95%；电压调整率Ƌ=5%；温升目标Tu=30k 
```

