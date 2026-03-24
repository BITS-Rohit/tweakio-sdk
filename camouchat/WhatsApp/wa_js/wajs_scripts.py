import json


class WAJS_Scripts:
    """
    The Vault: Contains all raw JavaScript execution strings for Playwright injection.
    All strings are wrapped in strict asynchronous Try-Catch blocks to prevent UI
    crashes and telemetry leaks to Meta.
    """

    @staticmethod
    def wrap_stealth_execution(js_code: str) -> str:
        """
        Wraps raw WPP JavaScript code for standard parameterization.
        (Wrapper logic moved to _evaluate_stealth CustomEvent bridge).
        """
        return js_code

    # --- 1. CORE & CONNECTION ---
    @classmethod
    def is_authenticated(cls) -> str:
        """Authentication script"""
        return cls.wrap_stealth_execution("wpp.conn.isAuthenticated()")

    @classmethod
    def get_chat(cls, chat_id: str) -> str:
        """Fetch extensive metadata for a specific chat by recursively dumping scalar properties."""
        js = f"""
            (() => {{
                const chat = wpp.chat.get('{chat_id}');
                if (!chat) return {{ error: "Chat not found in Meta memory." }};
                
                // Dynamically dump all primitive internal Webpack properties!
                const dump = {{}};
                for (let key in chat) {{
                    const val = chat[key];
                    if (typeof val === 'string' || typeof val === 'number' || typeof val === 'boolean') {{
                        dump[key] = val;
                    }}
                }}
                
                // Add crucial nested objects manually to prevent CloneErrors
                if (chat.id) dump["id_serialized"] = chat.id._serialized;
                if (chat.contact) {{
                    dump["contact_name"] = chat.contact.name;
                    dump["contact_pushname"] = chat.contact.pushname;
                }}
                
                return dump;
            }})()
        """
        return cls.wrap_stealth_execution(js)

    @classmethod
    def get_messages(cls, chat_id: str, count: int = 50) -> str:
        """Fetch history from active RAM"""
        js = f"""
            wpp.chat.getMessages('{chat_id}', {{ count: {count} }}).then(messages => 
                messages.map(m => ({{
                    id: m.id._serialized,
                    body: m.body,
                    type: m.type,
                    from: m.from,
                    to: m.to,
                    t: m.t,
                    isViewOnce: m.isViewOnce
                }}))
            )
        """
        return cls.wrap_stealth_execution(js)

    # --- 3. ACTIONS (TIER 3 FALLBACKS) ---
    @classmethod
    def send_text_message(cls, chat_id: str, message: str) -> str:
        """Pure API message sending"""
        safe_msg = json.dumps(message)
        return cls.wrap_stealth_execution(f"wpp.chat.sendTextMessage('{chat_id}', {safe_msg})")

    @classmethod
    def mark_is_read(cls, chat_id: str) -> str:
        return cls.wrap_stealth_execution(f"wpp.chat.markIsRead('{chat_id}')")

    # --- 4. EVENTS (THE PUSH ARCHITECTURE) ---
    @classmethod
    def setup_new_message_listener(cls, python_alias: str) -> str:
        """
        Injects the bridge that pushes new WS messages directly to the Python handler.
        Uses the hidden window hook.
        """
        return f"""(() => {{
            const wpp = window.__react_devtools_hook;
            if(!wpp || window._camou_has_listener) return false;
            wpp.on('chat.new_message', async (msg) => {{
                // Fire the Playwright-exposed python function with sterile data
                window.{python_alias}({{
                    id: msg.id._serialized,
                    body: msg.body,
                    type: msg.type,
                    from: msg.from,
                    to: msg.to,
                    t: msg.t,
                    isViewOnce: msg.isViewOnce
                }});
            }});
            window._camou_has_listener = true;
            return true;
        }})()"""
