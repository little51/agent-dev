# QAnything实践

## 一、大语言模型服务安装配置

### 1、安装ollama
```shell
curl -fsSL https://ollama.com/install.sh | sh
```

### 2、运行量化模型

```shell
ollama run llama3
# 模型可从https://ollama.com/library选取
```

### 3、查看日志

```shell
# 另开一个窗口
journalctl -u ollama -f
```

## 二、安装QAnything

```shell
conda create -n qanything-python python=3.10 -y
conda activate qanything-python
git clone -b qanything-python https://github.com/little51/QAnything.git
cd QAnything
pip install -e . -i https://pypi.mirrors.ustc.edu.cn/simple
```

## 三、OCR适配GPU

```shell
# 如果OCR服务使用cuda12和gpu,则执行下一步
pip uninstall onnxruntime -y
pip uninstall onnxruntime-gpu -y
pip install onnxruntime-gpu \
--extra-index-url \
https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
```

## 四、QAnything配置

```shell
vi scripts/run_for_openai_api_with_cpu_in_Linux_or_WSL.sh
# 第一处修改：https://api.openai.com/v1换成http://localhost:11434/v1
# 第二处修改：gpt-3.5-turbo-1106换成llama3
```

## 五、QAnything运行
```shell
bash scripts/run_for_openai_api_with_cpu_in_Linux_or_WSL.sh
# 在浏览器访问：http://主机ip地址:8777/qanything/
```

