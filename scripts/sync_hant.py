#!/usr/bin/env python3
"""從上游簡體 SKILL.md 產生繁體版 SKILL.zh-Hant.md。

需要 opencc：

    pip install opencc-python-reimplemented
    python scripts/sync_hant.py

這一步只做機械轉換，轉完一定要人工讀一次。OpenCC 的 s2tw 偶爾會把
「只」轉成「隻」、「粘贴」轉成「粘貼」，下面的 NORMALIZE 就是在修這類問題；
之後如果再發現新問題，直接加進 NORMALIZE，讓下一次同步也吃到。
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import opencc
except ImportError:  # pragma: no cover
    sys.exit("請先安裝 opencc-python-reimplemented")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "SKILL.md"
OUT = ROOT / "SKILL.zh-Hant.md"

# 轉換後的統一修正：左邊是 OpenCC 的輸出，右邊是我們要的寫法。
NORMALIZE = [
    ("臺", "台"),          # 台灣寫「台」，不寫「臺」
    ("別隻", "別只"),      # 「隻」是量詞，不是「只」
    ("儘量", "盡量"),
    ("粘貼", "貼上"),
]


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    out = opencc.OpenCC("s2tw").convert(text)
    for a, b in NORMALIZE:
        out = out.replace(a, b)
    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(out)} 字元)，請人工校訂一次")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
