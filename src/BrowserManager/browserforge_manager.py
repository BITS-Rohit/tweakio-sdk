"""
Fingerprint generation and management for BrowserForge.

Handles creating, loading, and persisting browser fingerprints
that match the system's actual screen dimensions.
"""
import json
import logging
import os
import pickle
from pathlib import Path
from typing import Tuple

from browserforge.fingerprints import Fingerprint, FingerprintGenerator

from src.Exceptions.base import BrowserException
from src.Interfaces.browserforge_capable_interface import BrowserForgeCapable


class BrowserForgeCompatible(BrowserForgeCapable):
    """
    Manages fingerprint generation and persistence.

    Ensures fingerprint matches real system screen size.
    Reuses saved fingerprint for account stability.
    """

    def __init__(self, log: logging.Logger = None) -> None:
        if log is None:
            raise BrowserException("Logger must be provided")

        self.log = log

    def get_fg(self, profile_path: Path) -> Fingerprint:
        """
        Load existing fingerprint if present.
        Otherwise generate and persist a new compatible fingerprint.
        """

        if not profile_path.exists():
            raise BrowserException("Fingerprint path does not exist")

        if profile_path.stat().st_size > 0:
            with open(profile_path, "rb") as fh:
                return pickle.load(fh)

        fg = self.__gen_fg__()

        with open(profile_path, "wb") as fh:
            pickle.dump(fg, fh)

        return fg

    def __gen_fg__(self) -> Fingerprint:
        gen = FingerprintGenerator()
        real_w, real_h = self.get_screen_size()

        if real_w <= 0 or real_h <= 0:
            raise BrowserException("Invalid screen dimensions")

        tolerance = 0.1
        attempt = 0

        while True:
            fg = gen.generate()
            w, h = fg.screen.width, fg.screen.height
            attempt += 1

            if (
                abs(w - real_w) / real_w < tolerance
                and abs(h - real_h) / real_h < tolerance
            ):
                self.log.info(
                    f"[OK] Fingerprint matched screen size: {w}x{h}"
                )
                return fg

            self.log.warning(
                f"[RETRY] Fingerprint mismatch ({w}x{h}) vs ({real_w}x{real_h}) attempt {attempt}"
            )

            if attempt >= 10:
                self.log.warning(
                    "Max attempts reached. Using last generated fingerprint."
                )
                return fg


    @staticmethod
    def get_screen_size() -> Tuple[int, int]:
        """
        Returns the width and height of the primary display in pixels.
        Supports Windows, Linux (X11), and macOS.
        """
        import platform

        system = platform.system()

        # ---------------- Windows ----------------
        if system == "Windows":
            try:
                import ctypes
                user32 = ctypes.windll.user32
                try:
                    user32.SetProcessDPIAware()
                except Exception:
                    pass  # older Windows versions

                return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

            except Exception as e:
                raise BrowserException("Windows screen size detection failed") from e

        # ---------------- Linux ----------------
        elif system == "Linux":
            try:
                import subprocess

                out = subprocess.check_output(
                    ["xdpyinfo"], stderr=subprocess.DEVNULL
                ).decode()

                for line in out.splitlines():
                    if "dimensions:" in line:
                        dims = line.split()[1].split("x")
                        return int(dims[0]), int(dims[1])

                raise BrowserException("xdpyinfo did not return screen dimensions")

            except Exception as e:
                raise BrowserException("Linux screen size detection failed") from e

        # ---------------- macOS ----------------
        elif system == "Darwin":
            try:
                import Quartz

                display = Quartz.CGMainDisplayID()
                return (
                    Quartz.CGDisplayPixelsWide(display),
                    Quartz.CGDisplayPixelsHigh(display),
                )

            except Exception as e:
                raise BrowserException("macOS screen size detection failed") from e

        # ---------------- Unsupported OS ----------------
        else:
            raise BrowserException(f"Unsupported OS for screen size detection: {system}")

    @staticmethod
    def get_fingerprint_as_dict(saved_fingerprint_path: Path) -> dict:
        if not saved_fingerprint_path.exists():
            raise BrowserException("saved_fingerprint_path does not exist")

        if not saved_fingerprint_path.is_file():
            raise BrowserException("saved_fingerprint_path is not a file")

        if os.stat(saved_fingerprint_path).st_size == 0:
            raise BrowserException("saved_fingerprint_path is empty")

        try:
            with open(saved_fingerprint_path, encoding="utf-8") as f:  # default opens in reading mode.
                data = json.load(f)

            if not isinstance(data, dict):
                raise BrowserException("Fingerprint JSON is not a valid dict")

            return data

        except json.JSONDecodeError as e:
            raise BrowserException(f"Invalid fingerprint JSON format: {e}")

        except Exception as e:
            raise BrowserException(f"Failed to load fingerprint JSON: {e}")
