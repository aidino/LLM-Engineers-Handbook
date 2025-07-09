# 🚀 **HƯỚNG DẪN SỬ DỤNG ZENML INFRASTRUCTURE**

## 📖 **Mục Lục**
1. [Tổng Quan Hệ Thống](#tổng-quan-hệ-thống)
2. [Khởi Động Infrastructure](#khởi-động-infrastructure)
3. [Sử Dụng ZenML Dashboard](#sử-dụng-zenml-dashboard)
4. [Làm Việc Với CLI](#làm-việc-với-cli)
5. [Database Operations](#database-operations)
6. [Chạy ML Pipelines](#chạy-ml-pipelines)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 **Tổng Quan Hệ Thống**

### 🏗️ **Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MongoDB       │    │     Qdrant      │    │   ZenML Server  │
│   Port: 27017   │    │   Port: 6333    │    │   Port: 8237    │
│   Database      │    │   Vector DB     │    │   ML Platform   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Your Projects  │
                    │  ML Pipelines   │
                    └─────────────────┘
```

### 📦 **Components**
- **MongoDB**: Lưu trữ metadata, artifacts, và pipeline configurations
- **Qdrant**: Vector database cho embedding storage và similarity search
- **ZenML**: ML orchestration platform với Web UI và API

---

## 🚀 **Khởi Động Infrastructure**

### ⚡ **Quick Start (All-in-One)**
```bash
# Khởi động toàn bộ infrastructure
poetry poe local-infrastructure-up
```

### 🔧 **Step-by-Step Setup**
```bash
# Bước 1: Khởi động Docker containers
poetry poe local-docker-infrastructure-up

# Bước 2: Dọn dẹp ZenML sessions cũ
poetry poe local-zenml-server-down

# Bước 3: Khởi động ZenML server
poetry poe local-zenml-server-up
```

### 🔌 **Kết Nối ZenML CLI**
```bash
# Kết nối CLI với server
poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl
# Nhấn Enter 3 lần khi được hỏi API key (server dùng NO_AUTH)
```

### ✅ **Kiểm Tra Trạng Thái**
```bash
# Kiểm tra tất cả services
docker ps
poetry run zenml status

# Kiểm tra ports
lsof -i :27017 :6333 :8237
```

---

## 🌐 **Sử Dụng ZenML Dashboard**

### 📱 **Truy Cập Web UI**
```
URL: http://127.0.0.1:8237/
```

### 🎛️ **Tính Năng Dashboard**
- **Pipelines**: Xem và quản lý ML pipelines
- **Runs**: Monitor training runs và experiments  
- **Artifacts**: Quản lý model artifacts và datasets
- **Stacks**: Cấu hình infrastructure components
- **Users**: Quản lý users và permissions

### 🔍 **Navigation Tips**
```
🏠 Home → Tổng quan system
📊 Pipelines → Danh sách pipelines
🏃 Runs → Execution history
📦 Artifacts → Stored models/data
⚙️ Stacks → Infrastructure config
👥 Users → User management
```

---

## 💻 **Làm Việc Với CLI**

### 📊 **Basic Commands**
```bash
# Xem trạng thái
poetry run zenml status

# Liệt kê stacks
poetry run zenml stack list

# Liệt kê pipelines
poetry run zenml pipeline list

# Xem runs
poetry run zenml pipeline runs list

# Liệt kê artifacts
poetry run zenml artifact list
```

### 🔧 **Stack Management**
```bash
# Xem stack hiện tại
poetry run zenml stack describe

# Chuyển đổi stack
poetry run zenml stack set <stack-name>

# Tạo stack mới
poetry run zenml stack register <stack-name> \
  --orchestrator <orchestrator-name> \
  --artifact-store <artifact-store-name>
```

### 🗂️ **Artifact Management**
```bash
# Xem chi tiết artifact
poetry run zenml artifact describe <artifact-id>

# Download artifact
poetry run zenml artifact download <artifact-id>

# List versions
poetry run zenml artifact versions list <artifact-name>
```

---

## 🗄️ **Database Operations**

### 🐘 **MongoDB Operations**
```bash
# Test connection
poetry run python -c "
from pymongo import MongoClient
client = MongoClient('mongodb://llm_engineering:llm_engineering@localhost:27017/')
print('MongoDB Status:', client.admin.command('ping'))
"

# Kết nối từ Python code
from pymongo import MongoClient
client = MongoClient('mongodb://llm_engineering:llm_engineering@localhost:27017/')
db = client['your_database']
collection = db['your_collection']
```

### 🔍 **Qdrant Operations**
```bash
# Test API
curl http://localhost:6333/collections

# Tạo collection mới
curl -X PUT "http://localhost:6333/collections/my_collection" \
  -H "Content-Type: application/json" \
  -d '{
    "vectors": {
      "size": 384,
      "distance": "Cosine"
    }
  }'

# Từ Python code
import requests
response = requests.get('http://localhost:6333/collections')
print(response.json())
```

### 📡 **ZenML API**
```bash
# Server info
curl http://127.0.0.1:8237/api/v1/info

# List stacks
curl http://127.0.0.1:8237/api/v1/stacks

# List pipelines
curl http://127.0.0.1:8237/api/v1/pipelines
```

---

## 🔄 **Chạy ML Pipelines**

### 📝 **Available Pipelines**
```bash
# Data ETL pipelines
poetry poe run-digital-data-etl-maxime
poetry poe run-digital-data-etl-paul
poetry poe run-digital-data-etl  # Chạy cả hai

# Feature engineering
poetry poe run-feature-engineering-pipeline

# Dataset generation
poetry poe run-generate-instruct-datasets-pipeline
poetry poe run-generate-preference-datasets-pipeline

# End-to-end pipeline
poetry poe run-end-to-end-data-pipeline

# Training & evaluation
poetry poe run-training-pipeline
poetry poe run-evaluation-pipeline
```

### 🎯 **Pipeline Examples**

#### 💾 **Data Export/Import**
```bash
# Export data warehouse to JSON
poetry poe run-export-data-warehouse-to-json

# Import data from JSON
poetry poe run-import-data-warehouse-from-json

# Export artifacts
poetry poe run-export-artifact-to-json-pipeline
```

#### 🤖 **Inference Services**
```bash
# Start ML inference service
poetry poe run-inference-ml-service

# Test inference API
poetry poe call-inference-ml-service

# RAG retrieval
poetry poe call-rag-retrieval-module
```

### 📊 **Monitoring Runs**
```bash
# Xem runs trong CLI
poetry run zenml pipeline runs list

# Xem chi tiết run
poetry run zenml pipeline runs describe <run-id>

# Xem logs
poetry run zenml pipeline runs logs <run-id>
```

---

## 🔧 **Custom Pipeline Development**

### 📄 **Tạo Pipeline Mới**
```python
# learning-code/my_pipeline.py
from zenml import pipeline, step
from zenml.integrations.mongodb import MongoDBSettings
from zenml.integrations.qdrant import QdrantSettings

@step
def data_loader() -> dict:
    """Load data from MongoDB"""
    from pymongo import MongoClient
    client = MongoClient('mongodb://llm_engineering:llm_engineering@localhost:27017/')
    # Your data loading logic
    return {"data": "sample_data"}

@step  
def feature_extractor(data: dict) -> list:
    """Extract features"""
    # Your feature extraction logic
    return [1, 2, 3, 4]

@step
def vector_store(features: list) -> None:
    """Store in Qdrant"""
    import requests
    # Store vectors in Qdrant
    pass

@pipeline
def my_ml_pipeline():
    """Complete ML pipeline"""
    data = data_loader()
    features = feature_extractor(data)
    vector_store(features)

if __name__ == "__main__":
    my_ml_pipeline()
```

### 🏃 **Chạy Custom Pipeline**
```bash
cd learning-code
poetry run python my_pipeline.py
```

---

## 🛠️ **Troubleshooting**

### ⚠️ **Common Issues**

#### 🔌 **Port Conflicts**
```bash
# Kiểm tra ports bị chiếm
lsof -i :27017 :6333 :8237

# Dừng processes conflict
docker stop <container-name>
pkill -f zenml
```

#### 🔄 **ZenML Connection Issues**
```bash
# Disconnect và reconnect
poetry run zenml logout
poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl

# Reset ZenML config
rm -rf ~/.config/zenml
poetry run zenml init
```

#### 🐳 **Docker Issues**
```bash
# Restart Docker containers
poetry poe local-docker-infrastructure-down
poetry poe local-docker-infrastructure-up

# Check Docker logs
docker logs llm_engineering_mongo
docker logs llm_engineering_qdrant
```

### 🔄 **Restart Everything**
```bash
# Hoàn toàn restart infrastructure
poetry poe local-infrastructure-down
poetry poe local-infrastructure-up

# Reconnect CLI
poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl
```

### 📊 **Health Checks**
```bash
# MongoDB
poetry run python -c "from pymongo import MongoClient; print(MongoClient('mongodb://llm_engineering:llm_engineering@localhost:27017/').admin.command('ping'))"

# Qdrant
curl http://localhost:6333/collections

# ZenML
curl http://127.0.0.1:8237/api/v1/info
poetry run zenml status
```

---

## 🎯 **Best Practices**

### 📋 **Development Workflow**
1. **Start Infrastructure**: `poetry poe local-infrastructure-up`
2. **Connect CLI**: `poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl`
3. **Develop Pipeline**: Tạo steps và pipelines
4. **Test Locally**: Chạy pipeline trong development
5. **Monitor**: Kiểm tra kết quả qua Dashboard
6. **Iterate**: Cải thiện pipeline dựa trên results

### 💡 **Tips**
- **Luôn kiểm tra status**: `poetry run zenml status`
- **Sử dụng Dashboard**: Dễ visualize hơn CLI
- **Backup data**: Export artifacts thường xuyên
- **Monitor resources**: Kiểm tra Docker memory/CPU usage
- **Clean up**: Xóa old runs và artifacts để tiết kiệm space

### 🔒 **Security Notes**
- Server hiện tại chạy `NO_AUTH` mode (development only)
- Cho production, cần setup proper authentication
- MongoDB credentials: `llm_engineering:llm_engineering`
- Chỉ bind localhost - không expose ra internet

---

## 📚 **Additional Resources**

### 🔗 **URLs**
- **ZenML Dashboard**: http://127.0.0.1:8237/
- **MongoDB**: mongodb://llm_engineering:llm_engineering@localhost:27017/
- **Qdrant API**: http://localhost:6333/
- **ZenML API**: http://127.0.0.1:8237/api/v1/

### 📖 **Documentation**
- [ZenML Docs](https://docs.zenml.io/)
- [MongoDB Docs](https://docs.mongodb.com/)
- [Qdrant Docs](https://qdrant.tech/documentation/)

### 🎓 **Learning Resources**
- Xem file `zenml_hello_world.py` trong folder này
- Tham khảo pipelines có sẵn trong project
- Thử nghiệm với các examples trong `tools/` folder

---

**🎉 Happy ML Engineering với ZenML Infrastructure! 🎉** 