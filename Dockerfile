
# FROM  ghcr.io/rachelos/base-mini:latest as werss-base
FROM  --platform=$BUILDPLATFORM docker.1ms.run/python:3.13.1-slim AS werss-base
#

ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
# ENV PIP_INDEX_URL=https://mirrors.huaweicloud.com/repository/pypi/simple

# 复制Python依赖文件
FROM werss-base
COPY requirements.txt .
# 安装系统依赖
WORKDIR /app
# 复制后端代码
COPY ./config.example.yaml  ./config.yaml
COPY . .
RUN chmod +x start.sh
# 暴露端口
EXPOSE 8001
CMD ["bash", "start.sh"]
# CMD ["sleep", "infinity"]