# PolyMentor - Complete Vision & Architecture

## 🎯 Mission Statement

**Build an AI coding tutor that starts with Groq and becomes a custom powerhouse through continuous learning.**

- **Phase 1 (Now):** PolyCode delivers instant help via Groq API
- **Phase 2 (Week 2):** Every conversation stored in MongoDB for training data
- **Phase 3 (Week 3):** Daily MLOps pipeline retrains on cloud GPUs
- **Phase 4 (Week 4+):** Custom model surpasses Groq through accumulated wisdom

---

## 📋 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         POLYMENTOR SYSTEM                        │
└─────────────────────────────────────────────────────────────────┘

LAYER 1: USER INTERFACE (PolyCode Website)
┌─────────────────────────────────────────────────────────────────┐
│  React Website (localhost:5173)                                  │
│  - Beautiful chat interface                                      │
│  - Code editor with syntax highlighting                         │
│  - Language selector (16+ languages)                            │
│  - Difficulty level selector                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓↑
LAYER 2: API GATEWAY (FastAPI)
┌─────────────────────────────────────────────────────────────────┐
│  FastAPI Server (localhost:8000)                                │
│  - Routes: /chat, /review, /teach                              │
│  - Request validation                                           │
│  - Response formatting                                          │
│  - CORS handling                                                │
└─────────────────────────────────────────────────────────────────┘
           ↓↑ (inference)              ↓ (log every chat)
           │                            │
LAYER 3: INFERENCE & DATA STORAGE
┌──────────────────────────────┐  ┌─────────────────────────────┐
│  GROQ API (Live Service)     │  │ MongoDB (Data Collection)   │
│  - Fast responses            │  │ - Store user messages       │
│  - LLM: Llama 3.3 70B       │  │ - Store Groq responses     │
│  - Temperature: 0.25         │  │ - Language metadata         │
│  - Max tokens: 1800          │  │ - Level metadata           │
│  - Response time: 100-500ms  │  │ - Timestamp & session ID   │
│                              │  │ - Chat history            │
└──────────────────────────────┘  └─────────────────────────────┘
           │                            ↑
           │                            │
    (serves users NOW)         (collects training data)
                                        │
LAYER 4: MLOPS PIPELINE (Daily, Automated)
┌─────────────────────────────────────────────────────────────────┐
│  Scheduled Jobs (Cron / Airflow)                                │
│                                                                 │
│  STEP 1: Extract Training Data                                 │
│  ├─ Query MongoDB for new conversations (last 24h)            │
│  ├─ Filter & clean data                                       │
│  ├─ Format as training pairs: (user_question, groq_response)  │
│  └─ Save to: data/processed/daily_train.json                 │
│                                                                 │
│  STEP 2: Launch Training on Cloud GPU                         │
│  ├─ Base model: Qwen2.5-Coder-7B or LLama-3.1-8B-Instruct   │
│  ├─ Fine-tuning method: LoRA (efficient)                     │
│  ├─ Cloud providers: RunPod / Lambda / AWS SageMaker          │
│  ├─ Epochs: 3                                                 │
│  └─ Output: models_saved/polymentor-lora-{date}              │
│                                                                 │
│  STEP 3: Evaluate New Model                                   │
│  ├─ Test on held-out eval set                                │
│  ├─ Compare: Custom Model vs Groq                             │
│  ├─ Metrics: accuracy, speed, relevance                       │
│  └─ Decision: Is custom model better?                         │
│                                                                 │
│  STEP 4: Deploy if Better                                     │
│  ├─ If quality ↑: Push to HF Hub                             │
│  ├─ If quality ↑: Update inference server                    │
│  ├─ If quality ↑: Route 10% traffic to custom                │
│  └─ If quality ↓: Keep using Groq                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
LAYER 5: MODEL INFERENCE (Eventually)
┌─────────────────────────────────────────────────────────────────┐
│  Custom Model Inference Server                                  │
│  - Hosts the retrained PolyMentor model                        │
│  - Gradually replaces Groq as quality improves                │
│  - Load balancing: % Groq vs % Custom                         │
│  - Monitoring & logging                                        │
└─────────────────────────────────────────────────────────────────┘

