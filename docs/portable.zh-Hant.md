# 在其他 AI 上使用

English: [portable.en.md](portable.en.md)

本倉庫有兩條線：

- **v1**（穩定）—— 上游 skill 的繁體版。判斷清單式，輸出「一句話＋備選＋解釋」。
- **v2**（候選）—— 互動版。五個變量判斷關係，輸出六段，多了第二手、渠道、留痕和提醒。

兩者都是標準 `SKILL.md`，支援這個格式的工具（Claude Code、Grok Build、Muse Code）**零改動**就能用。只有沒有檔案系統的聊天框，才需要用 `dist/` 的扁平版。

## 平台對照

| 平台 | 讀 SKILL.md | 放在哪 / 怎麼用 | 用哪個檔案 |
|---|---|---|---|
| **Grok Build**（CLI） | 是，且相容 Claude Code 佈局 | `~/.grok/skills/<name>/` 或專案內 `.grok/skills/`；亦可用 `~/.claude/skills/` | `SKILL.md`、`SKILL.zh-Hant.md` 或 `v2/SKILL.md` |
| **Muse Code**（Meta 開發者 agent） | 是 | `~/.agents/skills/<name>/`、`$XDG_CONFIG_HOME/muse/skills`，或 `~/.claude/skills/` | 同上 |
| **Grok 網頁 / X app** | 否 | Settings → Customize → Custom Instructions，或開專用 Custom Agent | v1：`dist/v1/grok-custom-instructions.zh-Hant.txt`（1,321 字元）<br>v2：`dist/v2/grok-agent.zh-Hant.txt`（2,353 字元） |
| **Meta Muse app** | 否 | 新開對話，貼上 `dist/v1/chat-bootstrap.zh-Hant.md` 並附上 skill 全文 | `dist/v1/chat-bootstrap.zh-Hant.md` |
| **ChatGPT / Gemini / Claude 網頁** | 否 | 同上；Claude 的 Project instructions、ChatGPT 的 Custom Instructions 都可以 | 同上 |

## 安裝 v1

```bash
git clone https://github.com/HarryW00/renqing-shigu-skill ~/.grok/skills/renqing-shigu
git clone https://github.com/HarryW00/renqing-shigu-skill ~/.agents/skills/renqing-shigu   # Muse Code 也讀得到
```

驗證：`muse skills list` 應見到 `renqing-shigu`。Grok Build 裡面打 `/skills`，或直接 `/renqing-shigu`。

## 安裝 v2

```bash
git clone https://github.com/HarryW00/renqing-shigu-skill /tmp/renqing
cp -R /tmp/renqing/v2 ~/.agents/skills/renqing-shigu-v2
muse skills list        # 應見到 renqing-shigu-v2
```

v2 的名稱是 `renqing-shigu-v2`，所以可以和 v1 並存，方便對照。

## 為甚麼需要扁平版

一份 skill 能按需載入，靠三樣東西；聊天框三樣都沒有：

1. **索引層** —— `name` + `description` 讓 agent 判斷該不該載入。聊天框沒有這一層，所以扁平版開頭必須寫清「幾時啟用、幾時唔好」，否則你叫它寫 Python，它會先「接住你」。
2. **檔案系統** —— `references/` 是按需讀取的。聊天框讀不到，所以扁平版把判斷、原則、例句全部內聯；v2 更加把第二手和開場各留一句例在正文，避免指向讀不到的檔案。
3. **長度預算** —— Grok 的 Custom Instructions 大約 4,000 字元（以介面計數為準）。v1 扁平版 3,580，v2 是 2,353，兩者都塞得進。

## 兩個容易踩的坑

- **別把全域 Custom Instructions 當成「安裝完成」。** 它是帳號級的，之後每個對話都會受影響。想只在這一類問題生效，開一個專用 Custom Agent，或者用短版並保留「無關請求不要套用」那句。
- **聊天框不會記住。** 換一個對話就要重新貼。想裝一次到處用，走 Muse Code / Grok Build。

## 給二次修改的人

- 改 v1 規則：改 `SKILL.md`（上游簡體原文），再跑 `scripts/sync_hant.py` 更新繁體版。
- 改 v2 規則：直接改 `v2/SKILL.md`，它是繁體，沒有同步問題。
- 改繁體用字：把規則加進 `scripts/sync_hant.py` 的 `NORMALIZE`，否則下次同步會被 OpenCC 改回去。
- 改完跑：

```bash
python scripts/build_dist.py          # 生成 dist/v1 與 dist/v2
python scripts/build_dist.py --check  # 只檢查，CI 用的就是這個
```

`dist/v1/grok-custom-instructions.zh-Hant.txt` 和 `dist/v1/chat-bootstrap.zh-Hant.md` 是手寫的，腳本只檢查字數和規則標記，不覆蓋內容。

## 已知限制

字數、結構、關鍵規則是否還在，由 `scripts/build_dist.py` 機械校驗。實際回覆質素取決於模型，同一份 prompt 在 Grok 和 Muse 上會有差別。v2 的質素對照（八條對抗案例）未跑完，所以它仍然是候選版本。
