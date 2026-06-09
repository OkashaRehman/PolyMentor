# 🚀 PolyMentor - Quick Start (5 Minutes)

## Your AI Coding Chatbot is Ready!

I've built a **complete, working chat interface** for your PolyMentor project.

---

## ⚡ Start in 3 Steps

### **Terminal 1: Start the API**
```powershell
cd d:\QuantumLogics\PolyMentor
uvicorn src.api.app:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### **Terminal 2: Start the Website**
```powershell
cd d:\QuantumLogics\PolyMentor\website
npm install
npm run dev
```

You should see:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

### **Step 3: Open Browser**
Go to:
```
http://localhost:5173/
```

Click the **"Chat"** button in the navigation bar!

---

## 🎯 Use the Chat

1. **Select Language** - Python, JavaScript, Java, etc.
2. **Select Level** - Beginner, Intermediate, or Advanced
3. **Paste Code** (optional) - Your buggy or confusing code
4. **Ask Question** - "Find the bug", "Explain this", etc.
5. **Send** - Get instant AI response with fixes and lessons!

---

## 📋 What You Get

Response includes:
- ✅ Direct answer to your question
- 🐛 Suspected bugs (if any)
- 💻 Fixed code (with copy button)
- 📚 Lesson (why the bug happened)
- 🎯 Next steps (practice suggestions)
- ⏱️ Response time

---

## 🔧 Troubleshooting

**"Connection refused" or "API Error"?**
- Make sure Terminal 1 (API) is still running
- Check `http://127.0.0.1:8000` in browser - should show JSON

**"npm not found"?**
- Install Node.js from https://nodejs.org

**Styles look weird?**
- Refresh browser (Ctrl+F5)
- Check browser console (F12) for errors

---

## 📁 Files I Created

**For the Chat Interface:**
- `website/src/components/ChatInterface.jsx` - Main chat UI
- `website/src/components/ChatMessage.jsx` - Message display
- `website/src/components/CodeBlock.jsx` - Code display with copy
- `website/src/styles/ChatInterface.css` - Chat styling
- `website/src/styles/ChatMessage.css` - Message styling
- `website/src/styles/CodeBlock.css` - Code styling
- `website/.env` - API configuration

**Updated:**
- `website/src/App.jsx` - Added `/chat` route
- `website/package.json` - Added `react-markdown` dependency

---

## 🚀 Next (Optional)

**Deploy to the internet:**
- Backend: Railway, Render, Heroku
- Frontend: Vercel, Netlify
- Update `website/.env` with production API URL

**Add more features:**
- User accounts & login
- Chat history storage
- File uploads
- Dark mode

---

## 💡 Tips

- **Keyboard shortcut**: Press `Enter` to send message (or Shift+Enter for new line)
- **Copy code**: Click the "Copy" button on any code block
- **Different languages**: Try Python, JavaScript, Java, C++, Go, Rust, etc.
- **Progressive complexity**: Start with "beginner", move to "advanced" as you learn

---

## ✨ You Now Have

✅ Full-stack AI coding tutor  
✅ Beautiful web interface  
✅ 16+ programming languages  
✅ Real Groq API integration  
✅ Professional UI with animations  
✅ Mobile-responsive design  
✅ Error handling & loading states  

---

**Ready?** Open two terminals and follow the 3 steps above! 🎉

Questions? Check `website/WEBSITE_SETUP.md` for detailed docs.
