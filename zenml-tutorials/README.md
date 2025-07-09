# 📚 **LEARNING CODE - ZENML HANDBOOK**

Chào mừng bạn đến với thư mục `learning-code`! Đây là nơi chứa tất cả các hướng dẫn, examples, và resources để học và làm việc với ZenML infrastructure.

## 🚨 **QUAN TRỌNG: _ctypes Issue**

**Nếu bạn gặp lỗi `ModuleNotFoundError: No module named '_ctypes'`:**

1. 🔧 **Quick Fix**: Đọc [FIX_ctypes_issue.md](./FIX_ctypes_issue.md)
2. 🧪 **Test trước**: Chạy `poetry run python test_zenml_connection.py`
3. ⚡ **Workaround**: Sử dụng ZenML Dashboard thay vì pipelines

**Root cause**: Python được build mà không có libffi support. Solution involves reinstalling Python.

---

## 📖 **Nội Dung Thư Mục**

### 📄 **Documentation Files**
| File | Mô Tả | Khi Nào Sử Dụng |
|------|-------|-----------------|
| **[ZenML_Infrastructure_Guide.md](./ZenML_Infrastructure_Guide.md)** | Hướng dẫn toàn diện về ZenML infrastructure | Đọc để hiểu chi tiết system |
| **[QuickStart_CheatSheet.md](./QuickStart_CheatSheet.md)** | Cheat sheet với commands thường dùng | Reference nhanh hàng ngày |
| **[FIX_ctypes_issue.md](./FIX_ctypes_issue.md)** | 🔧 Fix lỗi _ctypes module | Khi gặp ModuleNotFoundError |
| **[README.md](./README.md)** | File này - tổng quan folder | Điểm bắt đầu |

### 🐍 **Python Examples**
| File | Mô Tả | Level | Status |
|------|-------|-------|--------|
| **[zenml_hello_world.py](./zenml_hello_world.py)** | Basic ZenML example (có sẵn) | Beginner | ⚠️ Needs _ctypes fix |
| **[example_pipeline.py](./example_pipeline.py)** | Complete ML pipeline với pandas | Intermediate | ⚠️ Needs _ctypes fix |
| **[simple_example_pipeline.py](./simple_example_pipeline.py)** | Pure Python pipeline (no pandas) | Intermediate | ⚠️ Needs _ctypes fix |
| **[test_zenml_connection.py](./test_zenml_connection.py)** | Test ZenML connectivity | Diagnostic | ✅ Works |

---

## 🚀 **Quick Start (5 phút)**

### 1️⃣ **Setup Infrastructure**
```bash
# Từ root project directory
poetry poe local-infrastructure-up

# Connect CLI
poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl
# (Nhấn Enter 3 lần khi được hỏi API key)
```

### 2️⃣ **Test Connection (Recommended First)**
```bash
# Di chuyển vào learning-code
cd learning-code

# Test connectivity without running pipelines
poetry run python test_zenml_connection.py
```

### 3️⃣ **Choose Your Path**

#### 🎯 **If _ctypes works (test shows 100% pass rate):**
```bash
# Run full pipeline
poetry run python example_pipeline.py
```

#### ⚠️ **If _ctypes fails (test shows _ctypes error):**
```bash
# Option A: Fix the issue (recommended)
# See: FIX_ctypes_issue.md

# Option B: Use Dashboard only
# Open: http://127.0.0.1:8237/
# You can still explore ZenML features!
```

### 4️⃣ **View Results**
- **Web UI**: http://127.0.0.1:8237/
- **CLI**: `poetry run zenml pipeline runs list` (if pipelines worked)

---

## 📚 **Learning Path**

### 🌱 **Beginner**
1. **Đọc**: [QuickStart_CheatSheet.md](./QuickStart_CheatSheet.md) - Làm quen với commands cơ bản
2. **Chạy**: `zenml_hello_world.py` - Hello World example
3. **Khám phá**: ZenML Dashboard tại http://127.0.0.1:8237/

### 🌿 **Intermediate**  
1. **Đọc**: [ZenML_Infrastructure_Guide.md](./ZenML_Infrastructure_Guide.md) - Hiểu architecture
2. **Chạy**: `example_pipeline.py` - Complete ML pipeline
3. **Thử nghiệm**: Modify example để tạo pipeline riêng

### 🌳 **Advanced**
1. **Tích hợp**: Kết hợp với MongoDB và Qdrant
2. **Custom Components**: Tạo custom steps và artifacts
3. **Production**: Deploy pipelines lên cloud

---

## 🎯 **Use Cases & Examples**

### 📊 **Data Processing Pipeline**
```python
# Example từ example_pipeline.py
@pipeline
def data_processing_pipeline():
    raw_data = generate_sample_data()
    processed_data, stats = data_preprocessing(raw_data)
    engineered_data = feature_engineering(processed_data)
    return engineered_data
```

### 🤖 **ML Training Pipeline**
```python
@pipeline  
def ml_training_pipeline():
    data = load_training_data()
    model = train_model(data)
    metrics = evaluate_model(model, data)
    return model, metrics
```

