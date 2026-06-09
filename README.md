# chatgpt-export-stats

Get **"wrapped"-style stats from your ChatGPT history** — how you actually use ChatGPT, computed
locally from your own data export. Nothing leaves your machine.

ChatGPT lets you download your full history (**Settings → Data controls → Export data**), which emails
you a ZIP with `conversations.json`. Point this script at it and get a summary:

```
  📊  Your ChatGPT, by the numbers
  ──────────────────────────────────────
  Conversations:        842
  Total messages:       9,310
  Your messages:        4,655
  ChatGPT replies:      4,655
  Avg msgs/convo:       11.1
  You typed ~612,000 characters (~122,400 words)
  Span:                 Mar 2023 → Jun 2026 (1,186 days)
  Longest conversation: 78 messages — "Debugging the deploy pipeline"
  Busiest month:        January 2026 (1,204 messages)
  Busiest weekday:      Tuesday
  Your most-used words:  python, error, function, data, why...
```

## Usage

```bash
python3 chatgpt_export_stats.py conversations.json
```

✅ Accepts the raw export **.zip** or the extracted `conversations.json`

No dependencies — Python 3 standard library only. Handles both the modern (mapping-tree) and older
(flat `messages`) export formats. Share your numbers!

## Want to actually *use* all those conversations?

Stats are fun, but the real value of your AI history is being able to find things in it. If you want
your ChatGPT (and Claude / Gemini) history **searchable** — keyword + semantic search, plus asking
questions answered from your own past chats with citations — check out
**[Backscroll](https://backscroll.xyz)**. And if you ever want to grab a *single* conversation in one
click instead of the whole export, there's **[AI Chat Exporter](https://petescribe5.gumroad.com/l/tbnxg)**.

## Part of a small suite of ChatGPT-export tools
- [chatgpt-export-to-markdown](https://github.com/jelonman/chatgpt-export-to-markdown) — turn your export into readable Markdown
- [chatgpt-export-stats](https://github.com/jelonman/chatgpt-export-stats) — wrapped-style stats from your history
- [chatgpt-export-search](https://github.com/jelonman/chatgpt-export-search) — search your history from the CLI
- [claude-export-to-markdown](https://github.com/jelonman/claude-export-to-markdown) — same, for Claude (Claude.ai) exports

## License

MIT — do whatever you like.
