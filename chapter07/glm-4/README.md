# GLM-4

## 一、下载源码

```shell
git clone https://github.com/THUDM/GLM-4.git
cd GLM-4
git checkout 468a56e
```

## 二、建立虚拟环境

```shell
conda create -n glm4 python=3.10 -y
conda activate glm4
# 安装基础依赖库
pip install -r basic_demo/requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装vllm库
pip install vllm==0.5.1 \
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

## 六、微调

### 1、微调数据准备

```shell
python convert_data.py
```

### 2、微调环境准备

```shell
# 修改finetune_demo/requirements.txt文件
# 1、注释掉datasets>2.20.0
#datasets>2.20.0
# 2、增加一行
transformers==4.40.2
# 安装依赖库
pip install -r finetune_demo/requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

### 3、微调过程

```shell
OMP_NUM_THREADS=1 torchrun --standalone \
--nnodes=1 --nproc_per_node=2  \
finetune_demo/finetune.py  data/ \
dataroot/models/THUDM/glm-4-9b-chat \
finetune_demo/configs/lora.yaml 
```

### 4、微调模型测试

```shell
# glm4-gradio.py中装载模型换成
load_model_and_tokenizer_lora("output/checkpoint-500")
# 运行
python glm4-gradio.py
```

