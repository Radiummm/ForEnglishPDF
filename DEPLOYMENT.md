# 🌐 PDF Assistant 在线部署指南

## 方式一：Streamlit Community Cloud（推荐，免费）

### 步骤 1：准备 GitHub 仓库
✅ 您的代码已在 GitHub: `https://github.com/Radiummm/ForEnglishPDF`

### 步骤 2：部署到 Streamlit Cloud
1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 用 GitHub 账号登录
3. 点击 "New app"
4. 选择您的仓库：`Radiummm/ForEnglishPDF`
5. 主文件路径：`app.py`
6. 点击 "Deploy!"

### 步骤 3：配置 API 密钥
1. 在 Streamlit Cloud 应用页面，点击 "Manage app"
2. 在 "Secrets" 部分添加您的 API 密钥：

```toml
# SiliconFlow API（推荐）
SILICONFLOW_API_KEY = "your_actual_api_key"
SILICONFLOW_MODEL = "Qwen/Qwen2.5-72B-Instruct"
SELECTED_DOMAIN = "SiliconFlow"
```

### 步骤 4：访问您的应用
部署完成后，您将获得一个公开 URL，例如：
`https://forenglishpdf-radiummm.streamlit.app`

---

## 方式二：本地网络共享

### 启动应用供局域网访问
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

然后其他人可通过您的 IP 地址访问：
`http://你的IP地址:8501`

---

## 方式三：Docker 部署

### 构建并运行 Docker 容器
```bash
# 构建镜像
docker build -t pdf-assistant .

# 运行容器
docker run -p 8501:8501 --env-file .env pdf-assistant
```

### 使用 Docker Compose
```bash
# 编辑 .env 文件配置 API 密钥
cp .env.example .env

# 启动服务
docker-compose up -d
```

---

## 方式四：云服务器部署

### 推荐的云服务商
- **阿里云 ECS**
- **腾讯云 CVM** 
- **华为云 ECS**
- **AWS EC2**
- **Google Cloud**

### 部署步骤
1. 购买云服务器（1核2G内存即可）
2. 上传项目文件或克隆仓库
3. 安装 Docker 或 Python 环境
4. 配置防火墙开放 8501 端口
5. 运行应用

---

## 🔐 安全注意事项

1. **保护 API 密钥**：
   - 绝不在代码中硬编码密钥
   - 使用环境变量或密钥管理服务

2. **访问控制**：
   - 考虑添加用户认证
   - 限制文件上传大小和格式

3. **资源监控**：
   - 监控 API 使用量和成本
   - 设置合理的使用限制

---

## 📊 成本预估

### Streamlit Community Cloud
- **费用**: 完全免费
- **限制**: 公开访问，资源有限

### 云服务器
- **基础配置**: 1核2G，约 50-100元/月
- **API 费用**: 根据使用量，SiliconFlow 较便宜

### API 调用成本
- **SiliconFlow**: 约 ¥0.001/1K tokens
- **OpenAI**: 约 ¥0.01-0.06/1K tokens
- **月均成本**: 轻度使用 10-50元

---

## 🚀 推荐部署方案

**个人学习使用**: Streamlit Community Cloud（免费）

**团队内部使用**: Docker + 云服务器

**商业化应用**: 专业云服务 + 负载均衡 + CDN