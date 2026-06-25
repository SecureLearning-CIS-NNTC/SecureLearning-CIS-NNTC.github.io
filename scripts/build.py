#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "pages"

NAV = [
    ("Home", "/index.html"),
    ("Current Activities", "/pages/current-activities.html"),
    ("Past Activities", "/pages/past-activities.html"),
]


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta, body


def inline_markdown(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
        text,
    )
    return text


def markdown_to_html(markdown: str) -> str:
    blocks: list[str] = []
    paragraph: list[str] = []
    list_stack: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph = []

    def close_lists(to_level: int = 0) -> None:
        while len(list_stack) > to_level:
            blocks.append(f"</{list_stack.pop()}>")

    for raw in markdown.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            close_lists()
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            close_lists()
            level = len(heading.group(1))
            blocks.append(f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>")
            continue

        bullet = re.match(r"^(\s*)[-*]\s+(.+)$", line)
        if bullet:
            flush_paragraph()
            indent = len(bullet.group(1).replace("\t", "    "))
            level = indent // 2 + 1
            while len(list_stack) < level:
                list_stack.append("ul")
                blocks.append("<ul>")
            close_lists(level)
            blocks.append(f"<li>{inline_markdown(bullet.group(2))}</li>")
            continue

        ordered = re.match(r"^(\s*)\d+\.\s+(.+)$", line)
        if ordered:
            flush_paragraph()
            indent = len(ordered.group(1).replace("\t", "    "))
            level = indent // 2 + 1
            while len(list_stack) < level:
                list_stack.append("ol")
                blocks.append("<ol>")
            close_lists(level)
            blocks.append(f"<li>{inline_markdown(ordered.group(2))}</li>")
            continue

        close_lists()
        paragraph.append(stripped)

    flush_paragraph()
    close_lists()
    return "\n".join(blocks)


def rel_prefix(output: str) -> str:
    depth = len(Path(output).parts) - 1
    return "" if depth == 0 else "../" * depth


def render_page(meta: dict[str, str], body: str) -> str:
    output = meta.get("output", "index.html")
    prefix = rel_prefix(output)
    active = output
    nav = "\n".join(
        f'<a class="{"active" if href.lstrip("/") == active else ""}" href="{prefix}{href.lstrip("/")}">{label}</a>'
        for label, href in NAV
    )
    title = meta.get("title", "Task Force on Secure Learning")
    summary = meta.get("summary", "")
    content = markdown_to_html(body)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{html.escape(summary, quote=True)}">
    <title>{html.escape(title)} | IEEE-CIS-NNTC-TF-SL</title>
    <link rel="stylesheet" href="{prefix}assets/css/styles.css">
  </head>
  <body>
    <header class="site-header">
      <div class="nav-wrap">
        <a class="brand" href="{prefix}index.html">IEEE-CIS-NNTC-TF-SL</a>
        <nav class="site-nav" aria-label="Main navigation">
          {nav}
        </nav>
      </div>
    </header>
    <section class="hero">
      <div class="hero-inner">
        <p class="eyebrow">IEEE CIS Neural Networks Technical Committee</p>
        <h1>{html.escape(title)}</h1>
        <p class="hero-summary">{html.escape(summary)}</p>
      </div>
    </section>
    <main class="main markdown-content">
      {content}
    </main>
    <footer class="site-footer">
      <div class="footer-inner">
        <span>Task Force on Secure Learning</span>
        <span>Content maintained locally in Markdown</span>
      </div>
    </footer>
  </body>
</html>
"""


def main() -> None:
    for old in [ROOT / "index.html", ROOT / "pages"]:
        if old.is_dir():
            shutil.rmtree(old)
        elif old.exists():
            old.unlink()

    for md_file in sorted(CONTENT_DIR.rglob("*.md")):
        meta, body = parse_front_matter(md_file.read_text(encoding="utf-8"))
        output = meta.get("output")
        if not output:
            raise SystemExit(f"Missing output in {md_file}")
        target = ROOT / output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(meta, body), encoding="utf-8")
        print(f"built {output}")


if __name__ == "__main__":
    main()
