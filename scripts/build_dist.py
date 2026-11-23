#!/usr/bin/env python3
"""把 skill 正文壓成聊天框可以直接貼上的一段 prompt，並檢查字數預算與關鍵規則。

兩個版本共用一支腳本：

- v1：來源 `SKILL.zh-Hant.md`，輸出 `dist/grok-agent.zh-Hant.txt`
- v2：來源 `v2/SKILL.md`，輸出 `v2/dist/grok-agent.zh-Hant.txt`

`SKILL.md` 是上游簡體原文，保持原樣以便與上游合併；繁體版另存為
`SKILL.zh-Hant.md`（由 scripts/sync_hant.py 產生＋人工校訂）。

用法：

    python scripts/build_dist.py          # 重新生成所有生成檔
    python scripts/build_dist.py --check  # 只校驗，不改檔案（CI 用這個）

手寫檔案（custom instructions、起手式）不會被覆蓋，只檢查預算與關鍵規則。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 生成檔案的頭部：補上聊天框缺失的「觸發條件」和「語言」兩件事，
# 因為聊天框沒有 description 索引層。
HEADER_V1 = """人情世故（中國語境高情商回應）

【啟用時機】用戶貼出對話紀錄、會議原話、飯局或家族群對話，或問「這句怎麼回」「怎麼婉拒」「怎麼說才得體」「會不會得罪人」時，按下面規則處理。與關係溝通無關的請求（寫程式、查資料、算數）正常回答，不要套用這套風格，也不要主動說教。

【語言】用中文回答，跟隨用戶語體：用戶用繁體／粵語書面，就用繁體；用戶用簡體，就用簡體。

"""

HEADER_V2 = """人情世故 v2（互動版）

【啟用時機】用戶貼出對話紀錄、問「點回／點拒絕／點開口／會唔會得罪人」，或要處理關係、面子、邊界時使用。與人際無關的請求（寫程式、查資料、算數）正常回答，不要套用，也不要主動說教。

【語言】用中文回答，跟隨用戶語體：繁體／粵語書面就繁體，簡體就簡體。預設香港 register，見正文「設定」一節。

"""

# 每個交付物都必須保留的骨架。刪掉任何一條，扁平版就不再是同一個 skill。
TARGETS = [
    {
        "name": "v1",
        "source": "SKILL.zh-Hant.md",
        "out": "dist/v1/grok-agent.zh-Hant.txt",
        "header": HEADER_V1,
        "budget": 4000,
        "markers": ["先接住", "公開給面子", "說死", "留證據", "紅線"],
    },
    {
        "name": "v2",
        "source": "v2/SKILL.md",
        "out": "dist/v2/grok-agent.zh-Hant.txt",
        "header": HEADER_V2,
        "budget": 4000,
        "markers": ["五格", "第二手", "開場", "提醒", "紅線"],
    },
]

# 手寫檔：只檢查預算和標記，不生成、不覆蓋。
HANDWRITTEN = {
    "dist/v1/grok-custom-instructions.zh-Hant.txt": (
        4000,
        ["先接住", "公開給面子", "說死", "留證據", "紅線"],
    ),
}

# 起手式只是外殼，本身不含規則，所以只檢查它有沒有叫對方去跟 skill 全文。
BOOTSTRAP = "dist/v1/chat-bootstrap.zh-Hant.md"


def load_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit(f"{path} 缺少 YAML 頭部")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{path} 的 YAML 頭部沒有閉合")
    body = parts[2].lstrip("\n")
    if not body:
        raise SystemExit(f"{path} 正文為空")
    return body


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只校驗，不寫檔案")
    args = ap.parse_args()

    problems: list[str] = []

    for target in TARGETS:
        src = ROOT / target["source"]
        out = ROOT / target["out"]
        if not src.exists():
            problems.append(f"{target['source']} 不存在")
            continue

        content = target["header"] + load_body(src)

        if args.check:
            current = out.read_text(encoding="utf-8") if out.exists() else ""
            if current != content:
                problems.append(
                    f"{target['out']} 與 {target['source']} 不同步，"
                    "請執行 python scripts/build_dist.py"
                )
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8")
            print(f"wrote {target['out']}")

        size = len(content)
        status = "ok" if size <= target["budget"] else "OVER"
        print(f"{target['out']}: {size} 字元 / 上限 {target['budget']} [{status}]")
        if size > target["budget"]:
            problems.append(
                f"{target['out']} 超出預算 {size - target['budget']} 字元"
            )

        missing = [m for m in target["markers"] if m not in content]
        if missing:
            problems.append(
                f"{target['out']} 缺少關鍵規則: {', '.join(missing)}"
            )

    for rel, (limit, markers) in HANDWRITTEN.items():
        path = ROOT / rel
        if not path.exists():
            problems.append(f"{rel} 不存在")
            continue
        text = path.read_text(encoding="utf-8")
        size = len(text)
        status = "ok" if size <= limit else "OVER"
        print(f"{rel}: {size} 字元 / 上限 {limit} [{status}]")
        if size > limit:
            problems.append(f"{rel} 超出預算 {size - limit} 字元")
        missing = [m for m in markers if m not in text]
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
