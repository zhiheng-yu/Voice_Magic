# 第一阶段：构建阶段
FROM node:18-alpine AS builder

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制所有前端代码
COPY . .

# 构建项目
RUN npm run build

# 第二阶段：生产阶段
FROM nginx:1.25-alpine

# 复制自定义Nginx配置（如果需要）
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从构建阶段复制构建后的文件到Nginx的静态文件目录
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
