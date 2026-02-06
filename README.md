# Tweakio-SDK

> **Production-Grade WhatsApp Web Automation for Python**  
> _Anti-detection browser automation built on Playwright + Camoufox._

[![PyPI - Version](https://img.shields.io/pypi/v/tweakio-sdk?label=tweakio-sdk)](https://pypi.org/project/tweakio-sdk/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tweakio-sdk)](https://pypi.org/project/tweakio-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Test Coverage](https://img.shields.io/badge/coverage-%3E90%25-brightgreen)](https://github.com/BITS-Rohit/tweakio-sdk)

**[Documentation](https://github.com/BITS-Rohit/tweakio-sdk#readme)** · **[PyPI](https://pypi.org/project/tweakio-sdk/)** · **[Issues](https://github.com/BITS-Rohit/tweakio-sdk/issues)** · **[Contributing](#contributing)**

---

## 🔴 The Problem

WhatsApp automation is broken:

1. **Detection & Bans** — Standard Selenium/Playwright scripts are fingerprinted and banned within hours
2. **Fragile Scripts** — When WhatsApp updates its UI, your selectors break. You spend weeks patching instead of building
3. **No Production Patterns** — Most automation tools are throwaway scripts, not production software with proper architecture
4. **Platform Lock-In** — Want to add Telegram later? Start from scratch

**The industry treats automation as disposable code. We don't.**

---

## 💡 The Solution

**Tweakio-SDK** is a WhatsApp automation framework built with production-grade patterns:

| Problem | Tweakio Solution |
|---------|------------------|
| Detection | **Camoufox + BrowserForge** fingerprinting (indistinguishable from humans) |
| Fragile selectors | **Interface-driven architecture** — when WhatsApp breaks, only `src/WhatsApp/` needs updates |
| No persistence | **Async SQLite storage** with background queue workers |
| No typing | **Type-safe dataclasses** for Chat and Message objects |

**Current**: WhatsApp Web (v0.1.5)  
**Roadmap**: Telegram (Q2 2026), Instagram (Q3 2026)

---

## 📦 Installation

```bash
pip install tweakio-sdk
```

**Requirements**: Python 3.10+, Playwright browsers

```bash
# Install Playwright browsers (one-time)
playwright install chromium
```

---

## ⚡ Quick Start

### Basic: Fetch Chats

```python
import asyncio
from src.BrowserManager import BrowserManager
from src.WhatsApp.login import Login
from src.WhatsApp.chat_processor import ChatProcessor
from src.WhatsApp.web_ui_config import WebSelectorConfig
from Custom_logger import logger

async def main():
    # 1. Launch anti-detect browser
    browser = BrowserManager(headless=False)
    page = await browser.getPage()
    
    # 2. Initialize UI config and Login
    ui_config = WebSelectorConfig(page=page, log=logger)
    login = Login(page=page, UIConfig=ui_config, log=logger)
    
    # 3. Login (scan QR code on first run)
    await login.login(save_path="./session.json")
    
    # 4. Fetch chats
    chat_processor = ChatProcessor(page=page, UIConfig=ui_config, log=logger)
    async for chat, name in chat_processor.Fetcher(MaxChat=5):
        print(f"📂 Chat: {name}")

asyncio.run(main())
```

### Advanced: Message Processing with Storage

```python
import asyncio
from src.BrowserManager import BrowserManager
from src.WhatsApp.login import Login
from src.WhatsApp.chat_processor import ChatProcessor
from src.WhatsApp.message_processor import MessageProcessor
from src.WhatsApp.web_ui_config import WebSelectorConfig
from src.StorageDB.sqlite_db import SQLITE_DB
from Custom_logger import logger

async def main():
    # Browser + Login setup (same as above)
    browser = BrowserManager(headless=False)
    page = await browser.getPage()
    ui_config = WebSelectorConfig(page=page, log=logger)
    login = Login(page=page, UIConfig=ui_config, log=logger)
    await login.login(save_path="./session.json")
    
    # Initialize async storage
    queue = asyncio.Queue()
    async with SQLITE_DB(queue=queue, log=logger, db_path="messages.db") as storage:
        
        # Initialize processors
        chat_processor = ChatProcessor(page=page, UIConfig=ui_config, log=logger)
        msg_processor = MessageProcessor(
            page=page,
            UIConfig=ui_config,
            chat_processor=chat_processor,
            log=logger,
            storage=storage  # Messages auto-saved to SQLite
        )
        
        # Fetch and process messages
        async for chat, name in chat_processor.Fetcher(MaxChat=3):
            print(f"📂 Processing: {name}")
            
            # Fetcher returns wrapped Message objects with deduplication
            messages = await msg_processor.Fetcher(chat=chat, retry=3)
            
            for msg in messages:
                print(f"   💬 {msg.data_type}: {msg.raw_data[:50]}...")
                print(f"      ID: {msg.message_id}")
                print(f"      Direction: {msg.direction}")

asyncio.run(main())
```

---

## 🏗️ Architecture

```
tweakio-sdk/
├── src/
│   ├── BrowserManager/     # Anti-detect Playwright + Camoufox
│   ├── WhatsApp/           # Platform-specific implementation
│   │   ├── login.py        # QR + Phone authentication
│   │   ├── chat_processor.py
│   │   ├── message_processor.py
│   │   ├── web_ui_config.py  # Selector definitions
│   │   └── DerivedTypes/   # Chat, Message dataclasses
│   ├── Interfaces/         # Abstract contracts (for future platforms)
│   ├── StorageDB/          # Async SQLite with queue workers
│   └── Exceptions/         # Custom exception hierarchy
└── tests/                  # >90% coverage on core modules
```

### Key Design Decisions

- **Interface-Driven**: Every platform implements `ChatProcessorInterface`, `MessageProcessorInterface`, etc.
- **Dependency Injection**: All classes accept `log` parameter for testability
- **Async-First**: Non-blocking SQLite writes, background queue workers
- **Anti-Detection**: Camoufox fingerprints + human-like typing delays

---

## 📊 Modules

| Module | Description |
|--------|-------------|
| **BrowserManager** | Anti-detect browser with fingerprint rotation |
| **Login** | QR code + phone number authentication |
| **ChatProcessor** | Fetch chats, handle unread status, click navigation |
| **MessageProcessor** | Extract messages, deduplicate, filter, store |
| **SQLITE_DB** | Async queue-powered storage with batch inserts |
| **WebSelectorConfig** | Platform-specific DOM selectors |

---

## 🛠️ How It Works

### Message Processing Flow

```
1. ChatProcessor.Fetcher() → yields Chat objects
2. MessageProcessor.Fetcher(chat) → clicks chat, extracts messages
3. Messages wrapped as whatsapp_message dataclass
4. New messages enqueued to SQLITE_DB async queue
5. Background writer batches inserts every N seconds
```

### Anti-Detection Stack

```
Playwright (base) → Camoufox (fingerprint) → BrowserForge (realistic profiles)
```

---

## 🤝 Contributing

We welcome contributions! **Vibe coding accepted** — if it works and is clean, we'll merge it.

### Contribution Rules

1. **Fork → Branch → PR** workflow required
2. **AI-Assisted code is welcome** — just mention it in your PR description for transparency
3. **Tests required** for new features (we maintain >90% coverage on core modules)
4. **Type hints required** — we use `mypy` for static analysis

### Quick Start for Contributors

```bash
# Clone and setup
git clone https://github.com/BITS-Rohit/tweakio-sdk.git
cd tweakio-sdk
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest --cov=src

# Your feature branch
git checkout -b feature/your-feature
```

### PR Template

```markdown
## What does this PR do?
[Description]

## AI Disclosure
- [ ] This PR includes AI-generated code (Claude/GPT/Copilot)
- [ ] This PR is fully human-written

## Testing
- [ ] Added/updated tests
- [ ] All tests pass locally
```

---

## 🗺️ Roadmap

### v0.1.6 — Core Infrastructure
- [ ] Custom Logger improvements
- [ ] Multi-Account Handling
- [ ] BrowserManager enhancements
- [ ] Dependency Injection & Interface renewal
- [ ] Directory structure improvements
- [ ] Separate Browser Logging

### v0.1.7 — Security & Stability
- [ ] Encryption & Decryption module
- [ ] KeyBox integration
- [ ] Stability & Decryptor additions
- [ ] Stability increase → 60-70% reliability

### v0.1.8 — Quality Assurance
- [ ] Test coverage increase & logic improvements
- [ ] Web-UI tinkering & refinements

### v0.2.0 — Multi-Platform (Coming Soon)
- [ ] Another Platform integration (Telegram/Instagram)
- [ ] Platform-agnostic architecture

---

## ❓ FAQ

**Q: Will I get banned?**  
A: Tweakio uses Camoufox anti-detection. With reasonable rate limiting, bans are rare. Always test on disposable accounts first.

**Q: Can I use this for spam?**  
A: No. This SDK is for legitimate automation (customer support, archiving, notifications). Spam violates WhatsApp ToS and is not supported.

**Q: Why not just use the WhatsApp Business API?**  
A: Business API has message template restrictions and approval processes. Tweakio is for developers who need full control.

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 🔗 Links

- **PyPI**: [pypi.org/project/tweakio-sdk](https://pypi.org/project/tweakio-sdk/)
- **GitHub**: [github.com/BITS-Rohit/tweakio-sdk](https://github.com/BITS-Rohit/tweakio-sdk)
- **Issues**: [Report bugs](https://github.com/BITS-Rohit/tweakio-sdk/issues)

---

**Keywords**: tweakio, tweakio-sdk, whatsapp automation, whatsapp bot python, whatsapp api, web automation, playwright, browser automation, chatbot, messaging, anti-detection, camoufox

_Built with ❤️ by BITS-Rohit and the Tweakio community_
