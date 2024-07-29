# CogVLM2案例

## 一、安装虚拟环境

```shell
# 1、创建虚拟环境
conda create -n cogvlm2 python=3.10 -y
# 2、激活虚拟环境
conda activate cogvlm2
# 3、安装依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、下载模型

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载THUDM/cogvlm2-llama3-chinese-chat-19B-int4模型
python model_download.py --e \
--repo_id THUDM/cogvlm2-llama3-chinese-chat-19B-int4 \
--token YPY8KHDQ2NAHQ2SG
# 下载shibing624/text2vec-base-chinese模型
python model_download.py --e \
--repo_id shibing624/text2vec-base-chinese \
--token YPY8KHDQ2NAHQ2SG
```

## 三、运行程序

```shell
conda activate cogvlm2
python cogvlm2_chat.py
python image_search.py
# 访问 http://172.16.62.167:7860/
```

