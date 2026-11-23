#!/usr/bin/env python3
"""把 SKILL.zh-Hant.md 壓成聊天框可以直接貼上的一段 prompt，並檢查字數預算。

為甚麼來源不是 SKILL.md：SKILL.md 是上游簡體原文，保持原樣以便與上游合併；
繁體版另存為 SKILL.zh-Hant.md（由 scripts/sync_hant.py 產生＋人工校訂）。

用法：

    python scripts/build_dist.py          # 重新生成 dist/grok-agent.zh-Hant.txt
    python scripts/build_dist.py --check  # 只校驗，不改檔案（CI 用這個）

dist/grok-custom-instructions.zh-Hant.txt 與 dist/chat-bootstrap.zh-Hant.md
是手寫的，腳本不會覆蓋，只檢查預算和關鍵規則有沒有被刪掉。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "SKILL.zh-Hant.md"

# 生成檔案的頭部：補上聊天框缺失的「觸發條件」和「語言」兩件事，
# 因為聊天框沒有 description 索引層。
HEADER = """人情世故（中國語境高情商回應）

【啟用時機】用戶貼出對話紀錄、會議原話、飯局或家族群對話，或問「這句怎麼回」「怎麼婉拒」「怎麼說才得體」「會不會得罪人」時，按下面規則處理。與關係溝通無關的請求（寫程式、查資料、算數）正常回答，不要套用這套風格，也不要主動說教。

【語言】用中文回答，跟隨用戶語體：用戶用繁體／粵語書面，就用繁體；用戶用簡體，就用簡體。

"""

# 每個交付物都必須保留的判斷骨架。刪掉任何一條，扁平版就不再是同一個 skill。
REQUIRED = [
    "先接住",
    "公開給面子",
    "說死",
    "留證據",
    "紅線",
]

# 字元預算。Grok 的 Custom Instructions 大約 4,000 字元，留一點餘量。
BUDGETS = {
    "dist/grok-agent.zh-Hant.txt": 4000,
    "dist/grok-custom-instructions.zh-Hant.txt": 4000,
}

GENERATED = ["dist/grok-agent.zh-Hant.txt"]
HANDWRITTEN = ["dist/grok-custom-instructions.zh-Hant.txt"]

# 起手式只是外殼，本身不含規則，所以只檢查它有沒有叫對方去跟 skill 全文。
BOOTSTRAP = "dist/chat-bootstrap.zh-Hant.md"


def load_body() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"{SOURCE.name} 缺少 YAML 頭部")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{SOURCE.name} 的 YAML 頭部沒有閉合")
    body = parts[2].lstrip("\n")
    if not body:
        raise SystemExit(f"{SOURCE.name} 正文為空")
    return body


def render() -> str:
    return HEADER + load_body()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校驗，不寫檔案")
    args = ap.parse_args()

    problems: list[str] = []

    target = ROOT / "dist/grok-agent.zh-Hant.txt"
    content = render()
    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != content:
            problems.append(
                "dist/grok-agent.zh-Hant.txt 與 SKILL.zh-Hant.md 不同步，"
                "請執行 python scripts/build_dist.py"
            )
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}")

    for rel, limit in BUDGETS.items():
        path = ROOT / rel
        if not path.exists():
            problems.append(f"{rel} 不存在")
            continue
        size = len(path.read_text(encoding="utf-8"))
        status = "ok" if size <= limit else "OVER"
        print(f"{rel}: {size} 字元 / 上限 {limit} [{status}]")
        if size > limit:
            problems.append(f"{rel} 超出預算 {size - limit} 字元")

    for rel in GENERATED + HANDWRITTEN:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        missing = [m for m in REQUIRED if m not in text]
        if missing:
            problems.append(f"{rel} 缺少關鍵規則: {', '.join(missing)}")

    boot = ROOT / BOOTSTRAP
    if boot.exists() and "SKILL" not in boot.read_text(encoding="utf-8"):
        problems.append(f"{BOOTSTRAP} 沒有指示對方貼上 SKILL 全文")

    if problems:
        print("\n校驗失敗：", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print("\n全部通過")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
