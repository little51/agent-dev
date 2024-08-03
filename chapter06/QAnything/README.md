# QAnything实践

## 一、大语言模型服务安装配置

```shell
ollama run llama3
```

## 二、安装QAnything

```shell
# 创建虚拟环境
conda create -n qanything-python python=3.10 -y
# 激活虚拟环境
conda activate qanything-python
# clone源码
git clone -b qanything-python https://github.com/little51/QAnything.git
# 切换到源码目录
cd QAnything
# 安装依赖库
pip install -e . -i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、OCR适配GPU

```shell
# 如果OCR服务使用cuda12和gpu,则执行以下步骤
# 卸载可能已安装的onnxruntime-cpu版
pip uninstall onnxruntime -y
# 卸载可能已安装的旧版onnxruntime-gpu版
pip uninstall onnxruntime-gpu -y
# 安装onnxruntime-gpu
pip install onnxruntime-gpu \
--extra-index-url \
https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
```

## 四、QAnything配置

```shell
vi scripts/run_for_openai_api_with_cpu_in_Linux_or_WSL.sh
# 第一处修改：https://api.openai.com/v1换成http://server-dev:11434/v1
# 第二处修改：gpt-3.5-turbo-1106换成llama3
```

## 五、QAnything运行
```shell
bash scripts/run_for_openai_api_with_cpu_in_Linux_or_WSL.sh
# 在浏览器访问：http://server-dev:8777/qanything/
```

