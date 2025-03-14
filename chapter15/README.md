# 基于Qwen-Agent的应用开发


## 一、Qwen-VL服务安装配置

```shell
# 1、获取服务代码
git clone https://github.com/little51/agent-dev
# 切换到源码目录
cd agent-dev/chapter15
# 2、创建虚拟环境
conda create -n qwen-vl python=3.10 -y
# 3、激活虚拟环境
conda activate qwen-vl
# 4、安装依赖库
pip install -r requirements-openai-api.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 5、下载Qwen-VL-Chat模型
# （1）获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# （2）下载模型到dataroot/models/Qwen/Qwen-VL-Chat
python model_download.py --e --repo_id Qwen/Qwen-VL-Chat \
--token YPY8KHDQ2NAHQ2SG
# 6、运行Qwen-VL服务\
CUDA_VISIBLE_DEVICES=0 python qwenvl-openai-api.py \
-c dataroot/models/Qwen/Qwen-VL-Chat \
--server-name 0.0.0.0
```


## 二、Qwen-Agent环境安装

```shell
# 1、创建虚拟环境
conda create -n qwen-agent python=3.10 -y
# 2、激活虚拟环境
conda activate qwen-agent
# 3、安装依赖库
# （1）安装qwen-agent
pip install qwen-agent==0.0.6 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# （2）安装modelscope-studio
pip install modelscope-studio==0.4.0 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# （3）安装gradio
pip install gradio==4.37.2 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、运行程序

```shell
# 激活虚拟环境
conda activate qwen-agent
# 运行程序
python qwen-agent-sample.py
# 测试
# 访问：http://server-dev:7860/
# 输入
# 文本：识别图片中的方程组
# 图片：test1.png 或 test2.png
```
