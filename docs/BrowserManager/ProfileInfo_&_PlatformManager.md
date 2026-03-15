# 📂 ProfileInfo: Your Profile's Identity Card

The `ProfileInfo` class is a simple **Data Class** that acts like an identity card for your profile. It holds all the important paths and metadata that the SDK needs to know about a specific profile (like where its messages are stored, where its cache is, and whether it's currently active).

When you create or fetch a profile using the `ProfileManager`, you get one of these objects back. You don't usually need to create it yourself manually, but it's very useful for accessing profile-specific data!

---

### 🌐 The Platform Enum

Before creating a profile, you need to decide which platform it’s for. The `Platform` enum acts like a "category" for your profile:

*   **`Platform.WHATSAPP`**: For all your WhatsApp automation and bots.
*   **`Platform.ARATTAI`**: For the Arattai messenger (experimental).

You can easily see all supported platforms in your code:
```python
from camouchat.BrowserManager import Platform
print(Platform.list_platforms())  # Returns: ['WhatsApp', 'Arattai']
```

---

### 🛠️ Attributes inside ProfileInfo

Here’s a breakdown of what’s inside your `ProfileInfo` object:

| Attribute          | Type       | Description                                                                              |
|:-------------------|:-----------|:-----------------------------------------------------------------------------------------|
| `profile_id`       | `str`      | **Required.** The unique name you gave to your profile (e.g., "Work" or "Personal").     |
| `platform`         | `Platform` | **Required.** The platform this profile belongs to (e.g., `Platform.WHATSAPP`).          |
| `is_active`        | `bool`     | Tells you if this profile is currently running in a browser.                             |
| `profile_dir`      | `Path`     | The root directory on your disk where all profile data is stored.                        |
| `database_path`    | `Path`     | The exact path to the `messages.db` (SQLite) file for this profile.                      |
| `fingerprint_path` | `Path`     | Path to the browser fingerprint file (`fingerprint.pkl`) that keeps your browser unique. |
| `encryption`       | `dict`     | Details about whether encryption is enabled and which algorithm is being used.           |
| `created_at`       | `str`      | The timestamp of when you first birthed this profile!                                    |
| `last_used`        | `str`      | When the profile was last "touched" by the SDK.                                          |

---

### 📂 Media & Cache Folders

The `ProfileInfo` also keeps track of separate folders for different types of media to keep your data organized:

*   **`media_images_dir`**: Where all those WhatsApp images go.
*   **`media_videos_dir`**: Your video storage path.
*   **`media_voice_dir`**: Path for voice notes and audio.
*   **`media_documents_dir`**: Where PDFs and documents are saved.
*   **`cache_dir`**: Temporary browser cache files (safe to clear if needed).

---

### 💡 Pro Tip
You can easily check where your profile lives on your computer by printing the `profile_dir` attribute:
```python
profile = pm_obj.get_profile(Platform.WHATSAPP, "Work")
print(f"My profile is stored at: {profile.profile_dir}")
```

This is the core "State" object of your bot. If you have this object, you have the keys to that profile's kingdom! 🗝️
