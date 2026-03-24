import asyncio
import time
from logging import Logger, LoggerAdapter
from typing import Any, Callable, Dict, Optional, Union

from playwright.async_api import Page

from camouchat.camouchat_logger import camouchatLogger
from .wajs_scripts import WAJS_Scripts
from camouchat.Exceptions.whatsapp import WAJSError


class WapiWrapper:
    """
    The Bridge connecting Playwright (Python execution space) to wa-js (Browser space).
    Parses and handles the stealth-wrapped JSON responses from WAJS_Scripts.
    """

    def __init__(self, page: Page, log: Optional[Union[LoggerAdapter, Logger]] = None):
        self.log = log or camouchatLogger
        self.page = page
        self.wpp_handle = None

    async def _evaluate_stealth(self, js_string: str) -> Any:
        """
        Executes a Stealth JS script securely in the Main World using an Event-Bridged Injection.
        This flawlessly handles async Promises and evades all isolated-world traps.
        """
        import uuid
        req_id = f"camou_{uuid.uuid4().hex}"

        # We construct an isolated-world script that listens for a CustomEvent,
        # then injects a Main World script that executes the logic and fires the CustomEvent!
        bridge_script = f"""() => {{
            return new Promise((resolve) => {{
                // 1. Listen in the Isolated World for the result
                window.addEventListener('{req_id}', (e) => {{
                    resolve(e.detail);
                }}, {{ once: true }});
                
                // 2. Inject into the Main World to access hidden window hooks
                const script = document.createElement('script');
                const nonceMatch = document.querySelector('script[nonce]');
                if (nonceMatch) script.setAttribute('nonce', nonceMatch.nonce);
                
                script.textContent = `
                    (async () => {{
                        try {{
                            const wpp = window.__react_devtools_hook;
                            if (!wpp) throw new Error("Hidden WPP object is completely missing.");
                            const res = await {js_string};
                            window.dispatchEvent(new CustomEvent('{req_id}', {{ detail: {{ status: 'success', data: res }} }}));
                        }} catch (err) {{
                            window.dispatchEvent(new CustomEvent('{req_id}', {{ detail: {{ status: 'error', message: err.toString() }} }}));
                        }}
                    }})();
                `;
                document.documentElement.appendChild(script);
                script.remove();
            }});
        }}"""

        response = await self.page.evaluate(bridge_script)

        if not response or not isinstance(response, dict):
            raise WAJSError(f"Invalid stealth response format from browser: {response}")

        if response.get("status") == "error":
            err_msg = response.get("message", "Unknown JavaScript Error in wa-js execution")
            self.log.error(f"WA-JS Execution Error: {err_msg}")
            raise WAJSError(err_msg)

        return response.get("data")

    # --- 1. SETUP & CORE ---
    async def wait_for_ready(self, timeout_ms: float = 60000) -> bool:
        """Wait until `wa-js` completes Webpack hijack, then Extract and Erase"""
        import os
        import codecs
        import time
        import asyncio

        self.log.info("Injecting WPP engine and waiting for Webpack integration...")

        js_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "wppconnect-wa.js"))
        with codecs.open(js_path, "r", "utf-8") as f:
            js_code = f.read()

        start = time.time()
        injected = False
        
        while (time.time() - start) * 1000 < timeout_ms:
            try:
                # 1. Resiliently inject into the Main World if not already done
                if not injected:
                    has_global = await self.page.evaluate("mw:typeof window.WPP !== 'undefined'")
                    if not has_global:
                        try:
                            # DOM injection natively impacts the Main World regardless of isolation!
                            await self.page.evaluate('''([jsCode]) => {
                                const script = document.createElement('script');
                                const nonceMatch = document.querySelector('script[nonce]');
                                if (nonceMatch) script.setAttribute('nonce', nonceMatch.nonce);
                                script.textContent = jsCode;
                                document.documentElement.appendChild(script);
                                script.remove();
                            }''', [js_code])
                            injected = True
                        except Exception as e:
                            if "Execution context was destroyed" not in str(e):
                                self.log.warning(f"Failed to DOM inject WPP: {e}")
                    else:
                        injected = True

                # 2. Poll the integration status in Main World
                if injected:
                    is_ready = await self.page.evaluate("mw:window.WPP && window.WPP.isReady === true")
                    if is_ready:
                        # 3. SMASH AND GRAB (Non-Enumerable Cache): 
                        # Playwright JSHandles cannot cross Camoufox mw: boundaries natively without serializing.
                        # Instead, we bind the instance to an invisible, non-enumerable symbol on the Window.
                        # This completely hides it from Meta's integrity.js loop scanners!
                        await self.page.evaluate('''mw:(() => {
                            Object.defineProperty(window, "__react_devtools_hook", {
                                value: window.WPP,
                                enumerable: false,
                                configurable: true,
                                writable: true
                            });
                            delete window.WPP; 
                        })()''')
                        
                        self.log.info("WPP engine integrated! Global 'window.WPP' successfully completely annihilated and converted to stealth property.")
                        return True
            except Exception as e:
                # Context was probably destroyed by a WhatsApp navigation or reload
                if "Execution context was destroyed" in str(e):
                    injected = False
                    self.wpp_handle = None
                else:
                    self.log.warning(f"Error evaluating wpp status: {e}")

            await asyncio.sleep(0.5)

        self.log.error(f"wa-js failed to initialize before timeout.")
        raise WAJSError(f"WPP Initialization Timeout (waited {timeout_ms/1000} sec)")

    async def is_authenticated(self) -> bool:
        return await self._evaluate_stealth(WAJS_Scripts.is_authenticated())

    # --- 2. THE PUSH ARCHITECTURE (EVENTS) ---
    async def expose_message_listener(self, python_callback: Callable):
        """
        Exposes a Python handler to the browser to actively listen to WPP events.
        Zero-polling architecture.
        """
        alias = "__react_message_sync"

        # 1. Bind Python's callback to the browser's global JS space
        await self.page.expose_function(alias, python_callback)

        # 2. Tell WPP to start routing real-time WS payloads using hidden reference
        setup_script = WAJS_Scripts.setup_new_message_listener(alias)
        await self.page.evaluate("mw:" + setup_script)
        self.log.info(f"Stealth Message Push Listener activated via {alias}")

    # --- 3. DATA & ACTIONS ---
    async def get_chat(self, chat_id: str) -> Dict[str, Any]:
        return await self._evaluate_stealth(WAJS_Scripts.get_chat(chat_id))

    async def get_messages(self, chat_id: str, count: int = 50) -> list:
        return await self._evaluate_stealth(WAJS_Scripts.get_messages(chat_id, count))

    async def send_text_message(self, chat_id: str, message: str) -> Any:
        return await self._evaluate_stealth(WAJS_Scripts.send_text_message(chat_id, message))
