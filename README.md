
# CamouChat Core 🛠️

> [!IMPORTANT]
> 🦊 **This is the CamouChat Core SDK Repository.**
> If you are looking for the main CamouChat project, full ecosystem documentation, or the WhatsApp plugin, please visit our **[Central Repository](https://github.com/CamouChat-Team/CamouChat)**.

**`camouchat-core`** is the foundational SDK package providing strict async interfaces, AES-GCM-256 encrypted storage, and structured logging used by all CamouChat plugins.

<p align="center">
  <a href="https://pypi.org/project/camouchat-core/">
      <img src="https://img.shields.io/pypi/v/camouchat-core?label=camouchat-core&color=green" />
  </a>
  <a href="https://opensource.org/licenses/MIT">
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

## Key Features

- **Interface-First Design**: Pure `typing.Protocol` contracts for seamless cross-plugin interoperability.
- **Encrypted Storage Pipeline**: Built-in AES-GCM-256 encryption bridging abstract messages to SQLAlchemy.
- **Database Agnostic**: Supports SQLite, PostgreSQL, and MySQL via `SQLAlchemyStorage`.
- **Unified Metadata**: Centralized enums (`Platform`, `StorageType`, `MediaType`) across the ecosystem.
- **Concurrent Logging**: Thread-safe, colored console & rotating file logging via `LoggerFactory`.
- **Python 3.11+**: Compatible with Python 3.11, 3.12, 3.13, and 3.14.

## Installation

```bash
uv add camouchat-core
```

Or with `pip`:

```bash
pip install camouchat-core
```

> If building a full WhatsApp agent (recommended):
> ```bash
> uv add camouchat-whatsapp "camoufox[geoip]"
> uv run python -m camoufox fetch
> ```

> [!WARNING]
> `camoufox fetch` downloads the hardened Firefox binary. This is a **one-time setup step** that cannot be automated via `uv sync`.

## Documentation

- [Core SDK Docs](https://github.com/CamouChat-Team/camouchat-core/tree/main/docs) — Contracts, storage, logging.
- [Browser Plugin](https://github.com/CamouChat-Team/camouchat-browser) — Stealth browser engine.
- [WhatsApp Plugin](https://github.com/CamouChat-Team/camouchat-whatsapp) — Full automation plugin.
- [CHANGELOG](https://github.com/CamouChat-Team/camouchat-core/blob/main/CHANGELOG.md) — Full release history.

## Roadmap

- 🌐 **More Plugins**: Signal, Telegram, and Instagram automation plugins planned.
- 🐳 **Docker**: Headless container with Xvfb and Camoufox pre-configured (Targeting v0.8.0).

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
