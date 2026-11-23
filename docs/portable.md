# 在其他 AI 上使用

English speakers: see [portable.en.md](portable.en.md).

本倉庫的 `SKILL.md` 是按 [Agent Skills](https://agentskills.io) 格式寫的：YAML 頭部 + Markdown 正文，靠 `description` 裡的觸發詞被 agent 索引，需要時整份載入。

支援這個格式的工具（Claude Code、Grok Build、Muse Code 等）**零改動**就能用。只有「沒有檔案系統的聊天框」需要把 skill 壓成一段 prompt —— `dist/` 就是為這種情況準備的。

## 繁體與簡體的處理

- `SKILL.md` 保持上游簡體原文，方便與上游合併。
- `SKILL.zh-Hant.md` 是繁體版，由 `scripts/sync_hant.py` 轉換（OpenCC s2tw）＋人工校訂，內容與上游逐句對應。
- `dist/` 內所有檔案都是繁體，由繁體版產生。

## 平台對照

| 平台 | 支援 SKILL.md | 放在哪 / 怎麼用 | 用哪個檔案 |
|---|---|---|---|
| **Grok Build**（CLI） | 支援，且相容 Claude Code 佈局 | `~/.grok/skills/renqing-shigu/` 或專案內 `.grok/skills/`；也可直接放 `~/.claude/skills/` | 原 `SKILL.md` 或 `SKILL.zh-Hant.md` |
| **Muse Code**（Meta 開發者 agent） | 支援 | `~/.agents/skills/renqing-shigu/`、`$XDG_CONFIG_HOME/muse/skills`，或 `~/.claude/skills/` | 同上 |
| **Grok 網頁 / X app** | 不支援 | Settings → Customize → Custom Instructions，或新建一個 Custom Agent | `dist/grok-custom-instructions.zh-Hant.txt`（約 1,300 字）|
| **Meta Muse app** | 不支援安裝 | 新開對話，貼上 `dist/chat-bootstrap.zh-Hant.md` 並附上 skill 全文 | `dist/chat-bootstrap.zh-Hant.md` |
| **ChatGPT / Gemini / Claude 網頁** | 不支援 | 同上；Claude 的 Project instructions、ChatGPT 的 Custom Instructions 都可以 | `dist/chat-bootstrap.zh-Hant.md` |

## 安裝

```bash
# Grok Build
git clone https://github.com/HarryW00/renqing-shigu-skill ~/.grok/skills/renqing-shigu

# Muse Code（同時也能被 Grok Build 與 Claude Code 讀到）
git clone https://github.com/HarryW00/renqing-shigu-skill ~/.agents/skills/renqing-shigu
```

驗證：

```bash
muse skills list            # 應能看到 renqing-shigu
```

Grok Build 裡輸入 `/skills` 打開擴充面板，或直接 `/renqing-shigu` 呼叫。專案級共用請放到倉庫裡的 `.grok/skills/` 或 `.agents/skills/`，隨程式碼一起提交。

## 為甚麼需要扁平化版本

一份 skill 能「按需載入」，靠的是三樣東西；聊天框三樣都沒有：

1. **索引層** —— `name` + `description` 讓 agent 判斷該不該載入。聊天框沒有這一層，所以扁平版開頭必須寫清「甚麼時候啟用、甚麼時候不要啟用」，否則它會對着一句「幫我寫個 Python 腳本」也跟你講「先接住人，再處理事情」。
2. **檔案系統** —— 原 skill 的 `references/theory.md`、`references/cases.md` 是按需讀取的。聊天框讀不到，所以扁平版把五項判斷、五條原則、場景速查全部內聯。
3. **長度預算** —— Grok 的 Custom Instructions 大約 4,000 字元（以介面計數為準）。`SKILL.zh-Hant.md` 正文 3,401 字，去掉 YAML 頭部後加上一段啟用說明正好塞得進；`grok-custom-instructions.zh-Hant.txt` 則是更短的一版，留給需要和別的人設共存的場景。

`SKILL.md` 本身沒有 script、沒有工具呼叫、正文也沒有引用任何檔案路徑，所以扁平化只需要刪頭部、補觸發條件，判斷邏輯一句沒改。

## 兩個容易踩的坑

- **別把全域 Custom Instructions 當成「安裝完成」。** 它是帳號級的，會影響之後每一個對話。想「只在這類問題生效」，要麼建一個專用 Custom Agent，要麼用短版並保留「無關請求不要套用」那句。
- **聊天框不會記住。** 換一個對話就要重新貼一次。想「裝一次、到處用」，走 Muse Code / Grok Build 那條路。

## 給二次修改的人

- 想改判斷規則：改 `SKILL.md`（簡體，上游原文），必要時同步 `SKILL.zh-Hant.md`。
- 想改繁體用字：把規則加進 `scripts/sync_hant.py` 的 `NORMALIZE`，再跑一次，免得下次同步又被 OpenCC 改回去。
- 改完跑：

```bash
python scripts/build_dist.py          # 重新生成 dist/grok-agent.zh-Hant.txt
python scripts/build_dist.py --check  # 只檢查，CI 用的就是這個
```

`dist/grok-custom-instructions.zh-Hant.txt` 和 `dist/chat-bootstrap.zh-Hant.md` 是手寫的，腳本只檢查字數預算，不覆蓋內容。

## 已知限制

字數、結構和「該保留的規則是否都在」由 `scripts/build_dist.py` 機械校驗；實際回覆質素取決於模型，同一份 prompt 在 Grok 和 Muse 上會有差別。歡迎貼出跑偏的例子開 issue。
