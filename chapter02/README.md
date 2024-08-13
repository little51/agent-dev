# 环境安装

## 一、Agent应用环境安装

### 1、推理卡驱动安装

#### （1）安装编译环境

```shell
# 更新系统
sudo apt update
# 安装g++
sudo apt install g++
# 安装make
sudo apt install make
# 安装新版gcc
sudo apt install gcc-12
# 链接cc命令到新版gcc
sudo ln -sf /usr/bin/gcc-12 /etc/alternatives/cc
```

#### （2）禁用nouveau

```shell
# 编辑blacklist.conf文件
sudo vi /etc/modprobe.d/blacklist.conf
# 结尾处增加以下两行
blacklist nouveau
options nouveau modeset=0
# 保存后退出
# 安装dracut工具
sudo apt install dracut
# 使blacklist.conf的配置修改生效
sudo dracut --force
# 重启系统
sudo reboot
# 验证是否禁用了nouveau，显示为空说明成功禁用
lsmod | grep nouveau
# 停止图形用户界面服务
sudo telinit 3
# 停止GNOME Display Manager服务
sudo service gdm3 stop
```

#### （3）下载安装驱动

```shell
# 网址
https://www.nvidia.com/Download/index.aspx?lang=en-us
# 下载
wget https://cn.download.nvidia.com/XFree86/Linux-x86_64/545.23.06/NVIDIA-Linux-x86_64-545.23.06.run
# 安装
sudo sh ./NVIDIA-Linux-x86_64-545.23.06.run
# 验证
nvidia-smi
```

### 2、CUDA安装

```shell
# 网址
https://developer.nvidia.com/cuda-12-3-0-download-archive
# 下载
wget https://developer.download.nvidia.com/compute/cuda/12.3.0/local_installers/cuda_12.3.0_545.23.06_linux.run
# 安装
sudo sh ./cuda_12.3.0_545.23.06_linux.run
# 增加环境变量
vi ~/.bashrc
# 增加以下两行
export PATH=/usr/local/cuda-12.3/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-12.3/lib64
# 环境变量生效
source ~/.bashrc
# 验证
nvcc -V
```

### 3、Anaconda安装

```shell
# 网址
https://www.anaconda.com/download/success
# 下载
wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
# 安装
sh Anaconda3-2024.02-1-Linux-x86_64.sh
# 验证
# 重连ssh
conda -V
```

### 4、Git安装

```shell
# 安装
sudo apt install git
# 验证
git --version
```

### 5、环境验证

```shell
# 创建虚拟环境
conda create -n test python=3.10 -y
# 激活虚拟环境
conda activate test
# 安装pytorch
pip install torch==2.1.2 -i https://pypi.mirrors.ustc.edu.cn/simple
# 验证
python -c "import torch; print(torch.cuda.is_available())"
# 退出虚拟环境
conda deactivate
```

## 二、大语言模型服务搭建

### 1、Ollama

#### （1）安装

```shell
# 安装
curl -fsSL https://ollama.com/install.sh | sh
# 修改服务配置，监听真实IP
sudo vi /etc/systemd/system/ollama.service
# 增加以下配置
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
# 重新加载系统的服务管理器的配置
sudo systemctl daemon-reload
# 重启Ollama服务
sudo systemctl restart ollama
```

#### （2）常用命令

```shell
# 运行模型服务
ollama run 大模型服务名称
# 查看大模型列表
ollama list
# 删除大模型服务
ollama rm 大模型服务名称
# 复制大模型服务
ollama cp 大模型服务名称 新大模型服务名称
# 查看日志
journalctl -u ollama -f
# 非正常结束进程导致ssh连接慢和systemctl执行超时的解决办法
sudo systemctl --force --force reboot
```

#### （3）测试

```shell
curl --location --request POST http://127.0.0.1:11434/v1/chat/completions --header Content-Type: application/json --data-raw "{\"model\": \"llama3\",\"messages\": [{\"role\": \"user\",\"content\": \"你好\"}]}"
```

### 2、vLLM

#### （1）vLLM安装

```shell
# 创建虚拟环境
conda create -n vllm python=3.10 -y
# 激活虚拟环境
conda activate vllm
# 安装vllm及依赖库
pip install vllm==0.4.3 modelscope==1.15.0 numpy==1.24.2 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

#### （2）模型下载

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载Meta-Llama-3-8B-Instruct模型
python model_download.py --e \
--repo_id NousResearch/Meta-Llama-3-8B-Instruct \
--token YPY8KHDQ2NAHQ2SG
```

#### （3）运行OpenAI兼容API服务

```shell
CUDA_VISIBLE_DEVICES=0 \
python -m vllm.entrypoints.openai.api_server \
--model dataroot/models/NousResearch/Meta-Llama-3-8B-Instruct \
--served-model-name llama3 \
--dtype half \
--disable-log-stats
```

#### （4）测试

```shell
curl --location --request POST http://127.0.0.1:8000/v1/chat/completions --header Content-Type: application/json --data-raw "{\"model\": \"llama3\",\"messages\": [{\"role\": \"user\",\"content\": \"你好\"}]}"
```

### 3、GLM-4专用服务

#### （1）虚拟环境安装

```shell
# 下载源码
git clone https://github.com/little51/agent-dev
# 进入服务源码目录
cd agent-dev/chapter07/glm-4
# 创建虚拟环境
conda create -n glm4 python=3.10 -y
# 激活虚拟环境
conda activate glm4
# 安装依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

#### （2）模型下载

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载大语言模型glm-4-9b-chat
python model_download.py --e \
--repo_id THUDM/glm-4-9b-chat \
--token YPY8KHDQ2NAHQ2SG
# 下载向量模型bge-m3
python model_download.py --e \
--repo_id BAAI/bge-m3 \
--token YPY8KHDQ2NAHQ2SG
```

#### （3）运行OpenAI兼容API服务

```shell
MODEL_PATH=dataroot/models/THUDM/glm-4-9b-chat \
EMBEDDING_PATH=dataroot/models/BAAI/bge-m3 \
python openai_api_server.py
```

#### （4）测试

```shell
curl --location --request POST http://127.0.0.1:8000/v1/chat/completions --header Content-Type: application/json --data-raw "{\"model\": \"glm-4-9b-chat\",\"messages\": [{\"role\": \"user\",\"content\": \"你好\"}]}"
```

