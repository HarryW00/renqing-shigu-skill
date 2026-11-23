<div align="center">

# 人情世故.skill
### 繁體版 · 互動版

> 「中國語境下的高情商，不是會來事，是既把事辦了，也把人安頓好。」

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)
[![Fork](https://img.shields.io/badge/Fork-of%20IvyYang1999-blue)](https://github.com/IvyYang1999/renqing-shigu-skill)

</div>

---

這是 [IvyYang1999/renqing-shigu-skill](https://github.com/IvyYang1999/renqing-shigu-skill) 的 fork。上游教你**把一句話講得體**；這個 fork 做三件事：

1. **繁體版** —— 全文繁體，另分香港與大陸兩種 register。
2. **可以直接貼進聊天框** —— Grok 網頁、Meta Muse、ChatGPT 這類讀不到檔案的介面，有現成扁平版。
3. **v2 互動版（實驗中）** —— 由「潤色一句話」升級成「判斷局勢、給第二手、揀渠道、留痕」。

上游 `SKILL.md` 一字未改，所以這個 fork 仍然可以同上游合併。

## 五分鐘上手

| 你手上有的 | 怎樣做 |
|---|---|
| Claude Code / Grok Build / Muse Code | `git clone https://github.com/HarryW00/renqing-shigu-skill ~/.agents/skills/renqing-shigu` |
| 只有網頁版（Grok、Muse、ChatGPT） | 貼上 `dist/v1/grok-custom-instructions.zh-Hant.txt`（1,321 字元） |
| 想自己改規則 | 改 `SKILL.md` 或 `v2/SKILL.md`，再跑 `python scripts/build_dist.py` |

## v1 與 v2

| | **v1**（穩定） | **v2**（候選） |
|---|---|---|
| 判斷方式 | 七個場景規則 | 五個變量：權力差、依賴方向、觀眾、可逆性、未來互動 |
| 動作 | 換措辭 | 換措辭、改結構、改規則 |
| 輸出 | 一句話＋備選＋解釋 | 六段：判斷、句子、第二手、渠道、留痕、提醒 |
| 適合 | 即時回一句 | 多輪、重複發生、要主動開場 |
| 扁平版 | 3,580 字元 | 2,353 字元 |
| 狀態 | 可直接用 | [PR #1](https://github.com/HarryW00/renqing-shigu-skill/pull/1)，八條對照未跑完 |

v2 補上的三塊：

- **第二手** —— 對方否認意圖、施壓、情緒、搵中間人、公開將軍、翻舊帳，各有回應骨架。
- **開場** —— 求助、提反對、劃界、修補、拒絕前、事後收口。
- **提醒** —— 每次回覆結尾一句「AI 睇唔到全貌，你自己再斟酌」；高風險場景加「先確認三問」。

## 同一個場景，兩版怎樣答

同事第三次叫你頂夜更。

**v1**

> 你開口我肯定想幫，但這次確實接不住；勉強答應，後面做不到反而更耽誤你。

**v2**

> **判斷**：對等同事、他求你、第三次、私下。目標唔止拒一次，而係斷「每次問你」呢個模式。
>
> **可以直接用**：「阿 Ken，今次我真係接唔到。之前兩次係咁啱我鬆啲，我唔想做成慣例 — 以後排更嘅事你直接同阿頭講，唔好預我。」
>
> **第二手**：「吓，之前又得？」→「之前得係因為情況唔同，我唔想每次都解釋一次。」
>
> **渠道**：私下文字，今日內，唔好等到佢問第三次。
>
> **提醒**：以上係按你講嘅情況推嘅，實際關係同語氣你自己再斟酌。

差別唔在形容詞，在**動作** — v2 換嘅係關係均衡。

## 安裝

### CLI（Claude Code / Grok Build / Muse Code）

```bash
# v1
git clone https://github.com/HarryW00/renqing-shigu-skill ~/.agents/skills/renqing-shigu

# v2（名稱為 renqing-shigu-v2，可與 v1 並存）
git clone https://github.com/HarryW00/renqing-shigu-skill /tmp/renqing
cp -R /tmp/renqing/v2 ~/.agents/skills/renqing-shigu-v2

muse skills list     # 應見到 renqing-shigu 與 renqing-shigu-v2
```

Grok Build 裡面輸入 `/skills`，或直接 `/renqing-shigu`。

### 聊天框

| 平台 | 用哪個檔案 |
|---|---|
| Grok 網頁 / X app | `dist/v1/grok-custom-instructions.zh-Hant.txt`，貼入 Custom Instructions 或專用 Custom Agent |
| Meta Muse app | `dist/v1/chat-bootstrap.zh-Hant.md` ＋ skill 全文 |
| ChatGPT / Gemini / Claude 網頁 | 同上 |

分平台步驟、字數上限、踩坑記錄：[docs/portable.zh-Hant.md](docs/portable.zh-Hant.md) · [English](docs/portable.en.md)

## 專案結構

```text
.
├── SKILL.md                     # 上游簡體原文，v1 本體（未改動）
├── SKILL.zh-Hant.md             # v1 繁體版（OpenCC + 人工校訂）
├── v2/
│   ├── SKILL.md                 # v2 互動版
│   └── references/              # 第二手、register、開場例句
├── dist/
│   ├── v1/                      # 可直接貼上：Custom Instructions、起手式、全文
│   └── v2/                      # 可直接貼上：v2 全文
├── docs/                        # 平台說明、v2 設計稿
├── evals/                       # 上游案例測試 + v2 對抗案例
├── references/                  # 上游理論與真實案例
├── examples/                    # 上游速查
└── scripts/                     # 繁體同步、扁平版生成與校驗
```

## 開發

```bash
python scripts/build_dist.py          # 生成 dist/v1 與 dist/v2
python scripts/build_dist.py --check  # 只校驗，CI 用的就是這個
python scripts/sync_hant.py           # 上游更新後重新產生繁體版（需 opencc）
```

- v1 的規則只改 `SKILL.md`；改完要同步繁體版，否則 CI 會紅。
- 繁體用字修正請加進 `sync_hant.py` 的 `NORMALIZE`，否則下次同步會被 OpenCC 改回去。
- v2 直接用繁體寫，沒有同步問題。
- 扁平版有字數預算（4,000 字元）和關鍵規則標記，兩個都由腳本檢查。

## 人情世故是什麼

不是教 AI 變油滑，而是理解三件互相糾纏的事：

| 維度 | 核心問題 | 在表達上的體現 |
|---|---|---|
| **關係** | 你和對方是什麼關係，之後仲要唔要來往？ | 唔止睇字面，要睇角色同後續 |
| **面子** | 這句話會唔會令人當場落唔到台？ | 公開場合先顧體面，問題私下講 |
| **人情** | 今次邊個幫邊個，之後要唔要留餘地？ | 可以拒絕，但唔好堵死條路 |

一句話：**在關係網絡裡，用合適的體面和邊界，把事情推進。** 唔係永遠順着人，而係先接住對方、再表達自己；公開給面子、私下講條件；講得清拒絕，但唔把人講死。

## 案例與測試

- 上游五個真實案例：[`references/cases.md`](references/cases.md)、[`evals/case-tests.md`](evals/case-tests.md)
- v2 八條對抗案例與評分方法：[`evals/v2-adversarial.md`](evals/v2-adversarial.md)

## 致謝與授權

規則、案例與原始說明來自 [IvyYang1999](https://github.com/IvyYang1999/renqing-shigu-skill)，功勞屬於原作者。上游 README 的簡體原文可在該倉庫閱讀，本頁是按新結構重寫的繁體版。

上游的表達形式參考過 [同事.skill](https://github.com/titanwings/colleague-skill)、[前任.skill](https://github.com/titanwings/ex-skill)、[老板.skill](https://github.com/nicepkg/boss-skill)、[女娲.skill](https://github.com/alchaincyf/nuwa-skill)。

[MIT](LICENSE)
