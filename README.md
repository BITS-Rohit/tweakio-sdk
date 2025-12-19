# 🚀 Tweakio-Whatsapp Library

> **The Developer-First WhatsApp Automation Toolkit**  
> _Built on Playwright, Camoufox & BrowserForge for maximum reliability and undetectability._

---

This repository provides a powerful, modular toolkit for **WhatsApp automation**. Unlike standard libraries, Tweakio is designed for **modern, human-like interactions**, ensuring safety and longevity for your automation pipelines.

Whether you are building a smart chatbot, an automated alert system, or a workflow for your business, Tweakio gives you the granular control you need.

---

## ✨ Features

*   **🛡️ Anti-Detection First**: Built on **Playwright + Camoufox** to mimic real browser fingerprints.
*   **🧩 Modular Architecture**: Components like `ChatRoller`, `MessageLoader`, and `BrowserManager` work together or standalone.
*   **🤖 Human-Like Behavior**: Simulates natural typing speeds, mouse movements, and pauses.
*   **📡 SQLite Integration**: Built-in persistence for message history and state management.
*   **⚡ Dynamic Selectors**: Smart element detection that adapts to WhatsApp Web UI changes.

---

## 📦 Installation

```bash
pip install tweakio-SDK
```

_Note: Requires Python 3.8+_

_Currently we are supporting Whatsapp Web but in future we will add more support to different platforms_
---

## ⚡ Quick Start

Here is a complete, working example to login and start listening for messages:

```python
import asyncio
from tweakio_whatsapp import BrowserManager, WhatsappLogin, MessageLoader, ChatLoader

async def main():
    # 1️⃣ Initialize Browser with Anti-Detect capabilities
    browser_manager = BrowserManager(headless=False)
    page = await browser_manager.getPage()

    # 2️⃣ Perform Login (Scan QR Code if needed)
    wp_login = WhatsappLogin(page=page)
    await wp_login.login()

    # 3️⃣ Start Message Loader & Chat Loader
    loader = MessageLoader(page=page)
    chat_loader = ChatLoader(page=page)

    print("🚀 Listening for messages...")

    # 4️⃣ Iterate through chats and fetch messages
    async for chat, name in chat_loader.ChatRoller(cycle=1, MaxChat=3):
        print(f"📂 Checking Chat: {name}")
        
        async for msg, text, success, data in loader.LiveMessages(
            chat_id=chat, 
            cycle=3  # Check for 3 cycles of live updates
        ):
            print(f"   📩 New Message: {text}")

if __name__ == "__main__":
    asyncio.run(main())
```

> **💡 Pro Tip:** Check `test/play.py` in the repository for a more advanced example including chat navigation!

---

## 🛠️ Modules Overview

| Module | Description |
| :--- | :--- |
| **BrowserManager** | Handles browser creation, fingerprinting, and proxy management. |
| **WhastappLogin** | Manages QR scanning, session saving, and login verification. |
| **MessageLoader** | Fetches historical and live messages with duplicate protection. |
| **Storage** | SQLite wrapper for efficient message storage and retrieval. |
| **ChatRoller** | Automates scrolling and loading old chats. |

---

## 🤝 Contributing

We welcome contributions! If you have ideas for new features or bug fixes:

1.  Fork the repo 🍴
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request 🚀

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

_Made with passion by the Tweakio Team_
