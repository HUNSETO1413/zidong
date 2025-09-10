# 部署指南 / Deployment Guide

本文档说明如何将 N8N 工作流文档平台部署到 GitHub 和 Vercel。

## 🚀 部署步骤

### 1. 推送到 GitHub

```bash
# 1. 添加所有文件
git add .

# 2. 提交更改
git commit -m "feat: 添加中文版本支持和SEO优化文件"

# 3. 推送到 GitHub
git push origin main
```

### 2. 部署到 Vercel

#### 方法一：通过 Vercel Dashboard（推荐）

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 导入你的 GitHub 仓库
4. Vercel 会自动检测到 `vercel.json` 配置文件
5. 点击 "Deploy" 开始部署

#### 方法二：通过 Vercel CLI

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 登录 Vercel
vercel login

# 3. 部署项目
vercel --prod
```

### 3. 配置环境变量（可选）

如果需要配置环境变量，在 Vercel Dashboard 中：

1. 进入项目设置
2. 点击 "Environment Variables"
3. 添加需要的环境变量：
   - `PYTHONPATH`: `.`
   - 其他自定义环境变量

## 📁 项目结构

```
n8n-workflows/
├── api/
│   └── index.py          # Vercel 入口文件
├── static/
│   ├── index.html        # 英文版主页
│   ├── index-zh.html     # 中文版主页
│   ├── sitemap.xml       # 网站地图
│   ├── robots.txt        # 爬虫指令
│   └── llms.txt          # LLM 信息文件
├── .github/
│   └── workflows/
│       └── deploy.yml    # GitHub Actions 部署配置
├── vercel.json           # Vercel 部署配置
├── requirements-vercel.txt # Vercel 依赖
└── api_server.py         # 本地开发服务器
```

## 🔧 配置文件说明

### vercel.json
- 配置 Python 运行时
- 设置路由规则
- 配置函数超时时间

### api/index.py
- Vercel 优化的 FastAPI 应用
- 简化版本，适合 serverless 部署
- 包含基本的 API 端点和语言支持

### requirements-vercel.txt
- Vercel 部署所需的 Python 依赖
- 精简版本，只包含必要的包

## 🌐 访问地址

部署完成后，你的应用将可以通过以下地址访问：

- **生产环境**: `https://your-project.vercel.app`
- **中文版本**: `https://your-project.vercel.app/?lang=zh`
- **API 文档**: `https://your-project.vercel.app/docs`

## 📊 功能特性

### 多语言支持
- 自动语言检测（基于 Accept-Language 头）
- 手动语言切换按钮
- URL 参数语言控制 (`?lang=zh`)

### SEO 优化
- `/sitemap.xml` - 搜索引擎网站地图
- `/robots.txt` - 爬虫指令文件
- `/llms.txt` - 大语言模型信息文件

### API 端点
- `GET /api/workflows` - 搜索工作流
- `GET /api/categories` - 获取分类（支持翻译）
- `GET /api/stats` - 获取统计信息

## 🔍 故障排除

### 常见问题

1. **部署失败**
   - 检查 `requirements-vercel.txt` 中的依赖版本
   - 确保 `api/index.py` 文件存在且无语法错误

2. **静态文件无法访问**
   - 确保 `static/` 目录包含所有必要文件
   - 检查 `vercel.json` 中的路由配置

3. **API 响应错误**
   - 查看 Vercel 函数日志
   - 检查环境变量配置

### 调试技巧

```bash
# 本地测试 Vercel 部署
vercel dev

# 查看部署日志
vercel logs

# 检查函数状态
vercel inspect
```

## 📈 性能优化

### Vercel 部署优化
- 使用 serverless 函数
- 静态文件 CDN 加速
- 自动 HTTPS 和全球分发

### 建议配置
- 函数超时时间：30秒
- 最大包大小：50MB
- Python 版本：3.11

## 🔐 安全配置

### CORS 设置
- 允许跨域访问
- 支持所有 HTTP 方法
- 生产环境建议限制域名

### 环境变量
- 敏感信息使用环境变量
- 不要在代码中硬编码密钥
- 定期更新访问令牌

## 📝 更新部署

每次推送到 `main` 分支时，GitHub Actions 会自动触发部署：

1. 运行测试（如果有）
2. 构建应用
3. 部署到 Vercel
4. 更新生产环境

## 🎯 下一步

1. 配置自定义域名
2. 设置分析和监控
3. 添加更多 API 端点
4. 优化性能和缓存
5. 添加用户认证（如需要）

---

部署完成后，你将拥有一个高性能、多语言、SEO 优化的 N8N 工作流文档平台！🎉
