# 使用官方Node.js运行时作为父镜像
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/node:22-alpine AS build-stage

# 设置工作目录
WORKDIR /usr/src/app

# 安装依赖项
COPY package*.json ./
RUN npm install --registry=https://registry.npmmirror.com && npm cache clean --force

# 复制项目文件并构建
COPY . .
RUN npm run build

# 使用Nginx服务静态文件
FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/nginx:1.25-alpine as production-stage

# 复制自定义Nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制构建产物
COPY --from=build-stage /usr/src/app/dist /usr/share/nginx/html

# 优化Nginx配置
RUN echo "\n# Additional optimizations" >> /etc/nginx/nginx.conf && \
    echo "worker_processes auto;" >> /etc/nginx/nginx.conf && \
    echo "events {" >> /etc/nginx/nginx.conf && \
    echo "    worker_connections 1024;" >> /etc/nginx/nginx.conf && \
    echo "    multi_accept on;" >> /etc/nginx/nginx.conf && \
    echo "}" >> /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 8080

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
