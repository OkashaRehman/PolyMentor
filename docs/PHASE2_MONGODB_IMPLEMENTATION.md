# Phase 2: MongoDB Data Collection Implementation

## 🎯 Goal
Store every user conversation in MongoDB so we have training data for the custom model.

---

## 📋 Implementation Checklist

### 1. MongoDB Setup
- [ ] Create MongoDB Atlas account (free tier)
- [ ] Create cluster and database
- [ ] Get connection string
- [ ] Add to `.env` file

### 2. Database Schema
- [ ] Create `conversations` collection
- [ ] Create indexes for queries
- [ ] Create `models` collection for tracking versions

### 3. API Updates
- [ ] Add MongoDB connection to FastAPI
- [ ] Save every chat to database
- [ ] Add endpoints to retrieve chat history
- [ ] Add error handling

### 4. Testing
- [ ] Verify chats are saved
- [ ] Query conversations from DB
- [ ] Create sample eval set

### 5. Documentation
- [ ] Document schema
- [ ] Document API changes
- [ ] Create sample queries

---

## 🚀 Quick Setup (30 minutes)

### Step 1: MongoDB Atlas (Cloud - Recommended)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free)
3. Create organization & project
4. Create cluster (free tier)
5. Add database user
6. Get connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/polymentor?retryWrites=true&w=majority
   ```

### Step 2: Local MongoDB (Alternative)

```bash
# Windows - using Chocolatey
choco install mongodb-community

# Or download from https://www.mongodb.com/try/download/community

# Start MongoDB
mongod
```

### Step 3: Update .env

```env
# .env (in project root)
GROQ_API_KEY=your_key
GROQ_MODEL=llama-3.3-70b-versatile
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/polymentor?retryWrites=true&w=majority
```

---

## 📊 Database Schema

### Collection: `conversations`

```python
# Example document
{
    "_id": ObjectId("..."),
    
    # Session & User Info
    "session_id": "uuid-1234-5678",
    "user_id": None,  # Optional, for auth later
    "user_ip": "127.0.0.1",
    
    # Timestamps
    "created_at": ISODate("2026-06-08T10:30:00Z"),
    "updated_at": ISODate("2026-06-08T10:30:05Z"),
    
    # User Input
    "user_message": "Find the bug in my code",
    "user_code": "for i in range(10)\n    print(i)",
    "language": "python",
    "level": "beginner",
    
    # Groq Response
    "groq_response": "I found a syntax error...",
    "groq_model": "llama-3.3-70b-versatile",
    "response_time_ms": 245.5,
    
    # Extracted fields (for later)
    "suspected_bugs": ["Missing colon after range(10)"],
    "fixed_code": "for i in range(10):\n    print(i)",
    "lesson": "In Python, colons mark code blocks...",
    "next_steps": ["Practice with other loops"],
    
    # Quality scoring (for custom model)
    "user_satisfaction": None,  # 1-5 stars, optional
    "is_training_sample": True,
    "quality_score": None  # Computed by eval system
}
```

### Indexes (for fast queries)

```python
# Index definitions
db.conversations.create_index([("created_at", -1)])
db.conversations.create_index([("language", 1)])
db.conversations.create_index([("level", 1)])
db.conversations.create_index([("session_id", 1)])
db.conversations.create_index([
    ("created_at", -1),
    ("language", 1),
    ("level", 1)
])  # Compound index for common queries
```

---

## 💻 Code Implementation

### File: `src/database.py` (New)

```python
"""
MongoDB connection and utilities
"""

from datetime import datetime
import os
from pymongo import MongoClient
from bson import ObjectId

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "polymentor"
CONVERSATIONS_COLLECTION = "conversations"

class Database:
    def __init__(self):
        self.client = None
        self.db = None
    
    def connect(self):
        """Connect to MongoDB"""
        if not MONGODB_URI:
            print("WARNING: MONGODB_URI not set, running without database")
            return False
        
        try:
            self.client = MongoClient(MONGODB_URI)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[DATABASE_NAME]
            self._create_indexes()
            print("✅ Connected to MongoDB")
            return True
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            return False
    
    def _create_indexes(self):
        """Create indexes for queries"""
        coll = self.db[CONVERSATIONS_COLLECTION]
        coll.create_index([("created_at", -1)])
        coll.create_index([("language", 1)])
        coll.create_index([("level", 1)])
        coll.create_index([("session_id", 1)])
    
    def save_conversation(self, conversation_data):
        """Save a single conversation"""
        try:
            coll = self.db[CONVERSATIONS_COLLECTION]
            doc = {
                **conversation_data,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_training_sample": True
            }
            result = coll.insert_one(doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"❌ Error saving conversation: {e}")
            return None
    
    def get_conversations(self, query=None, limit=100):
        """Get conversations from database"""
        try:
            coll = self.db[CONVERSATIONS_COLLECTION]
            cursor = coll.find(query or {})
            return list(cursor.limit(limit).sort("created_at", -1))
        except Exception as e:
            print(f"❌ Error getting conversations: {e}")
            return []
    
    def get_conversations_by_language(self, language, limit=100):
        """Get conversations for a specific language"""
        return self.get_conversations({"language": language.lower()}, limit)
    
    def get_conversations_by_level(self, level, limit=100):
        """Get conversations for a specific level"""
        return self.get_conversations({"level": level.lower()}, limit)
    
    def get_training_data(self, days=1):
        """Get conversations from last N days (for training)"""
        from datetime import timedelta
        
        since = datetime.utcnow() - timedelta(days=days)
        query = {"created_at": {"$gte": since}}
        
        conversations = self.get_conversations(query, limit=10000)
        
        # Format as training pairs
        training_pairs = [
            {
                "input": {
                    "message": c.get("user_message", ""),
                    "code": c.get("user_code", ""),
                    "language": c.get("language", "python"),
                    "level": c.get("level", "beginner")
                },
                "output": c.get("groq_response", "")
            }
            for c in conversations
        ]
        
        return training_pairs
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()