### 🔍 **Vector Search Pipeline**
```python
@pipeline
def vector_search_pipeline():
    documents = load_documents()
    embeddings = generate_embeddings(documents)
    store_in_qdrant(embeddings)
    return "Embeddings stored successfully"
```

---

## 🛠️ **Development Workflow**

### 📋 **Daily Workflow**
1. **Morning Setup**:
   ```bash
   cd /home/dino/Documents/LLM-Engineers-Handbook
   poetry run zenml status  # Check if running
   ```

2. **Development**:
   ```bash
   cd learning-code
   # Edit your pipeline
   poetry run python my_pipeline.py
   ```

3. **Monitoring**:
   - Dashboard: http://127.0.0.1:8237/
   - CLI: `poetry run zenml pipeline runs list`

### 🔄 **Iteration Cycle**
1. **Code** → Write/modify pipeline
2. **Run** → Execute pipeline 
3. **Monitor** → Check results in Dashboard
4. **Debug** → Fix issues if any
5. **Repeat** → Improve pipeline

---

## 🔧 **Tools & Utilities**

### 📱 **Quick Commands** 
```bash
# Infrastructure
poetry poe local-infrastructure-up    # Start all
poetry poe local-infrastructure-down  # Stop all

# ZenML
poetry run zenml status               # Check status
poetry run zenml pipeline runs list  # List runs
poetry run zenml artifact list       # List artifacts

# Docker
docker ps                            # Check containers
docker logs llm_engineering_mongo    # MongoDB logs
docker logs llm_engineering_qdrant   # Qdrant logs
```

### 🌐 **URLs**
- **ZenML Dashboard**: http://127.0.0.1:8237/
- **Qdrant API**: http://localhost:6333/collections
- **ZenML API**: http://127.0.0.1:8237/api/v1/info

---

## 📂 **File Structure**

```
learning-code/
├── README.md                           # Tổng quan (file này)
├── ZenML_Infrastructure_Guide.md       # Hướng dẫn chi tiết
├── QuickStart_CheatSheet.md            # Reference nhanh
├── zenml_hello_world.py               # Basic example (có sẵn)
├── example_pipeline.py                # Complete ML pipeline
└── [your_custom_pipelines.py]         # Pipelines của bạn
```

---

## 🎓 **Learning Resources**

### 📖 **Documentation**
- **ZenML Official**: https://docs.zenml.io/
- **MongoDB**: https://docs.mongodb.com/
- **Qdrant**: https://qdrant.tech/documentation/

### 🎬 **Video Tutorials**
- ZenML Getting Started (YouTube)
- MLOps with ZenML (YouTube)

### 📚 **Books & Articles**
- "Building Machine Learning Pipelines" - O'Reilly
- MLOps best practices articles

---

## 🚨 **Troubleshooting**

### ⚡ **Quick Fixes**
| Problem | Solution |
|---------|----------|
| **ZenML not connecting** | `poetry run zenml logout && poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl` |
| **Docker not running** | `poetry poe local-docker-infrastructure-up` |
| **Pipeline fails** | Check `poetry run zenml status` first |
| **Port conflicts** | `lsof -i :8237 :6333 :27017` |

### 📞 **Get Help**
1. **Check status**: `poetry run zenml status`
2. **Read logs**: `docker logs llm_engineering_mongo`
3. **Test example**: `cd learning-code && poetry run python example_pipeline.py`
4. **Reset all**: `poetry poe local-infrastructure-down && poetry poe local-infrastructure-up`

---

## 💡 **Pro Tips**

### ⚡ **Productivity**
- **Bookmark** Dashboard: http://127.0.0.1:8237/
- **Alias** common commands trong `~/.bashrc`
- **Auto-complete** với ZenML CLI
- **Monitor** resources với `docker stats`

### 🎯 **Best Practices**
- **Test** với `example_pipeline.py` trước khi debug
- **Version control** pipeline code
- **Document** custom steps
- **Monitor** pipeline performance
- **Clean up** old artifacts thường xuyên

### 🔒 **Security**
- Current setup dùng **NO_AUTH** (development only)
- **Không expose** ports ra internet
- **Backup** data thường xuyên

---

## 🎉 **Next Steps**

### 🎯 **Immediate Goals**
1. ✅ Setup infrastructure thành công
2. ✅ Chạy example pipeline  
3. ⏳ Tạo custom pipeline đầu tiên
4. ⏳ Tích hợp với MongoDB/Qdrant
5. ⏳ Deploy pipeline production

### 🚀 **Advanced Goals**
- **Custom Components**: Tạo custom steps
- **Integration**: Kết nối external APIs
- **Monitoring**: Setup alerting và logging
- **Scaling**: Deploy distributed pipelines
- **MLOps**: Full CI/CD pipeline

---

## 📞 **Contact & Support**

- **GitHub Issues**: Báo cáo bugs
- **Documentation**: Đọc docs khi gặp vấn đề
- **Community**: Join ZenML Discord/Slack

---

**🎯 Happy Learning và Happy ML Engineering! 🚀**

---

*Last updated: $(date)*
*Location: `/home/dino/Documents/LLM-Engineers-Handbook/learning-code/`* 