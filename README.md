<div style="text-align: center;">
  <img src="./assets/text.png" alt="CamouChat Text" />
</div>

> [!IMPORTANT]  
> 🦊 **This is the CamouChat Core SDK Repository.**  
> If you are looking for the main CamouChat project, full ecosystem documentation, or the WhatsApp plugin, please visit our **[Central Repository](https://github.com/CamouChat-Team/CamouChat)**.

**`camouchat-core`** is the foundational SDK package. It provides the strict asynchronous interfaces (`typing.Protocol`), end-to-end encrypted storage engines (`AES-GCM-256`), and standardized logging systems used by all CamouChat plugins.

<p align= "center">
  <a href="https://pypi.org/project/camouchat/">
      <img src="https://img.shields.io/pypi/v/camouchat?label=camouchat-core&color=green" />
  </a>
  <a href="https://opensource.org/licenses/MIT">
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

---

## Core SDK Features

* **Interface-First Design**: Pure `typing.Protocol` contracts for seamless cross-plugin interoperability.
* **Encrypted Storage Pipeline**: Built-in 256-bit AES-GCM encryption bridging abstract messages to SQLAlchemy.
* **Database Agnostic**: `SQLAlchemyStorage` supports SQLite, PostgreSQL, and MySQL completely natively.
* **Unified Metadata**: Centralized enums (`Platform`, `StorageType`, `MediaType`) ensures consistency.
* **Concurrent Logging**: Automatic structured, thread-safe, colored console & rotating file logging via `LoggerFactory`.

---

## Installation

```bash
uv add camouchat-core
```
*(If you are building an agent, you likely want to install `camouchat-whatsapp` instead, which includes this core SDK automatically).*

---

## Installation

> 🚀 CamouChat v0.7 is on PyPI

### Using `uv` (Recommended)

```bash
uv add camouchat-core
```

> If installing the full stack with browser support:
```bash
uv add camouchat-whatsapp "camoufox[geoip]"
uv run python -m camoufox fetch
```

### Using `pip`

```bash
pip install camouchat-core
```

> If installing with full browser + WhatsApp support:
```bash
pip install camouchat-whatsapp "camoufox[geoip]"
python -m camoufox fetch
```

> [!WARNING]
> `camoufox fetch` downloads the hardened Firefox binary used by [Camoufox](https://camoufox.com/). This is a **one-time setup step** and cannot be automated via `uv sync`.

---

## Documentation & Community

- 👉 [Core SDK Docs](https://github.com/CamouChat-Team/camouchat-core/tree/main/docs)
- 👉 [Browser Plugin](https://github.com/CamouChat-Team/camouchat-browser)
- 👉 [Browser Plugin Docs](https://github.com/CamouChat-Team/camouchat-browser/tree/main/docs)
- 👉 [WhatsApp Plugin](https://github.com/CamouChat-Team/camouchat-whatsapp)
- 👉 [WhatsApp Plugin Docs](https://github.com/CamouChat-Team/camouchat-whatsapp/tree/main/docs)
- 👉 [Code of Conduct](https://github.com/CamouChat-Team/camouchat-core/blob/main/CODE_OF_CONDUCT.md)
- 👉 [Changelog](https://github.com/CamouChat-Team/camouchat-core/releases)

---

## Roadmap

### v0.7 — Plugin Architecture
- Decoupled `core`, `browser`, and `whatsapp` packages
- Centralized logging via `LoggerFactory`
- Standardized Protocol contracts


## FAQ

**Will I get banned?**
Rare but possible. Use rate limiting. Avoid spam. Soft bans (logout) are more common than number bans.

**Can I use this for spam?**
No. Use at your own risk.

**Why not WhatsApp Business API?**

* Template restrictions
* Approval process
* Costs per message
* Limited flexibility

---

## License

MIT — see [LICENSE](https://github.com/CamouChat-Team/camouchat-core/blob/main/LICENSE)

---

## ⚖️ Security & Ethics

CamouChat's strict policy regarding acceptable automation, anti-spam, and stealth disclaimers can be found in our central ecosystem hub:

👉 **[SECURITY.md](https://github.com/CamouChat-Team/CamouChat/blob/main/SECURITY.md)**

## Thanks to all the Contributors

<!-- readme: contributors -start -->
<table>
	<tbody>
		<tr>
            <td align="center">
                <a href="https://github.com/BITS-Rohit">
                    <img src="https://avatars.githubusercontent.com/u/125949183?v=4" width="60;" alt="BITS-Rohit"/>
                    <br />
                    <sub><b>Ivy </b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/bibhupradhanofficial">
                    <img src="https://avatars.githubusercontent.com/u/77357902?v=4" width="60;" alt="bibhupradhanofficial"/>
                    <br />
                    <sub><b>Bibhu Pradhan</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/xinss-plus">
                    <img src="https://avatars.githubusercontent.com/u/260048405?v=4" width="60;" alt="xinss-plus"/>
                    <br />
                    <sub><b>Xinss</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Adez017">
                    <img src="https://avatars.githubusercontent.com/u/142787780?v=4" width="60;" alt="Adez017"/>
                    <br />
                    <sub><b>aditya singh rathore</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/AnkithaMadhyastha">
                    <img src="https://avatars.githubusercontent.com/u/174180608?v=4" width="60;" alt="AnkithaMadhyastha"/>
                    <br />
                    <sub><b>AnkithaMadhyastha</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/dharapandya85">
                    <img src="https://avatars.githubusercontent.com/u/109461918?v=4" width="60;" alt="dharapandya85"/>
                    <br />
                    <sub><b>Dhara Pandya </b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Vaishnav-Sabari-Girish">
                    <img src="https://avatars.githubusercontent.com/u/88036970?v=4" width="60;" alt="Vaishnav-Sabari-Girish"/>
                    <br />
                    <sub><b>Vaishnav-sabari-girish</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/OVERDOZZZE">
                    <img src="https://avatars.githubusercontent.com/u/113797353?v=4" width="60;" alt="OVERDOZZZE"/>
                    <br />
                    <sub><b>Saparbekov Nurdan</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/magic-peach">
                    <img src="https://avatars.githubusercontent.com/u/146705736?v=4" width="60;" alt="magic-peach"/>
                    <br />
                    <sub><b>Akanksha Trehun</b></sub>
                </a>
            </td>
		</tr>
	<tbody>
</table>
<!-- readme: contributors -end -->

---

<p align="center">
  Built with ❤️ by BITS-Rohit and the CamouChat community
</p>
