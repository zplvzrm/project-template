# 银行智能问答系统 (Banking RAG System)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-85%25-yellow.svg)]()

## 📖 项目简介

银行智能问答系统是基于RAG(Retrieval-Augmented Generation)架构的智能客服解决方案，专为银行业务场景设计。系统结合了检索增强生成技术，能够准确回答银行业务相关问题，包括账户查询、贷款咨询、投资理财、风险管控等多个业务领域。

### 🎯 核心功能
- 🏦 **银行业务问答**: 支持储蓄、贷款、信用卡、投资等业务咨询
- 🔍 **智能检索**: 基于向量数据库的语义检索
- 🤖 **生成式回答**: 结合检索结果的自然语言生成
- 📊 **多模态支持**: 支持文本、表格、图表等多种数据格式
- 🛡️ **安全合规**: 符合银行业数据安全和隐私保护要求
- 📈 **实时监控**: 问答质量监控和业务指标统计

### 🏗️ 技术架构
- **检索层**: 向量数据库 + 传统搜索引擎
- **生成层**: 大语言模型 (LLM)
- **知识库**: 银行业务文档、政策法规、FAQ
- **安全层**: 访问控制、数据脱敏、审计日志

## 🚀 快速开始

### 前置要求
- Python 3.8+
- Docker & Docker Compose (可选)
- CUDA 11.8+ (GPU部署)
- 内存: 最少16GB，推荐32GB+

### 安装部署

#### 方式一: 本地安装
```bash
# 克隆项目
git clone https://github.com/your-org/banking-rag-system.git
cd banking-rag-system

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 安装可选的GPU依赖
pip install -r requirements-gpu.txt  # 如需GPU支持
```

#### 方式二: Docker部署
```bash
# 使用Docker Compose启动
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 配置设置

#### 1. 环境变量配置
```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
vim .env
```

```bash
# .env 配置示例
# 大语言模型配置
LLM_MODEL_NAME=chatglm2-6b
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.example.com

# 向量数据库配置
VECTOR_DB_TYPE=chroma
VECTOR_DB_HOST=localhost
VECTOR_DB_PORT=8000

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/banking_rag
REDIS_URL=redis://localhost:6379/0

# 安全配置
JWT_SECRET_KEY=your_jwt_secret
ENCRYPT_KEY=your_encryption_key
```

#### 2. 模型配置
```yaml
# config/model_config.yaml
llm:
  model_name: "chatglm2-6b"
  max_tokens: 2048
  temperature: 0.7
  top_p: 0.9

embedding:
  model_name: "text2vec-large-chinese"
  dimension: 1024
  batch_size: 32

retrieval:
  top_k: 5
  similarity_threshold: 0.7
  rerank_model: "bge-reranker-large"
```

### 初始化知识库

#### 1. 准备知识库数据
```bash
# 数据目录结构
data/
├── documents/              # 业务文档
│   ├── banking_policies/   # 银行政策
│   ├── product_manuals/    # 产品手册
│   └── regulations/        # 法规文件
├── structured/             # 结构化数据
│   ├── faq.json           # 常见问题
│   ├── products.csv       # 产品信息
│   └── rates.json         # 利率信息
└── templates/              # 回答模板
```

#### 2. 构建向量索引
```bash
# 处理并构建知识库
python scripts/build_knowledge_base.py --data_path ./data --output_path ./vector_db

# 验证知识库
python scripts/validate_knowledge_base.py
```

### 启动服务

#### API服务启动
```bash
# 开发模式
python app.py

# 生产模式
gunicorn -c gunicorn.conf.py app:app
```

#### Web界面启动
```bash
# 启动前端服务
cd web_ui
npm install
npm run serve
```

## 📚 使用指南

### API接口

#### 智能问答接口
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "query": "什么是定期存款？利率是多少？",
    "session_id": "user_session_123",
    "context": {
      "user_type": "individual",
      "product_interest": ["savings", "investment"]
    }
  }'
```

#### 响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "answer": "定期存款是银行的一种储蓄产品...",
    "sources": [
      {
        "document": "储蓄产品手册",
        "relevance_score": 0.95,
        "chunk_id": "doc_001_chunk_05"
      }
    ],
    "confidence": 0.89,
    "response_time": 1.2
  }
}
```

### Python SDK使用

```python
from banking_rag import BankingRAGClient

# 初始化客户端
client = BankingRAGClient(
    api_key="your_api_key",
    base_url="http://localhost:8000"
)

# 简单问答
response = client.chat("信用卡年费是多少？")
print(response.answer)

