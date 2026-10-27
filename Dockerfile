# 方正贤良工作室官网 · 静态站镜像
# 构建：docker build -t fangzheng-site .
# 运行：docker run -p 8080:80 fangzheng-site
FROM nginx:1.27-alpine

# 站点内容（纯静态，无需构建步骤）
COPY index.html /usr/share/nginx/html/index.html
COPY assets/ /usr/share/nginx/html/assets/
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf

# 健康检查给 Dokploy / 反代探活用
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q --spider http://127.0.0.1/healthz || exit 1

EXPOSE 80