RESULT: Each day, PolyMentor gets smarter! 🚀
```

---

## 🔄 4-Phase Rollout Plan

### **PHASE 1: PolyCode with Groq (✅ DONE - This Week)**

**Goal:** Launch working chat interface using Groq API

**What's Implemented:**
- ✅ React chat website (beautiful UI)
- ✅ FastAPI backend (/chat, /review, /teach endpoints)
- ✅ Groq API integration (Llama 3.3 70B)
- ✅ Code syntax highlighting
- ✅ Language support (16+ languages)
- ✅ Error handling & loading states
- ✅ Responsive design (mobile, tablet, desktop)

**What You Can Do:**
```bash
# Terminal 1
uvicorn src.api.app:app --reload

# Terminal 2
cd website && npm run dev

# Browser
http://localhost:5173/
```

**Output:** Users get instant coding help from Groq ✨

---

### **PHASE 2: MongoDB Data Collection (🔄 NEXT - Week 2)**

**Goal:** Store every conversation for training data

**What to Implement:**
1. **MongoDB Setup**
   ```bash
   # Local MongoDB or MongoDB Atlas (cloud)
   # Connection string in .env
   MONGODB_URI=mongodb+srv://user:pass@cluster/polymentor
   ```

2. **Chat Storage Schema**
   ```python
   db.conversations.insertOne({
       "_id": ObjectId(),
       "session_id": "uuid",
       "user_id": "optional",
       "timestamp": ISODate(),
       "user_message": "Find the bug",
       "user_code": "for i in range(10)\n    print(i)",
       "language": "python",
       "level": "beginner",
       "groq_response": "I found a syntax error...",
       "groq_model": "llama-3.3-70b-versatile",
       "response_time_ms": 245.5,
       "quality_score": null  # For later ML model evaluation
   })
   ```

3. **Update API to Save Chats**
   - Modify `/chat` endpoint to store each interaction
   - Track conversation context
   - Index by language, level, timestamp

4. **Benefits:**
   - Data grows with every user interaction
   - Real programming conversations
   - Natural distribution of problem types
   - Ready for ML training

**Est. Time:** 2-3 days

---

### **PHASE 3: MLOps Pipeline (🔄 Week 3)**

**Goal:** Automatically retrain model daily using new conversation data

**What to Implement:**

#### **1. Data Extraction (Daily at 2 AM)**
```python
# scripts/extract_training_data.py
from datetime import datetime, timedelta
import pymongo

def extract_daily_data():
    """Extract yesterday's conversations from MongoDB"""
    db = connect_mongodb()
    yesterday = datetime.now() - timedelta(days=1)
    
    conversations = db.conversations.find({
        "timestamp": {"$gte": yesterday}
    })
    
    # Format as training pairs
    training_data = [
        {
            "input": conv["user_message"],
            "code": conv["user_code"],
            "language": conv["language"],
            "output": conv["groq_response"]
        }
        for conv in conversations
    ]
    
    # Save to file
    with open("data/processed/daily_train.json", "w") as f:
        json.dump(training_data, f)
    
    return len(training_data)  # Report count
```

#### **2. Training on Cloud GPU (Daily at 3 AM)**
```bash
# scripts/train_model.py
python scripts/train_cloud.py \
  --data data/processed/daily_train.json \
  --base-model "Qwen/Qwen2.5-Coder-7B-Instruct" \
  --lora-rank 32 \
  --lora-alpha 64 \
  --epochs 3 \
  --learning-rate 2e-4 \
  --output models_saved/polymentor-lora-{date} \
  --cloud-provider runpod