# 带上下文的问答
response = client.chat(
    query="这个产品的风险等级如何？",
    context={
        "previous_query": "推荐一款理财产品",
        "user_profile": {"risk_tolerance": "moderate"}
    }
)
print(response.answer)
print(response.sources)
```

### Web界面使用

访问 `http://localhost:3000` 进入Web管理界面:

1. **问答测试**: 实时测试问答效果
2. **知识库管理**: 上传、更新、删除知识库文档
3. **对话历史**: 查看和分析历史对话
4. **系统监控**: 监控系统性能和问答质量
5. **用户管理**: 管理用户权限和访问控制

## 🏗️ 系统架构

### 整体架构图
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户界面      │    │   API网关       │    │   负载均衡      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────────────────────────────────────┐
         │              RAG核心服务                        │
         └─────────────────────────────────────────────────┘
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   检索服务      │    │   生成服务      │    │   管理服务      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   向量数据库    │    │   大语言模型    │    │   关系数据库    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 核心模块

#### 1. 文档处理模块 (`src/document_processor/`)
- **文档解析**: 支持PDF、Word、Excel、HTML等格式
- **内容提取**: 文本、表格、图片信息提取
- **文档分块**: 智能分块策略，保持语义完整性
- **元数据管理**: 文档来源、版本、更新时间等信息

#### 2. 向量检索模块 (`src/retrieval/`)
- **向量化**: 文本向量化和相似度计算
- **混合检索**: 向量检索 + 关键词检索
- **重排序**: 基于深度学习的结果重排序
- **缓存机制**: 查询结果缓存，提升响应速度

#### 3. 生成模块 (`src/generation/`)
- **模型适配**: 支持多种大语言模型
- **提示工程**: 针对银行业务优化的提示模板
- **内容生成**: 基于检索结果的答案生成
- **质量控制**: 生成内容的质量评估和过滤

#### 4. 安全模块 (`src/security/`)
- **访问控制**: 基于角色的权限管理
- **数据脱敏**: 敏感信息自动脱敏
- **审计日志**: 完整的操作审计记录
- **合规检查**: 符合银行业监管要求

## 📊 数据管理

### 知识库结构

#### 文档类型支持
- **政策文档**: 银行内部政策、监管政策
- **产品手册**: 各类金融产品说明书
- **业务流程**: 操作手册、业务流程图
- **FAQ文档**: 常见问题及标准答案
- **法规文件**: 相关法律法规条文

#### 数据预处理流程
```python
# 文档处理示例
from src.document_processor import DocumentProcessor

processor = DocumentProcessor()

# 1. 文档解析
documents = processor.parse_documents("./data/documents/")

# 2. 内容清洗
cleaned_docs = processor.clean_content(documents)

# 3. 智能分块
chunks = processor.chunk_documents(
    cleaned_docs, 
    chunk_size=512, 
    overlap=50
)

# 4. 向量化存储
processor.store_to_vector_db(chunks)
```

### 数据更新策略

#### 增量更新
```bash
# 增量更新脚本
python scripts/incremental_update.py \
  --new_documents ./data/new_docs/ \
  --update_mode append
```

#### 全量重建
```bash
# 全量重建索引
python scripts/full_rebuild.py \
  --data_path ./data/ \
  --backup_existing true
```

## 🔧 配置说明

### 模型配置

#### 大语言模型配置
```yaml
# config/llm_config.yaml
models:
  chatglm2:
    model_path: "/models/chatglm2-6b"
    device: "cuda:0"
    precision: "fp16"
    max_memory: "14GB"
    
  baichuan:
    model_path: "/models/baichuan-13b-chat"
    device: "cuda:1"
    precision: "int4"
    
prompts:
  banking_qa:
    template: |
      你是一个专业的银行客服助手。请基于以下知识内容回答用户问题：
      
      知识内容：
      {context}
      
      用户问题：
      {question}
      
      请提供准确、专业的回答：
    max_tokens: 1024
```

#### 检索配置
```yaml
# config/retrieval_config.yaml
vector_search:
  embedding_model: "text2vec-large-chinese"
  similarity_metric: "cosine"
  top_k: 10
  
keyword_search:
  enabled: true
  weight: 0.3
  min_score: 0.1
  
reranking:
  model: "bge-reranker-large"
  enabled: true
  top_k: 5
```

### 业务配置

#### 业务规则配置
```json
{
  "business_rules": {
    "sensitive_info": [
      "账号", "密码", "身份证", "银行卡号"
    ],
    "restricted_topics": [
      "内幕交易", "洗钱", "违规操作"
    ],
    "auto_escalation": {
      "confidence_threshold": 0.6,
      "escalation_keywords": ["投诉", "纠纷", "法律"]
    }
  }
}
```

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定模块测试
pytest tests/test_retrieval.py -v

