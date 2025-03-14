# 辅助开发型：Devika应用

## 一、大语言模型服务安装配置

```shell
ollama run llama3:8b-instruct-fp16
```

## 二、Devika安装

```shell
# clone源码
git clone https://github.com/stitionai/devika
# 切换到源码目录
cd devika
# 检出历史版本
git checkout 7a8c980
# 创建虚拟环境
conda create -n devika python=3.10 -y
# 激活虚拟环境
conda activate devika
# 安装基础依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装playwright
playwright install --with-deps
# 安装curl-cffi
pip install curl-cffi==0.6.4 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、配置向量模型

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载句子转向量模型
python model_download.py \
--repo_id sentence-transformers/all-MiniLM-L6-v2
# 建立模型目标目录./sentence-transformers/all-MiniLM-L6-v2
mkdir -p sentence-transformers/all-MiniLM-L6-v2
# 批量复制模型文件
cp -R ./dataroot/models/sentence-transformers/all-MiniLM-L6-v2/* \
./sentence-transformers/all-MiniLM-L6-v2/
# 删除下载目录
rm -fr ./dataroot
```

## 四、Devika配置

```shell
# 复制配置文件
cp sample.config.toml config.toml
# 修改配置文件
vi config.toml
# 配置API_ENDPOINTS->OLLAMA为http://server-dev:11434
```

## 五、Devika运行

### 1、服务器端

```shell
# 激活虚拟环境
conda activate devika
# 运行服务程序
python devika.py
```

### 2、客户端

#### （1）Node.js安装

```shell
# 添加Node.js到apt存储库
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
# 安装Node.js
sudo apt update && sudo apt install -y nodejs
# 验证npm（显示Node.js的版本号）
node -v
```

#### （2）安装依赖库

```shell
# 切换到ui目录
cd ui
# 指定npm使用淘宝镜像加速
npm config set registry https://registry.npmmirror.com
# 安装依赖库
npm i
```

#### （3）运行

```shell
# 设置环境变量
export VITE_API_BASE_URL=http://server-dev:3001
# 运行程序
npm start -host
```