```

**Cloud Providers:**
- RunPod (cheapest, $0.30/GPU hour)
- Lambda Labs
- AWS SageMaker
- Google Vertex AI

#### **3. Model Evaluation (Daily at 6 AM)**
```python
# scripts/evaluate_model.py
def evaluate():
    """Compare custom model vs Groq on eval set"""
    
    custom_model = load_model("models_saved/latest")
    eval_set = load_eval_set("data/processed/eval_set.json")
    
    custom_results = {
        "accuracy": 0.87,
        "relevance": 0.91,
        "speed_ms": 120
    }
    
    groq_results = {
        "accuracy": 0.89,
        "relevance": 0.93,
        "speed_ms": 150
    }
    
    # Custom is close to Groq!
    improvement = (custom_results["accuracy"] - groq_results["accuracy"]) * 100
    
    return {
        "custom_is_better": improvement > 0,
        "improvement_percent": improvement,
        "recommend_deploy": improvement > 2
    }
```

#### **4. Conditional Deployment (Daily at 8 AM)**
```bash
# scripts/deploy_model.py
if evaluation.recommend_deploy:
    # Push to Hugging Face
    huggingface-cli upload your-org/polymentor \
      models_saved/polymentor-lora-{date} \
      . --repo-type model
    
    # Update inference server to use new checkpoint
    # Gradually route traffic: 10% custom, 90% Groq
    
    send_notification("New model deployed! 🚀")
else:
    # Keep using Groq
    send_notification("Model not ready yet, keeping Groq")
```

**Automation Options:**
1. **Cron job** (simple, on server)
2. **GitHub Actions** (free, if repo is public)
3. **Airflow** (powerful, for complex pipelines)
4. **Cloud scheduler** (GCP Cloud Scheduler, AWS EventBridge)

**Est. Time:** 3-4 days

---

### **PHASE 4: Gradual Model Takeover (🔄 Week 4+)**

**Goal:** Progressively shift from Groq to custom model

**Deployment Strategy:**

```
Week 4:  10% custom  | 90% Groq
Week 5:  30% custom  | 70% Groq
Week 6:  50% custom  | 50% Groq
Week 7:  70% custom  | 30% Groq
Week 8: 100% custom  | 0% Groq
```

**Code:**
```python
# src/inference/router.py
import random

def get_response(user_message, code, language, level):
    """Route to Groq or custom model based on traffic split"""
    
    traffic_split = {
        "groq": 0.7,      # 70% → Groq
        "custom": 0.3     # 30% → Custom model
    }
    
    choice = random.choices(
        population=["groq", "custom"],
        weights=[traffic_split["groq"], traffic_split["custom"]],
        k=1
    )[0]
    
    if choice == "groq":
        return groq_pipeline.chat(user_message, code, language, level)
    else:
        return custom_model.chat(user_message, code, language, level)
```

**Monitoring During Transition:**
- Track response quality
- Monitor user satisfaction
- Compare metrics (speed, accuracy, helpfulness)
- A/B test with different user segments

**Est. Time:** Ongoing, 4+ weeks

---

## 📊 Data Pipeline Flow

```
Day 1:
  User asks "Fix my bug"
         ↓
  Groq API responds instantly
         ↓
  Response saved to MongoDB
         ↓
  Training data accumulates ✅

Day 2-7:
  Thousands of new conversations
  MongoDB grows with real data

Day 8 (First Retraining):
  Extract 7 days of data
         ↓
  Train LoRA adapter on Cloud GPU
         ↓
  Evaluate vs Groq baseline
         ↓
  If better: Deploy new model
  If worse: Keep Groq, try again tomorrow
         ↓
  Repeat every day! 🔄

Week 4+:
  Custom model gets stronger each day
  Eventually surpasses Groq
  Users don't notice - seamless upgrade
