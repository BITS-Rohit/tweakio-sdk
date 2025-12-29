from setuptools import setup, find_packages

setup(
    name="tweakio-SDK",
    version="0.1.4",
    description="High-performance, anti-detection WhatsApp automation SDK. Features async SQLite storage, rate limiting, and human-like interaction loops.",
    author="Rohit",
    author_email="",  # Update with actual email if known, else leave blank or placeholder
    packages=find_packages(),
    py_modules=[
        "ChatLoader", 
        "MessageProcessor", 
        "Extra", 
        "Storage", 
        "directory", 
        "Errors", 
        "Reply", 
        "Shared_Resources", 
        "login", 
        "selector_config", 
        "unread_handler", 
        "_Humanize", 
        "_Media"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Playwright",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8", install_requires=['playwright']
)
