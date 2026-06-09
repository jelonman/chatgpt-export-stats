#!/usr/bin/env python3
"""
chatgpt_export_stats.py — get "wrapped"-style stats from your ChatGPT export.

ChatGPT lets you export your full history (Settings -> Data controls -> Export data),
which emails you a ZIP containing `conversations.json`. This script reads that file and
prints a summary of how you actually use ChatGPT: how many conversations, total messages,
your busiest months, longest chats, and more. No dependencies, nothing leaves your machine.

Usage:
    python3 chatgpt_export_stats.py conversations.json
"""
import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone

STOP = set("the a an and or but to of in on for with is are was were be been i you it that this my your "
           "me we he she they them his her our their as at by from how what why when can do does did "
           "if so not no yes will would should could have has had get got make like just want need".split())


import zipfile

def _load_export(path):
    """Load conversations from a ChatGPT export — accepts the raw .zip or conversations.json."""
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            name = next((n for n in z.namelist() if n.endswith("conversations.json")), None)
            if not name:
                raise SystemExit("No conversations.json found inside the zip.")
            with z.open(name) as f:
                return json.loads(f.read().decode("utf-8"))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _parts_to_text(content):
    if not isinstance(content, dict):
        return ""
    parts = content.get("parts")
    if isinstance(parts, list):
        return "\n".join((p if isinstance(p, str) else (p.get("text", "") if isinstance(p, dict) else "")) for p in parts).strip()
    return (content.get("text") or "").strip()


def _messages(convo):
    mapping = convo.get("mapping")
    rows = []
    if isinstance(mapping, dict):
        for node in mapping.values():
            msg = node.get("message")
            if not msg:
                continue
            role = ((msg.get("author") or {}).get("role")) or "user"
            text = _parts_to_text(msg.get("content"))
            if text and role in ("user", "assistant"):
                rows.append((role, text, msg.get("create_time")))
    else:
        for msg in convo.get("messages", []) or []:
            role = ((msg.get("author") or {}).get("role")) or msg.get("role") or "user"
            text = _parts_to_text(msg.get("content")) or (msg.get("content") if isinstance(msg.get("content"), str) else "")
            if text and role in ("user", "assistant"):
                rows.append((role, (text or "").strip(), msg.get("create_time")))
    return rows


def main():
    ap = argparse.ArgumentParser(description="Print stats from a ChatGPT conversations.json export.")
    ap.add_argument("input", help="Path to conversations.json OR the export .zip")
    ap.add_argument("--top-words", type=int, default=12, help="How many top words to show (default 12)")
    args = ap.parse_args()

    data = _load_export(args.input)
    convos = [c for c in (data if isinstance(data, list) else data.get("conversations", [data])) if isinstance(c, dict)]

    total_msgs = user_msgs = asst_msgs = 0
    months = Counter()
    weekdays = Counter()
    words = Counter()
    longest = (0, "")          # (message count, title)
    first_t = last_t = None
    user_chars = 0

    for c in convos:
        msgs = _messages(c)
        total_msgs += len(msgs)
        if len(msgs) > longest[0]:
            longest = (len(msgs), c.get("title") or "Untitled")
        for role, text, t in msgs:
            if role == "user":
                user_msgs += 1
                user_chars += len(text)
                for w in re.findall(r"[a-zA-Z']{3,}", text.lower()):
                    if w not in STOP:
                        words[w] += 1
            else:
                asst_msgs += 1
            if t:
                try:
                    dt = datetime.fromtimestamp(float(t), tz=timezone.utc)
                    months[dt.strftime("%Y-%m")] += 1
                    weekdays[dt.strftime("%A")] += 1
                    first_t = dt if first_t is None or dt < first_t else first_t
                    last_t = dt if last_t is None or dt > last_t else last_t
                except (ValueError, OSError, OverflowError):
                    pass

    n = len(convos)
    print("\n  📊  Your ChatGPT, by the numbers")
    print("  " + "─" * 38)
    print(f"  Conversations:        {n:,}")
    print(f"  Total messages:       {total_msgs:,}")
    print(f"  Your messages:        {user_msgs:,}")
    print(f"  ChatGPT replies:      {asst_msgs:,}")
    print(f"  Avg msgs/convo:       {(total_msgs / n):.1f}" if n else "  Avg msgs/convo:       0")
    print(f"  You typed ~{user_chars:,} characters (~{user_chars // 5:,} words)")
    if first_t and last_t:
        span = (last_t - first_t).days
        print(f"  Span:                 {first_t:%b %Y} → {last_t:%b %Y} ({span:,} days)")
    if longest[0]:
        print(f"  Longest conversation: {longest[0]} messages — \"{longest[1][:48]}\"")
    if months:
        top_m, cnt = months.most_common(1)[0]
        print(f"  Busiest month:        {datetime.strptime(top_m, '%Y-%m'):%B %Y} ({cnt:,} messages)")
    if weekdays:
        top_d, cnt = weekdays.most_common(1)[0]
        print(f"  Busiest weekday:      {top_d} ({cnt:,} messages)")
    if words:
        print("\n  Your most-used words:")
        for w, c in words.most_common(args.top_words):
            print(f"    {c:>5,}  {w}")
    print()


if __name__ == "__main__":
    main()
