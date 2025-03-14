# 辅助开发型：CodeFuse-ChatBot应用

## 一、CodeFuse-ChatBot安装

```shell
# 创建虚拟环境
conda create --name devopsgpt python=3.9 -y
# 激活虚拟环境
conda activate devopsgpt
# clone源码
git clone https://github.com/codefuse-ai/codefuse-chatbot
# 切换到源码目录
cd codefuse-chatbot
# 检出历史版本
git checkout d6932ec
# 安装依赖库
pip install -r requirements.txt --use-pep517 \
-i https://pypi.mirrors.ustc.edu.cn/simple
# 降级streamlit到1.36.0
# 因为这个版本之后，属性experimental_rerun被删除，程序会报错
pip install streamlit==1.36.0  \
-i https://pypi.mirrors.ustc.edu.cn/simple
```

## 二、大语言模型服务安装配置

```shell
# 获取模型下载脚本
wget https://e.aliendao.cn/model_download.py
# 下载Embedding模型到以下目录
# dataroot/models/shibing624/text2vec-base-chinese 
python model_download.py --e \
--repo_id shibing624/text2vec-base-chinese \
--token YPY8KHDQ2NAHQ2SG
# 使用Ollama运行glm4模型
ollama run glm4
```

## 三、CodeFuse-ChatBot配置

```shell
# 复制模型配置文件
cp ./configs/model_config.py.example ./configs/model_config.py
# 复制服务配置文件
cp ./configs/server_config.py.example ./configs/server_config.py
# 在./configs/model_config.py的最后
# 增加大语言模型和Embedding模型的配置
llm_model_dict = {'glm4': {
'local_model_path': '', 
'api_base_url': 'http://server-dev:11434/v1', 'api_key': 'EMPTY'}}
embedding_model_dict = {"text2vec-base": 
"../dataroot/models/shibing624/text2vec-base-chinese"}
```

## 四、CodeFuse-ChatBot运行

```shell
# 切换到examples
cd examples
# 激活虚拟环境
conda activate devopsgpt
# 方式1，无docker环境运行
SANDBOX_DO_REMOTE=false DOCKER_SERVICE=false LLM_MODEL=glm4 \
API_BASE_URL=http://server-dev:11434/v1 python start.py
# 方式2，有docker环境运行
LLM_MODEL=glm4 API_BASE_URL=http://server-dev:11434/v1 \
python start.py
# 在浏览器访问
http://server-dev:8501/
```

## 五、停止服务

```shell
python stop.py或sudo pkill -f -9 python
```

