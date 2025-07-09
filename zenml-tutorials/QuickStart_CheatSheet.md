# 🚀 **ZENML QUICK START CHEAT SHEET**

## ⚡ **Quick Commands**

### 🏃 **Khởi Động Nhanh (30 seconds)**
```bash
# All-in-one startup
poetry poe local-infrastructure-up

# Connect CLI  
poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl
# (Nhấn Enter 3 lần)

# Mở Dashboard
http://127.0.0.1:8237/
```

### 🔍 **Kiểm Tra Nhanh**
```bash
# Status check
poetry run zenml status
docker ps

# Port check
lsof -i :8237 :6333 :27017
```

---

## 🛠️ **Essential Commands**

### 📦 **Infrastructure**
```bash
# Start all
poetry poe local-infrastructure-up

# Start individual
poetry poe local-docker-infrastructure-up
poetry poe local-zenml-server-up

# Stop all  
poetry poe local-infrastructure-down
```

### 🔗 **Connection**
```bash
# Login
poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl

# Status
poetry run zenml status

# Logout
poetry run zenml logout
```

### 📊 **Pipelines**
```bash
# List pipelines
poetry run zenml pipeline list

# List runs
poetry run zenml pipeline runs list

# Run example
cd learning-code && poetry run python example_pipeline.py
```

### 🗄️ **Artifacts & Stacks**
```bash
# List artifacts
poetry run zenml artifact list

# List stacks
poetry run zenml stack list

# Stack info
poetry run zenml stack describe
```

---

## 🔗 **URLs Bookmark**

| Service | URL | Purpose |
|---------|-----|---------|
| **ZenML Dashboard** | http://127.0.0.1:8237/ | ML Pipeline UI |
| **ZenML API** | http://127.0.0.1:8237/api/v1/ | REST API |
| **Qdrant** | http://localhost:6333/ | Vector DB API |
| **MongoDB** | mongodb://llm_engineering:llm_engineering@localhost:27017/ | Database |

---

## 🚨 **Troubleshooting 1-Liners**

### 🔌 **Port Issues**
```bash
# Find what's using ports
lsof -i :8237 :6333 :27017

# Kill specific port
sudo fuser -k 8237/tcp

# Restart Docker
docker restart llm_engineering_mongo llm_engineering_qdrant
```

### 🔄 **Connection Issues**
```bash
# Reset connection
poetry run zenml logout && poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl

# Check server health
curl http://127.0.0.1:8237/api/v1/info
```

### 🐳 **Docker Issues**
```bash
# Restart containers
poetry poe local-docker-infrastructure-down
poetry poe local-docker-infrastructure-up

# Check logs
docker logs llm_engineering_mongo --tail 10
docker logs llm_engineering_qdrant --tail 10
```

---

## 📋 **Workflow Templates**

### 🆕 **New Project Workflow**
```bash
# 1. Start infrastructure
poetry poe local-infrastructure-up

# 2. Connect CLI
poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl

# 3. Check status
poetry run zenml status

# 4. Create pipeline (copy from example_pipeline.py)
cp learning-code/example_pipeline.py my_pipeline.py

# 5. Run pipeline
poetry run python my_pipeline.py

# 6. Check results
http://127.0.0.1:8237/
```

### 🔄 **Daily Development Workflow**
```bash
# Morning startup
docker ps                                    # Check if running
poetry run zenml status                      # Check connection
http://127.0.0.1:8237/                      # Open dashboard

# Development
poetry run python my_pipeline.py            # Run pipeline
poetry run zenml pipeline runs list         # Check results

# End of day
poetry poe local-infrastructure-down         # Optional: stop all
```

### 🚨 **Quick Fix Workflow**
```bash
# Infrastructure not responding
poetry poe local-infrastructure-down
poetry poe local-infrastructure-up
poetry run zenml login http://127.0.0.1:8237 --api-key --no-verify-ssl

# Pipeline not running
poetry run zenml status                      # Check connection
cd learning-code                            # Check example first
poetry run python example_pipeline.py       # Run known working pipeline
```

---

## 💡 **Pro Tips**

### ⚡ **Speed Tips**
- **Bookmark Dashboard**: http://127.0.0.1:8237/
- **Alias commands**: 
  ```bash
  alias zml="poetry run zenml"
  alias zstatus="poetry run zenml status"
  alias zruns="poetry run zenml pipeline runs list"
  ```
- **Auto-start**: Add to `~/.bashrc`:
  ```bash
  # Auto-start ZenML when entering project
  if [[ "$PWD" == *"LLM-Engineers-Handbook"* ]]; then
      poetry run zenml status > /dev/null 2>&1 || echo "💡 Run: poetry poe local-infrastructure-up"
  fi
  ```

### 🎯 **Development Tips**
- **Test với example**: Luôn test `example_pipeline.py` trước khi debug
- **Dashboard > CLI**: Dùng Web UI để visualize, CLI để automate
- **Save commands**: Tạo scripts cho workflows thường dùng
- **Monitor resources**: `docker stats` để xem resource usage

### 🔒 **Security Tips**
- **Development only**: Current setup dùng NO_AUTH
- **Local binding**: Services chỉ bind localhost
- **Firewall**: Đảm bảo ports không expose ra internet

---

## 📱 **Mobile Quick Reference**

### 📟 **Status Indicators**
- ✅ **Green**: Service hoạt động bình thường
- 🟡 **Yellow**: Service starting/warning
- ❌ **Red**: Service error/stopped
- 🔄 **Blue**: Processing/in progress

### 🎮 **Keyboard Shortcuts (Dashboard)**
- `Ctrl+R`: Refresh page
- `Ctrl+Shift+I`: Developer tools
- `F5`: Hard refresh
- `Ctrl+T`: New tab để multi-task

---

## 📞 **Quick Support**

| Issue | Command | Expected Result |
|-------|---------|-----------------|
| **Cannot connect to ZenML** | `curl http://127.0.0.1:8237/api/v1/info` | JSON response với server info |
| **MongoDB not working** | `poetry run python -c "from pymongo import MongoClient; print(MongoClient('mongodb://llm_engineering:llm_engineering@localhost:27017/').admin.command('ping'))"` | `{'ok': 1.0}` |
| **Qdrant not working** | `curl http://localhost:6333/collections` | JSON response với collections |
| **Docker issues** | `docker ps \| grep llm_engineering` | 2 containers running |

---

**🎯 Remember: Nếu có vấn đề, luôn bắt đầu với `poetry run zenml status` và `docker ps`!** 