# Global instance
db = Database()

def init_db():
    """Initialize database on startup"""
    return db.connect()
```

### File: `src/api/app.py` (Updated)

Update the existing `/chat` endpoint to save conversations:

```python
from src.database import db, init_db

# Add to startup
@app.on_event("startup")
async def startup():
    init_db()
    print("✅ PolyMentor API ready")

# Update the /chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = pipeline.chat(
        message=request.message,
        code=request.code,
        language=request.language,
        level=request.level,
    )
    
    # Save to MongoDB
    db.save_conversation({
        "session_id": request.session_id,  # Add session ID to request
        "user_message": request.message,
        "user_code": request.code,
        "language": request.language,
        "level": request.level,
        "groq_response": result.answer,
        "groq_model": result.model,
        "response_time_ms": result.elapsed_ms,
        "suspected_bugs": result.suspected_bugs,
        "fixed_code": result.fixed_code,
        "lesson": result.lesson,
        "next_steps": result.next_steps
    })
    
    return result.__dict__
```

### File: `scripts/extract_training_data.py` (New)

Extract conversations for training:

```python
"""
Extract training data from MongoDB
Run daily to prepare data for model training
"""

import json
from datetime import datetime, timedelta
import argparse
from pathlib import Path

from src.database import db

def extract_training_data(days=1, output_path="data/processed/daily_train.json"):
    """Extract conversations from last N days"""
    
    print(f"📊 Extracting training data from last {days} day(s)...")
    
    # Connect to MongoDB
    if not db.connect():
        print("❌ Cannot connect to MongoDB")
        return False
    
    # Get conversations
    training_pairs = db.get_training_data(days=days)
    
    print(f"📈 Found {len(training_pairs)} conversation pairs")
    
    if not training_pairs:
        print("⚠️  No conversations found")
        return False
    
    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save to file
    with open(output_path, "w") as f:
        json.dump(training_pairs, f, indent=2)
    
    print(f"✅ Saved training data to {output_path}")
    
    # Print statistics
    languages = {}
    levels = {}
    
    for pair in training_pairs:
        lang = pair["input"]["language"]
        lvl = pair["input"]["level"]
        languages[lang] = languages.get(lang, 0) + 1
        levels[lvl] = levels.get(lvl, 0) + 1
    
    print("\n📊 Statistics:")
    print(f"  Languages: {languages}")
    print(f"  Levels: {levels}")
    
    db.close()
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=1)
    parser.add_argument("--output", default="data/processed/daily_train.json")
    
    args = parser.parse_args()
    
    extract_training_data(days=args.days, output_path=args.output)
```

### Update: `website/src/components/ChatInterface.jsx`

Add session ID tracking:

```javascript
const [sessionId] = useState(() => {
  // Generate unique session ID
  return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
});

// In sendMessage function, add session_id:
const response = await fetch(`${API_URL}/chat`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    session_id: sessionId,  // Add this
    message: message || "Review this code",
    code: code,
    language: language,
    level: level,
  }),
});
```

---

## 🧪 Testing

### Test 1: Start Backend & Send Message

```bash
# Terminal 1
uvicorn src.api.app:app --reload

# Terminal 2
cd website && npm run dev

# Browser: Open http://localhost:5173/, click Chat
# Send a test message with code
```

### Test 2: Verify MongoDB Save

```bash
# In MongoDB Atlas or local MongoDB, run:
db.conversations.find().pretty()

# You should see your chat!
```

### Test 3: Extract Training Data

```bash
python scripts/extract_training_data.py --days 1

# Check output
cat data/processed/daily_train.json
```

---

## 📈 Expected Data Growth

```
Day 1:  10-20 conversations
Day 2:  30-50 total
Day 3:  100+ total
Week 1: 500+ conversations
Week 2: 1000+ conversations (ready for training!)
```

---

## ✅ Completion Checklist

- [ ] MongoDB setup (Atlas or local)
- [ ] `.env` updated with MONGODB_URI
- [ ] `src/database.py` created
- [ ] `src/api/app.py` updated to save chats
- [ ] Schema with indexes created
- [ ] ChatInterface updated with session ID
- [ ] Test: Send message and verify save
- [ ] `scripts/extract_training_data.py` working
- [ ] Extract data and verify format

---

## 🚀 Next Phase
Once MongoDB is collecting data (1 week of usage), move to **Phase 3: MLOps Pipeline** to start training!

---

## 📚 Useful Commands

```bash
# Test MongoDB connection
python -c "from src.database import db; db.connect(); print('✅ Connected!')"

# Extract training data
python scripts/extract_training_data.py --days 7 --output data/training/week1.json

# Count conversations
python -c "from src.database import db; db.connect(); print(db.db.conversations.count_documents({}))"

# Clear all conversations (careful!)
python -c "from src.database import db; db.connect(); db.db.conversations.delete_many({}); print('Cleared')"
```

---

## 🆘 Troubleshooting

**"MONGODB_URI not set"**
- Add to `.env` file in project root
- Verify MongoDB Atlas connection string

**"Connection refused"**
- MongoDB service not running
- Wrong connection string
- Check firewall/VPN settings

**"Data not saving"**
- Check API logs for errors
- Verify MongoDB credentials
- Test with `mongo` shell directly

**Can't extract training data**
- Make sure conversations exist in DB
- Check file permissions on `data/` folder
- Verify JSON format is correct
