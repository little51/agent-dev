# Devika实践

## 一、大语言模型服务安装配置

```shell
ollama run llama3:8b-instruct-fp16
```

## 二、Devika安装

```shell
# 下载源码
git clone https://github.com/stitionai/devika.git
cd devika
git checkout 7a8c980
# 建立python3.10虚拟环境并激活
conda create -n devika python=3.10 -y
conda activate devika
# 安装依赖库
pip install -r requirements.txt \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 安装playwright
playwright install --with-deps \
-i https://pypi.mirrors.ustc.edu.cn/simple
pip install curl-cffi==0.6.4 \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、配置向量模型

```shell
# 句子转向量模型下载
wget https://e.aliendao.cn/model_download.py
python model_download.py \
--repo_id sentence-transformers/all-MiniLM-L6-v2
# 移动模型文件到./sentence-transformers/all-MiniLM-L6-v2
mkdir -p sentence-transformers/all-MiniLM-L6-v2
cp -R ./dataroot/models/sentence-transformers/all-MiniLM-L6-v2/* \
./sentence-transformers/all-MiniLM-L6-v2/
rm -fr ./dataroot
```

## 四、Devika配置

```shell
cp sample.config.toml config.toml
vi config.toml
# 配置API_ENDPOINTS->OLLAMA为http://llm-server:11434
```

## 五、Devika运行

### 1、服务器端

```shell
conda activate devika
python devika.py
```

### 2、客户端

#### （1）Node.js安装

```shell
# 安装 nvm (Node.js版本管理器)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
# 下载安装Node.js (需要重连ssh)
nvm install 20
# 验证安装结果
node -v # 应显示`v20.15.0`
# 验证npm
npm -v # 应显示 `10.7.0`
```

#### （2）安装依赖库

```shell
cd ui
npm i
```

#### （3）运行

```shell
export VITE_API_BASE_URL=http://172.16.62.37:3001
npm start -host
```

