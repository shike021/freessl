# 使用官方Node.js运行时作为父镜像
FROM node:16 as build-stage

# 设置工作目录
WORKDIR /usr/src/app

# 安装依赖项
COPY package*.json ./
RUN npm install

# 复制项目文件并构建
COPY . .
RUN npm run build

# 使用Nginx服务静态文件
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /usr/src/app/dist /usr/share/nginx/html
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
