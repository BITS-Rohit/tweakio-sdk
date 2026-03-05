<div align="center">

# ⚡ Tweakio-SDK

### Production-Grade WhatsApp Web Automation for Python

*Anti-detection browser automation built on Playwright + Camoufox*

<br>

[![PyPI Version](https://img.shields.io/pypi/v/tweakio-sdk?style=flat-square&label=tweakio-sdk&color=22c55e)](https://pypi.org/project/tweakio-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/tweakio-sdk?style=flat-square&color=3b82f6)](https://pypi.org/project/tweakio-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-f59e0b?style=flat-square)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage->90%25-brightgreen?style=flat-square)](https://github.com/BITS-Rohit/tweakio-sdk)

<br>

[**Docs**](https://github.com/BITS-Rohit/tweakio-sdk#readme) · [**PyPI**](https://pypi.org/project/tweakio-sdk/) · [**Issues**](https://github.com/BITS-Rohit/tweakio-sdk/issues) · [**Contributing**](OSCG_CONTRIBUTOR_Guidelines.md) · [**Mentors**](OSCG_MENTORS_Guidelines.md)

</div>

---

## The Problem with WhatsApp Automation

Every existing solution fails in one of four ways:

- **Bans within hours** — Standard Selenium/Playwright scripts are fingerprinted immediately
- **Fragile selectors** — A single WhatsApp UI update breaks your entire bot
- **No production patterns** — Most tools are throwaway scripts, not maintainable software
- **Platform lock-in** — Adding Telegram means starting from scratch

Tweakio-SDK was built to solve all four.

---

## What Makes Tweakio Different

| Problem | Solution |
|---|---|
| Bot detection | **Camoufox + BrowserForge** fingerprinting — indistinguishable from human traffic |
| Breaking UI changes | **Interface-driven architecture** — only `src/WhatsApp/` ever needs updating |
| Lost messages | **Async SQLite storage** with background queue workers |
| Runtime errors | **Type-safe dataclasses** for every Chat and Message object |

> **Current:** WhatsApp Web `v0.1.5` · **Roadmap:** Telegram (Q2 2026), Instagram (Q3 2026)

---

## Installation

```bash
pip install tweakio-sdk
```

**Requirements:** Python 3.10+

```bash
# Install Playwright browsers (one-time setup)
playwright install chromium
```

---

## Quick Start

### Fetch Chats

```python
import asyncio
from BrowserManager import BrowserManager
from src.WhatsApp.login import Login
from src.WhatsApp.chat_processor import ChatProcessor
from src.WhatsApp.web_ui_config import WebSelectorConfig
from Custom_logger import logger

async def main():
    # Launch anti-detect browser
    browser = BrowserManager(headless=False)
    page = await browser.getPage()

    # Initialize UI config and login
    ui_config = WebSelectorConfig(page=page, log=logger)
    login = Login(page=page, UIConfig=ui_config, log=logger)

    # Scan QR code on first run — session saved automatically
    await login.login(save_path="./session.json")

    # Fetch up to 5 chats
    chat_processor = ChatProcessor(page=page, UIConfig=ui_config, log=logger)
    async for chat, name in chat_processor.Fetcher(MaxChat=5):
        print(f"📂 {name}")

asyncio.run(main())
```

### Message Processing with Persistent Storage

```python
import asyncio
from BrowserManager import BrowserManager
from src.WhatsApp.login import Login
from src.WhatsApp.chat_processor import ChatProcessor
from src.WhatsApp.message_processor import MessageProcessor
from src.WhatsApp.web_ui_config import WebSelectorConfig
from src.StorageDB.sqlite_db import SQLITE_DB
from Custom_logger import logger

async def main():
    browser = BrowserManager(headless=False)
    page = await browser.getPage()
    ui_config = WebSelectorConfig(page=page, log=logger)
    login = Login(page=page, UIConfig=ui_config, log=logger)
    await login.login(save_path="./session.json")

    queue = asyncio.Queue()
    async with SQLITE_DB(queue=queue, log=logger, db_path="messages.db") as storage:

        chat_processor = ChatProcessor(page=page, UIConfig=ui_config, log=logger)
        msg_processor = MessageProcessor(
            page=page,
            UIConfig=ui_config,
            chat_processor=chat_processor,
            log=logger,
            storage=storage  # Messages auto-saved to SQLite
        )

        async for chat, name in chat_processor.Fetcher(MaxChat=3):
            print(f"📂 Processing: {name}")

            messages = await msg_processor.Fetcher(chat=chat, retry=3)
            for msg in messages:
                print(f"  💬 [{msg.direction}] {msg.data_type}: {msg.raw_data[:60]}...")
                print(f"     ID: {msg.message_id}")

asyncio.run(main())
```

---

## Architecture

```
tweakio-sdk/
├── src/
│   ├── BrowserManager/         # Anti-detect Playwright + Camoufox
│   ├── WhatsApp/               # Platform-specific implementation
│   │   ├── login.py            # QR + phone number authentication
│   │   ├── chat_processor.py   # Chat fetching and navigation
│   │   ├── message_processor.py
│   │   ├── web_ui_config.py    # DOM selector definitions
│   │   └── DerivedTypes/       # Chat, Message dataclasses
│   ├── Interfaces/             # Abstract contracts (multi-platform ready)
│   ├── StorageDB/              # Async SQLite with queue workers
│   └── Exceptions/             # Custom exception hierarchy
└── tests/                      # >90% coverage on core modules
```

### Design Principles

**Interface-driven** — Every platform implements `ChatProcessorInterface` and `MessageProcessorInterface`. Swapping platforms is one file, not a rewrite.

**Dependency injection** — All classes accept a `log` parameter, making unit testing trivial.

**Async-first** — SQLite writes are non-blocking. A background queue worker handles batching so your main loop never stalls.

**Anti-detection** — Camoufox fingerprints paired with human-like typing delays make automated traffic look organic.

---

## Module Reference

| Module | What it does |
|---|---|
| `BrowserManager` | Anti-detect browser with fingerprint rotation |
| `Login` | QR code + phone number authentication, session persistence |
| `ChatProcessor` | Fetch chats, handle unread status, click navigation |
| `MessageProcessor` | Extract messages, deduplicate, filter, and store |
| `SQLITE_DB` | Async queue-powered storage with batch inserts |
| `WebSelectorConfig` | Platform-specific DOM selectors |

---

## How It Works

**Message Processing Flow**

```
ChatProcessor.Fetcher()
  → yields Chat objects

MessageProcessor.Fetcher(chat)
  → clicks chat, extracts raw DOM nodes
  → wraps each as whatsapp_message dataclass
  → deduplicates against previous runs

SQLITE_DB async queue
  → background writer batches inserts every N seconds
```

**Anti-Detection Stack**

```
Playwright  →  Camoufox (fingerprint patching)  →  BrowserForge (realistic device profiles)
```

---

## Contributing

Contributions are welcome. **Vibe coding accepted** — if it works and it's clean, we'll merge it.

### Workflow

```bash
# Setup
git clone https://github.com/BITS-Rohit/tweakio-sdk.git
cd tweakio-sdk
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest --cov=src

# Create your feature branch
git checkout -b feature/your-feature-name
```

### Rules

1. **Fork → Branch → PR** — no direct pushes to `main`
2. **AI-assisted code is welcome** — just disclose it in your PR description
3. **Tests required** for new features — maintain >90% coverage on core modules
4. **Type hints required** — we run `mypy` in CI

### PR Template

```markdown
## What does this PR do?
[Description]

## AI Disclosure
- [ ] This PR includes AI-generated code (Claude / GPT / Copilot)
- [ ] This PR is fully human-written

## Testing
- [ ] Added / updated tests
- [ ] All tests pass locally
```

---

## Roadmap

### v0.1.6 — Core Infrastructure
- [ ] Custom Logger improvements
- [ ] Multi-account handling
- [ ] BrowserManager enhancements
- [ ] Dependency injection & interface renewal
- [ ] Directory structure improvements
- [ ] Separate browser logging

### v0.1.7 — Security & Stability
- [ ] Encryption & decryption module
- [ ] KeyBox integration
- [ ] Stability target: 60–70% reliability

### v0.1.8 — Quality Assurance
- [ ] Test coverage increase & logic improvements
- [ ] Web-UI refinements

### v0.2.0 — Multi-Platform
- [ ] Telegram or Instagram integration
- [ ] Platform-agnostic architecture

---

## FAQ

**Will I get banned?**
Tweakio uses Camoufox anti-detection. With reasonable rate limiting, bans are rare. Always test on a disposable account first.

**Can I use this for spam?**
No. This SDK is for legitimate automation — customer support, archiving, notifications. Spam violates WhatsApp ToS and is not supported.

**Why not just use the WhatsApp Business API?**
The Business API restricts message templates and requires approval workflows. Tweakio is for developers who need full control over their automation.

---

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

**[PyPI](https://pypi.org/project/tweakio-sdk/)** · **[GitHub](https://github.com/BITS-Rohit/tweakio-sdk)** · **[Report a Bug](https://github.com/BITS-Rohit/tweakio-sdk/issues)**

*Built with ❤️ by BITS-Rohit and the Tweakio community*

</div>