# 生成覆盖率报告
pytest --cov=src tests/ --cov-report=html
```

### 性能测试
```bash
# API性能测试
python tests/performance/api_benchmark.py

# 向量检索性能测试
python tests/performance/retrieval_benchmark.py

# 端到端性能测试
python tests/performance/e2e_benchmark.py
```

### 问答质量评估
```bash
# 运行评估脚本
python scripts/evaluate_qa_quality.py \
  --test_data ./data/test_qa.json \
  --output_report ./reports/qa_evaluation.html
```

## 📈 监控和运维

### 系统监控

#### Prometheus监控指标
- `rag_query_total`: 查询总数
- `rag_query_duration`: 查询响应时间
- `rag_retrieval_accuracy`: 检索准确率
- `rag_generation_quality`: 生成质量评分

#### 日志配置
```yaml
# config/logging.yaml
version: 1
formatters:
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  file:
    class: logging.handlers.RotatingFileHandler
    filename: logs/banking_rag.log
    maxBytes: 10485760
    backupCount: 5
    formatter: detailed
loggers:
  banking_rag:
    level: INFO
    handlers: [file]
```

### 运维工具

#### 健康检查
```bash
# 系统健康检查
curl http://localhost:8000/health

# 详细健康状态
curl http://localhost:8000/health/detailed
```

#### 管理命令
```bash
# 重载知识库
python manage.py reload_knowledge_base

# 清理缓存
python manage.py clear_cache

# 数据库迁移
python manage.py db upgrade
```

## 🔒 安全说明

### 数据安全
- **传输加密**: 所有API通信使用HTTPS/TLS
- **存储加密**: 敏感数据加密存储
- **访问控制**: 基于JWT的身份认证
- **数据脱敏**: 自动识别和脱敏敏感信息

### 合规要求
- 符合银行业数据安全规范
- 支持审计日志记录
- 实现数据访问权限控制
- 提供数据备份和恢复机制

## 🚀 部署指南

### 生产环境部署

#### Docker部署
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  banking-rag:
    image: banking-rag:latest
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 8G
          cpus: '4'
```

#### Kubernetes部署
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: banking-rag
spec:
  replicas: 3
  selector:
    matchLabels:
      app: banking-rag
  template:
    metadata:
      labels:
        app: banking-rag
    spec:
      containers:
      - name: banking-rag
        image: banking-rag:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
```

### 性能优化建议

#### 硬件配置
- **CPU**: Intel Xeon或AMD EPYC，最少16核
- **内存**: 最少32GB，推荐64GB+
- **GPU**: NVIDIA A100/V100 (可选，用于模型推理加速)
- **存储**: NVMe SSD，最少500GB

#### 软件优化
- 使用模型量化减少内存占用
- 实现查询缓存提升响应速度
- 配置连接池优化数据库性能
- 启用CDN加速静态资源访问

## 📋 更新日志

### v2.1.0 (2024-01-15)
- ✨ 新增多轮对话支持
- 🔧 优化向量检索算法
- 🐛 修复知识库更新Bug
- 📈 提升问答准确率至89%

### v2.0.0 (2023-12-01)
- 🎉 全新RAG架构重构
- ✨ 支持多模态问答
- 🔒 增强安全审计功能
- 📊 新增管理后台

### v1.5.0 (2023-10-15)
- ✨ 新增API接口
- 🔧 优化模型推理性能
- 📚 扩充银行业务知识库
- 🐛 修复若干已知问题

## 🤝 贡献指南

### 开发流程
1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范
- 遵循PEP8代码风格
- 使用Black进行代码格式化
- 添加必要的类型注解
- 编写单元测试

### 提交规范
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

类型说明:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 📞 支持与联系

### 技术支持
- 📧 邮箱: support@bankingrag.com
- 💬 微信群: 扫码加入技术交流群
- 🐛 问题反馈: [GitHub Issues](https://github.com/your-org/banking-rag-system/issues)

### 社区资源
- 📖 详细文档: [文档中心](https://docs.bankingrag.com)
- 🎓 教程视频: [YouTube频道](https://youtube.com/bankingrag)
- 💼 商业合作: business@bankingrag.com

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

感谢以下开源项目的支持:
- [Langchain](https://github.com/hwchase17/langchain)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Sentence Transformers](https://github.com/UKPLab/sentence-transformers)
- [FastAPI](https://github.com/tiangolo/fastapi)

---

**⭐ 如果这个项目对你有帮助，请给我们一个Star！**

You may need to read the [develop document](./docs/development.md) to use SRC Layout in your IDE.
