# Llama3应用开发与微调

## 一、Llama3模型部署

### 1、建立虚拟环境

```bash
# 创建虚拟环境
conda create -n llama3 python=3.10 -y
# 激活虚拟环境
conda activate llama3
```

### 2、安装依赖库

```shell
# 建立源码目录
mkdir llama3
# 切换到源码目录
cd llama3
# 安装依赖库(requirements.txt先复制到llama3目录)
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 验证PyTorch
python -c "import torch; print(torch.cuda.is_available())"
```

### 3、下载模型

```bash
# 获取模型下载脚本
wget https://aliendao.cn/model_download.py
# 下载大语言模型到以下目录
# dataroot/models/NousResearch/Meta-Llama-3-8B-Instruct
python model_download.py --e \
--repo_id NousResearch/Meta-Llama-3-8B-Instruct \
--token YPY8KHDQ2NAHQ2SG
```

## 二、Chat应用

```bash
# 激活虚拟环境
conda activate llama3
# 运行程序
python llama3-gradio.py
# 访问http://server-dev:6006/
```
## 三、LLama3服务开发

```bash
# 激活虚拟环境
conda activate llama3
# 运行程序
python llama3-api.py
```

## 四、LLama3微调

```bash
# 微调
CUDA_VISIBLE_DEVICES=0 python llama3-train.py
# 模型合并
python merge_lora_weights.py \
--base_model ./dataroot/models/NousResearch/Meta-Llama-3-8B-Instruct \
--peft_model output/PEFT/model \
--output_dir output/merged/model
# 合并后，就可以把output/merged/model下的模型装载推理
```
