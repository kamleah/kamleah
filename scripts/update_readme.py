#!/usr/bin/env python3
"""Refresh the GitHub-activity section of README.md from the public GitHub API.

Rewrites everything between <!--GH_ACTIVITY:START--> and <!--GH_ACTIVITY:END-->.
Standard library only. Set GITHUB_TOKEN (Actions provides it) to avoid rate limits.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import urllib.request
from collections import Counter
from pathlib import Path

USER = os.environ.get("GH_USER", "kamleah")
README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!--GH_ACTIVITY:START-->", "<!--GH_ACTIVITY:END-->"
RECENT_LIMIT = 6


def api(path: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": f"{USER}-profile-readme"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_repos() -> list[dict]:
    repos: list[dict] = []
    page = 1
    while True:
        batch = api(f"/users/{USER}/repos?per_page=100&type=owner&sort=pushed&page={page}")
        repos += batch
        if len(batch) < 100:
            return repos
        page += 1


def cell(text: str | None, limit: int = 90) -> str:
    text = (text or "").replace("|", "/").replace("\n", " ").strip()
    if not text:
        return "-"
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def bar(share: float, width: int = 16) -> str:
    filled = round(share * width)
    return "█" * filled + "░" * (width - filled)


def render(user: dict, repos: list[dict], today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    own = [r for r in repos if not r["fork"] and r["name"].lower() != USER.lower()]
    stars = sum(r["stargazers_count"] for r in own)
    since = int(user["created_at"][:4])

    langs = Counter(r["language"] for r in own if r.get("language"))
    total = sum(langs.values())
    lang_rows = [
        f"| {name} | `{bar(count / total)}` | {count / total:.0%} |"
        for name, count in langs.most_common(6)
    ] if total else []

    recent = sorted(own, key=lambda r: r["pushed_at"], reverse=True)[:RECENT_LIMIT]
    repo_rows = [
        f"| [{r['name']}]({r['html_url']}) | {cell(r['description'])} | {r.get('language') or '-'} | {r['pushed_at'][:10]} |"
        for r in recent
    ]

    out = [
        f"**{len(own)}** original public repositories &nbsp;|&nbsp; **{stars}** stars earned "
        f"&nbsp;|&nbsp; **{user['followers']}** followers &nbsp;|&nbsp; on GitHub since **{since}**",
        "",
    ]
    if lang_rows:
        out += ["**Languages across my repositories**", "", "| Language | Share | |", "| --- | --- | --: |", *lang_rows, ""]
    if repo_rows:
        out += ["**Recently active repositories**", "", "| Repository | About | Language | Last push |", "| --- | --- | --- | --- |", *repo_rows, ""]
    out.append(f"<sub>Updated automatically on {today.isoformat()} by a GitHub Action.</sub>")
    return "\n".join(out)


def main() -> None:
    user = api(f"/users/{USER}")
    block = f"{START}\n{render(user, fetch_repos())}\n{END}"
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        raise SystemExit("Markers not found in README.md")
    README.write_text(pattern.sub(lambda _: block, text), encoding="utf-8")


if __name__ == "__main__":
    main()
