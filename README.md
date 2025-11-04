# ALIAS - Advanced Learning Intelligence Assistant System

**The Ultimate FREE AI Companion - Now with Built-In AI Engine!**

ALIAS is your complete digital assistant with **zero costs forever**:
- **Built-in AI Engine** - No external APIs needed!
- **Voice Interaction** with wake word detection
- **Academic Tutoring** across all subjects  
- **Professional Productivity** assistance
- **Creative Writing** support
- **Programming Help**
- **Personal Life Management**
- **Entertainment**

**One `alias.py` file + custom AI engine - no API keys, no costs, no limits!**

## Quick Start

```bash
# Clone and run
git clone https://github.com/daemonw628-ops/ALIAS.git
cd ALIAS
python alias.py

# Or start in a specific mode:
python alias.py study      # Start in Study mode
python alias.py work       # Start in Work mode
python alias.py creative   # Start in Creative mode
python alias.py tech       # Start in Tech mode
python alias.py personal   # Start in Personal mode
python alias.py fun        # Start in Fun mode
```

**Windows:** Just double-click `run.bat`

### Important: What You Get Out-of-the-Box

Running `python alias.py` immediately gives you:
- **A fully functional AI engine** (built by us!)
- **Intelligent context understanding** using embeddings
- **Learning from conversations** - gets smarter over time
- **Knowledge base** that grows with each interaction
- **Works 100% offline** - no internet required
- **Zero dependencies on external AI services**

**This is REAL AI, not just keyword matching!**

### Want Even More Power?

Our built-in engine is great, but you can add MORE:

```bash
# Option 1: Install Ollama (for GPT-like models)
# Download from: https://ollama.ai
ollama pull llama2
# Then run alias.py - it will use Ollama when available

# Option 2: Install Transformers (advanced models)
pip install transformers torch
# Downloads ~500MB-2GB of AI models

# Option 3: Voice features (optional)
pip install SpeechRecognition pyttsx3 pyaudio
```

**Our built-in engine works great standalone. These are just optional enhancements!**

##  Features

###  **Built-In Free AI Engine**
- Sentence embedding-based understanding
- Context-aware response generation
- Learns from every conversation
- Knowledge base that grows over time
- Works 100% offline
- No external AI services needed
- Gets smarter the more you use it!

###  **What You Get Out-of-the-Box**
- Professional Tkinter GUI with dark theme
- Intelligent conversational AI
- Context understanding and memory
- 7 different modes/personalities
- Conversation history
- Session tracking
- Persistent learning

### **Optional Enhancements** (Not Required!)
- Add Ollama for GPT-like capabilities
- Install Transformers for advanced models
- Enable voice features for hands-free use

### **Zero Cost Forever**
- No API fees or subscriptions
- No usage limits  
- No external dependencies for AI
- Works completely offline
- **Built-in intelligent AI engine included!**
- Optional enhancements available (Ollama/Transformers)

###  **7 AI Modes**
- **Assistant** - General help for anything
- **Study** - Academic tutoring with subject specialization
- **Work** - Professional productivity tasks
- **Creative** - Writing and brainstorming
- **Personal** - Life management and planning
- **Tech** - Programming and debugging
- **Fun** - Entertainment and games

###  **Voice Capabilities** (Optional)
- Wake word detection ("ALIAS", "Hey ALIAS", "OK ALIAS")
- Continuous voice listening
- Text-to-speech responses
- Hands-free operation

###  **Built-in Tools**
Study, Work, Creative, Tech, Personal tools + Quick actions (web search, weather, news, system info)

##  Usage Examples

```bash
# Voice commands
"ALIAS, help me with this math problem"
"Hey ALIAS, write an email to my manager"
"OK ALIAS, explain quantum mechanics"

# Keyboard shortcuts
Ctrl+Enter - Send message
Ctrl+L     - Toggle voice listening
Ctrl+M     - Cycle through modes
F1         - Show help
```

##  System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Memory**: 512MB+ RAM
- **Microphone**: Optional, for voice features
- **Internet**: Optional with local AI models

##  Repository Structure

```
ALIAS/
├── alias.py          # Main application (entry point)
├── ai_engine.py      # Built-in Free AI Engine 🧠
├── requirements.txt  # Python dependencies (minimal)
├── LICENSE          # MIT License
├── README.md        # This file
├── run.sh           # Linux/Mac launcher
├── run.bat          # Windows launcher
└── docs/            # Additional documentation
    ├── CHANGELOG.md
    ├── CONTRIBUTING.md
    └── GITHUB_UPLOAD.md
```

**Key Files:**
- `alias.py` - The GUI and main application
- `ai_engine.py` - Our custom-built AI (the "engine"!)
- Knowledge files are created on first run (auto-saved)

##  Contributing

Contributions welcome! See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

##  License

MIT License - See [LICENSE](LICENSE) file.

##  Why ALIAS?

### What ALIAS Actually Is
**ALIAS is a complete free AI system** that includes:
- Custom-built AI engine (embeddings + retrieval + generation)
- Professional GUI for AI interaction
- Learning system that improves from conversations
- Optional connections to external AI (Ollama, Transformers)
- Voice integration setup
- **Works out-of-the-box with NO external services**

### For Students 
- Zero cost - no API subscriptions
- Actual working AI included
- Learns and helps with homework
- Privacy-focused (all local)

### For Developers 
- Real AI engine to study and modify
- Multi-backend support
- Easy to customize and extend
- Educational codebase

### For Everyone
- No payment barriers
- No internet required
- Open source and transparent
- Helps people learn and grow

---

**Making advanced AI assistance free and accessible to everyone, everywhere!**

##  How Our AI Engine Works

Our built-in AI engine uses modern techniques without requiring massive models:

1. **Sentence Embeddings** - Converts text to vectors for semantic understanding
2. **Knowledge Base** - Stores information from conversations and built-in knowledge
3. **Retrieval System** - Finds relevant information using vector similarity
4. **Response Generation** - Combines templates, context, and learned knowledge
5. **Continuous Learning** - Improves from every conversation

**It's like having a mini-GPT that runs on any computer and learns from you!**

### Technical Details
- Uses TF-IDF weighted word embeddings
- Cosine similarity for context matching
- Template-based generation with dynamic knowledge insertion
- Persistent storage (knowledge saved between sessions)
- Zero dependencies on cloud services

---

Version 1.0.0 | [Changelog](docs/CHANGELOG.md) | [GitHub](https://github.com/daemonw628-ops/ALIAS)
