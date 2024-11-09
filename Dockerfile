# 使用官方的Python基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 将 requirements.txt 文件复制到工作目录中
COPY requirements.txt .

# 安装依赖库
RUN pip install --no-cache-dir -r requirements.txt

# 将项目中的所有文件复制到工作目录中
COPY . .

# 设置启动命令
CMD ["python", "main.py"]