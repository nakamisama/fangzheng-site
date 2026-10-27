# 方正贤良工作室 · 官网

静态单页站，零构建、零依赖。内容全部在 `index.html`，样式与脚本在 `assets/`。

## 目录

```
网站/
├── index.html              页面内容（改文案只动这里）
├── assets/
│   ├── style.css           样式（色板取自 Logo）
│   ├── main.js             滚动显现、页头收缩、年份
│   ├── fonts/              思源宋体子集（约 320KB，四个字重）
│   ├── logo.png            工作室 Logo（已去纸底）
│   ├── seal-fang.png       朱砂「方」印，用作站点图标
│   ├── hero-ink.webp       首页水墨山水
│   ├── game-xiake.webp     《侠行三国》插画
│   └── studio-desk.webp    工作室书桌
├── deploy/nginx.conf       站点 nginx 配置
├── Dockerfile              镜像（nginx:alpine）
├── docker-compose.yml      本地或服务器一键起
└── tools/subset_fonts.py   字体子集化脚本
```

## 本地预览

```bash
cd 网站
python -m http.server 8899
# 打开 http://127.0.0.1:8899
```

## Docker

```bash
docker compose up -d          # 访问 http://localhost:8080
```

## 部署到 Dokploy

1. Dokploy 新建 Application → 来源选 Git → 仓库指向本仓库，分支 `main`。
2. Build Type 选 **Dockerfile**，路径填 `Dockerfile`（本仓库根目录就是站点根目录）。
3. 容器端口填 **80**，在 Domains 里绑定域名并开启 HTTPS（Let's Encrypt）。
4. 部署完成后访问域名，`/healthz` 应返回 `ok`。

镜像不落数据库、不写磁盘，可随时重建。

## 改内容时注意

- **改了文案就要重跑字体子集**，否则新字会回退到系统字体，观感会不一致：
  ```bash
  python tools/subset_fonts.py
  ```
  脚本按 `index.html` + `assets/*.css|js` 里出现的字重新裁剪，四个字重一起处理。
- 游戏正式开放后，把 `index.html` 里「即将开放」那个 `<span class="btn btn--primary is-soon">` 换成指向游戏地址的 `<a>` 即可，注释已写好。
- 新增作品时，复制 `<article class="work">` 整块，或把 `.reserve-card` 换成真实条目。

## 色板

取自 Logo，全站只用这几个色：

| 变量 | 值 | 用途 |
|------|-----|------|
| `--paper` | `#f0e9dc` | 宣纸底色 |
| `--ink` | `#14110d` | 正文墨色 |
| `--gold` | `#ac7d44` | 鎏金、小标题 |
| `--cinnabar` | `#7c1c16` | 朱砂、强调 |