```

---

## 🛠 Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| **Frontend** | React + Vite | Free |
| **Backend** | FastAPI (Python) | Free |
| **Live LLM** | Groq API | $0.01-0.05/1000 tokens |
| **Data Storage** | MongoDB Atlas | Free (512MB) → $10/month (shared) |
| **Training** | Cloud GPU (RunPod) | $0.30-1.00/GPU hour |
| **Model Hosting** | Hugging Face | Free |
| **Inference** | Custom GPU server | $0.30-1.00/hour (or free local) |
| **Scheduling** | GitHub Actions | Free (public repo) |

**Monthly Cost (at scale):**
- Groq API: $100-500
- MongoDB: $10-50
- Training: $200-400 (1 GPU, 2 hours/day)
- Inference: $100-200 (if self-hosted)
- **Total: ~$400-1150/month** (very reasonable!)

---

## 📈 Success Metrics

Track over time:

```
Week 1-2:
  ✅ Users chatting with Groq
  ✅ Data flowing to MongoDB
  ✅ 100+ conversations/day

Week 3:
  ✅ First model trained
  ✅ Evaluation metrics computed
  ✅ Decide: deploy or keep Groq?

Week 4-8:
  ✅ Custom model quality improving
  ✅ Response time decreasing
  ✅ User satisfaction scores increasing
  ✅ Groq dependency decreasing

Month 2+:
  ✅ Custom model beats Groq
  ✅ 80%+ traffic on custom model
  ✅ Cost per response: lower than Groq
  ✅ PolyMentor is self-improving system! 🚀
```

---

## 📚 Concepts Covered

This project teaches:

**Web Development:**
- React (frontend)
- FastAPI (backend)
- REST APIs
- Responsive design

**ML/AI:**
- LLM API integration (Groq)
- Fine-tuning (LoRA)
- Model evaluation
- A/B testing

**Data Engineering:**
- MongoDB (document DB)
- Data extraction & cleaning
- Schema design
- Querying & indexing

**MLOps:**
- Automated pipelines
- Cloud GPU training
- Model versioning
- CI/CD deployment
- Monitoring & logging

**DevOps:**
- Docker & deployment
- Environment variables
- Scheduled jobs (cron)
- Cloud infrastructure

**Software Engineering:**
- System design
- Scalability
- Monitoring
- Production-grade code

---

## 🚀 Getting Started

### Step 1: Groq Phase (This Week) ✅
```bash
cd d:\QuantumLogics\PolyMentor

# Terminal 1: Start API
uvicorn src.api.app:app --reload

# Terminal 2: Start website
cd website && npm run dev

# Visit: http://localhost:5173/
```

### Step 2: MongoDB Phase (Next Week)
```bash
# Install MongoDB locally or use MongoDB Atlas (cloud)
# Update .env:
MONGODB_URI=mongodb+srv://user:pass@cluster/polymentor

# Create schema
python scripts/setup_mongodb.py

# Update API to save chats
# Test saving conversations
```

### Step 3: MLOps Phase (Week 3)
```bash
# Create data extraction scripts
# Set up cloud GPU account (RunPod, Lambda)
# Create training pipeline
# Set up scheduling (cron/Airflow)
```

### Step 4: Custom Model Phase (Week 4+)
```bash
# Deploy inference server
# Implement traffic splitting
# Monitor metrics
# Gradually increase custom model traffic
```

---

## 💡 Key Insights

1. **Groq is the bootstrap:** Use Groq to get started fast, collect data
2. **MongoDB is the flywheel:** Every conversation makes the custom model smarter
3. **MLOps is the automation:** Train daily without manual work
4. **Gradual rollout is safe:** A/B testing lets you switch models without risk
5. **Eventually, you win:** Custom model trained on your own data > generic LLM

---

## 🎯 End Goal

**A self-improving coding tutor that:**
- Starts with Groq for instant reliability
- Learns from every user conversation
- Gets smarter daily through automated retraining
- Eventually becomes more powerful than Groq
- Remains cost-effective and scalable

**Timeline:** 4-8 weeks to full custom model deployment

---

## Next Steps

1. ✅ **DONE:** Phase 1 (Groq + chat interface)
2. 🔄 **NEXT:** Phase 2 (MongoDB integration)
   - Add MongoDB connection
   - Store conversations
   - Create schema & indexes

Ready to build Phase 2? 🚀
