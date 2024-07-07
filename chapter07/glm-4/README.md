# GLM-4

## 一、下载代码

```shell
git clone https://github.com/THUDM/GLM-4.git
cd GLM-4
git checkout 468a56e
```

## 二、建立虚拟环境

```shell
conda create -n glm4 python=3.10 -y
conda activate glm4
pip install -r basic_demo/requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、模型下载

```shell
wget https://e.aliendao.cn/model_download.py
# 下载大语言模型到以下目录
# dataroot/models/THUDM/glm-4-9b-chat
python model_download.py --e \
--repo_id THUDM/glm-4-9b-chat \
--token YPY8KHDQ2NAHQ2SG
# 下载向量模型到以下目录
# dataroot/models/BAAI/bge-m3
python model_download.py --e \
--repo_id BAAI/bge-m3 \
--token YPY8KHDQ2NAHQ2SG
```

## 四、运行Chat应用

```shell
python glm4-gradio.py
```

## 五、运行api_server

```shell
MODEL_PATH=dataroot/models/THUDM/glm-4-9b-chat \
EMBEDDING_PATH=dataroot/models/BAAI/bge-m3 \
python openai_api_server.py
```

