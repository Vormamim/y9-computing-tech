"""Convert the raw GitBook scrape (raw/) into an MkDocs Material site (docs/ + mkdocs.yml).

Usage:
    python tools/convert_to_mkdocs.py

Reads only from raw/ - safe to re-run without touching the network.
"""

import html
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
DOCS = ROOT / "docs"
SITE_NAME = "9 Computing Technology"
HOME_SLUG = "9-computing-tech"

VIDEO_EXT = {".mp4", ".mov", ".webm", ".m4v", ".mkv"}
HINT_TYPES = {"info": "info", "success": "success", "warning": "warning", "danger": "danger", "tip": "tip"}
MARK_COLOURS = {"$warning": "#fde68a", "$danger": "#fecaca", "$info": "#bfdbfe", "$success": "#bbf7d0",
                "$primary": "#c7d2fe"}

warnings = []


def doc_path(slug):
    """GitBook slug -> path of the converted .md relative to docs/."""
    return "index.md" if slug == HOME_SLUG else f"{slug}.md"


def rel(from_doc, to_path):
    """Relative link from one docs/ file to another docs/ path."""
    return posixpath.relpath(to_path, posixpath.dirname(from_doc) or ".")


def asset_url(from_doc, to_path):
    """Relative, URL-encoded link to an asset (filenames contain spaces)."""
    return quote(rel(from_doc, to_path))


# --- block-level GitBook tags ---------------------------------------------

def indent(text, n=4):
    return "\n".join((" " * n + line) if line.strip() else "" for line in text.strip("\n").splitlines())


def convert_hints(md):
    def repl(m):
        style = HINT_TYPES.get(m.group(1), "note")
        body = m.group(2)
        # Use a leading heading as the admonition title
        title = ""
        h = re.match(r"\s*#{1,6}\s+(.+)\n", body)
        if h:
            title, body = f' "{h.group(1).strip()}"', body[h.end():]
        return f"!!! {style}{title}\n\n{indent(body)}\n"
    # innermost first so nested hints survive
    pattern = re.compile(r'\{% hint style="(\w+)" %\}((?:(?!\{% hint).)*?)\{% endhint %\}', re.S)
    while pattern.search(md):
        md = pattern.sub(repl, md)
    return md


def convert_details(md):
    pattern = re.compile(r"<details[^>]*>\s*<summary>(.*?)</summary>((?:(?!<details).)*?)</details>", re.S)

    def repl(m):
        title = BeautifulSoup(m.group(1), "html.parser").get_text().strip().replace('"', "'")
        return f'??? note "{title}"\n\n{indent(m.group(2))}\n'
    while pattern.search(md):
        md = pattern.sub(repl, md)
    return md


def convert_tabs(md):
    def tab(m):
        return f'=== "{m.group(1)}"\n\n{indent(m.group(2))}\n'
    md = re.sub(r'\{% tab title="([^"]*)" %\}(.*?)\{% endtab %\}', tab, md, flags=re.S)
    return re.sub(r"\{% (end)?tabs %\}\n?", "", md)


def convert_steppers(md):
    """Steps become numbered sections separated by rules; the stepper wrapper is dropped."""
    def stepper(m):
        steps = re.findall(r"\{% step %\}(.*?)\{% endstep %\}", m.group(1), re.S)
        return "\n\n".join(f'<div class="gb-step" markdown>\n<span class="gb-step-num">{i}</span>\n\n'
                           f"{s.strip()}\n\n</div>" for i, s in enumerate(steps, 1)) + "\n"
    return re.sub(r"\{% stepper %\}(.*?)\{% endstepper %\}", stepper, md, flags=re.S)


def convert_code(md):
    def repl(m):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        fence, body = m.group(2), m.group(3)
        extra = []
        if "title" in attrs:
            extra.append(f'title="{attrs["title"].replace(chr(92), "")}"')
        if attrs.get("lineNumbers") == "true":
            extra.append('linenums="1"')
        return f"{fence} {' '.join(extra)}".rstrip() + body
    return re.sub(r"\{% code([^%]*)%\}\s*(```\w*)(.*?```)\s*\{% endcode %\}", repl, md, flags=re.S)


# --- embeds, files, assets --------------------------------------------------

def drive_id(url):
    m = re.search(r"/d/([\w-]{20,})", url) or re.search(r"[?&]id=([\w-]{20,})", url)
    return m.group(1) if m else None


def youtube_id(url):
    q = parse_qs(urlparse(url).query)
    if "v" in q:
        return q["v"][0]
    m = re.search(r"youtu\.be/([\w-]+)|/embed/([\w-]+)", url)
    return m and (m.group(1) or m.group(2))


def embed_block(url, caption, entry, doc):
    kind = entry["kind"] if entry else "other"
    local = [f"assets/{p}" for p in (entry or {}).get("local", [])]
    label = caption or None

    if kind == "youtube" and youtube_id(url):
        return (f'<div class="video-wrapper"><iframe src="https://www.youtube-nocookie.com/embed/{youtube_id(url)}" '
                f'title="{html.escape(label or "YouTube video")}" allowfullscreen></iframe></div>'
                + (f"\n\n*{label}*" if label else ""))

    if kind == "drive":
        gid = drive_id(url)
        if local and Path(local[0]).suffix.lower() not in VIDEO_EXT:
            name = label or Path(local[0]).name.split("__", 1)[-1]
            return (f"[:material-file-download: {name}]({asset_url(doc, local[0])}){{ .md-button }} "
                    f"[:material-google-drive: Open in Google Drive]({url})")
        # videos (too big for GitHub; backed up in raw/drive) and undownloadable files
        # play through Drive's own preview player
        return (f'<div class="video-wrapper"><iframe src="https://drive.google.com/file/d/{gid}/preview" '
                f'allow="autoplay" allowfullscreen></iframe></div>' + (f"\n\n*{label}*" if label else ""))

    if kind.startswith("google-"):
        what = {"google-presentation": "Google Slides", "google-document": "Google Doc",
                "google-spreadsheets": "Google Sheet"}.get(kind, "Google file")
        parts = [f"[:material-open-in-new: {label or 'Open in ' + what}]({url}){{ .md-button }}"]
        for p in local:
            parts.append(f"[:material-file-download: {Path(p).suffix[1:].upper()}]({asset_url(doc, p)}){{ .md-button }}")
        return " ".join(parts)

    return f"[:material-link-variant: {label or url}]({url})"


def convert_embeds(md, embeds, doc):
    def repl(m):
        url = html.unescape(m.group(1)).strip("<>")
        caption = (m.group(2) or "").strip()
        return embed_block(url, caption, embeds.get(url), doc) + "\n"
    md = re.sub(r'\{% embed url="([^"]+)" %\}\n?(?:(.*?)\{% endembed %\})?', repl, md, flags=re.S)
    return md


def convert_files(md, files, doc):
    def repl(m):
        entry = files.get(m.group(1), {})
        if "local" not in entry:
            warnings.append(f"{doc}: file {m.group(1)} was not downloaded")
            return m.group(0)
        path = f"assets/{entry['local']}"
        name = Path(path).name.split("__", 1)[-1]
        return f"[:material-file-download: {name}]({asset_url(doc, path)}){{ .md-button }}"
    return re.sub(r'\{% file src="([^"]+)" %\}(?:.*?\{% endfile %\})?', repl, md, flags=re.S)


def localise_assets(md, files, images, doc):
    for key, entry in list(files.items()) + list(images.items()):
        if "local" in entry and key in md:
            # markdown-escaped query strings ('\&token=...') trail past the captured key
            md = re.sub(re.escape(key) + r'(?:\\&[^\s)"\]]*)?',
                        asset_url(doc, f"assets/{entry['local']}").replace("\\", "\\\\"), md)
        elif key in md and not key.startswith("/files/"):
            warnings.append(f"{doc}: asset not downloaded {key[:80]}")
    return md


def convert_marks(md):
    def repl(m):
        style = m.group(1)
        for token, colour in MARK_COLOURS.items():
            style = style.replace(token, colour)
        return f'<mark style="{style}">'
    return re.sub(r'<mark style="([^"]*)">', repl, md)


# --- links -------------------------------------------------------------------

def convert_links(md, slugs, aliases, base, doc):
    """Absolute or site-relative links to course pages -> relative .md links."""
    site_path = urlparse(base).path  # /9-computing-tech
    md = md.replace(base, site_path)

    def repl(m):
        slug = re.sub(r"\.md$", "", (m.group(1) or "").strip("/"))
        slug = aliases.get(slug, slug)
        if slug not in slugs:
            warnings.append(f"{doc}: unknown internal link {m.group(0)}")
            return m.group(0)
        return rel(doc, doc_path(slug)) + (m.group(2) or "")
    return re.sub(rf'(?<=[("]){re.escape(site_path)}(/[^\s)"#<>]*)?(#[\w-]+)?', repl, md)


# --- nav -----------------------------------------------------------------------

def breadcrumb(slug):
    """[(title, href), ...] from the page's rendered HTML breadcrumb."""
    soup = BeautifulSoup((RAW / "pages" / f"{slug}.html").read_text(encoding="utf-8"), "html.parser")
    for nav in soup.find_all("nav"):
        ol = nav.find("ol")
        if ol:
            return [(a.get_text(strip=True), a.get("href")) for a in ol.find_all("a")]
    return []


def build_nav(pages):
    """Rebuild the GitBook sidebar: section -> group -> page -> child pages."""
    slugs = {p["slug"] for p in pages}
    nav = []
    lists = {}  # key (section name / group slug / page slug) -> the nav list it owns
    for p in pages:
        slug, title, section = p["slug"], p["title"], p["section"]
        if slug == HOME_SLUG:
            nav.append({"Home": "index.md"})
            continue
        if section not in lists:
            lists[section] = []
            nav.append({section: lists[section]})

        parent = max((s for s in slugs if slug.startswith(s + "/")), key=len, default=None)
        if parent in lists:
            target = lists[parent]
        else:
            # GitBook groups ("2 - Programming and Algorithms") are path segments with no page
            parts = slug.split("/")
            group = "/".join(parts[:2]) if len(parts) > 2 and "/".join(parts[:2]) not in slugs else None
            if group and group not in lists:
                crumbs = breadcrumb(slug)
                gtitle = crumbs[1][0] if len(crumbs) > 1 else parts[1]
                lists[group] = []
                lists[section].append({gtitle: lists[group]})
            target = lists[group] if group else lists[section]

        if any(s.startswith(slug + "/") for s in slugs):
            lists[slug] = [{title: doc_path(slug)}]
            target.append({title: lists[slug]})
        else:
            target.append({title: doc_path(slug)})
    return nav


def yaml_nav(items, depth=1):
    out = []
    for item in items:
        (k, v), = item.items()
        k = k.replace('"', '\\"')
        if isinstance(v, list):
            out.append(f'{"  " * depth}- "{k}":')
            out += yaml_nav(v, depth + 1)
        else:
            out.append(f'{"  " * depth}- "{k}": {v}')
    return out


MKDOCS_YML = """\
site_name: {site_name}
site_description: Year 9 Computing Technology - Gosford High School
docs_dir: docs
use_directory_urls: false   # keeps relative paths in raw HTML (figures, video) valid

theme:
  name: material
  features:
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - navigation.footer
    - search.highlight
    - content.code.copy
    - content.code.annotate
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      toggle: {{icon: material/weather-night, name: Dark mode}}
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      toggle: {{icon: material/weather-sunny, name: Light mode}}

extra_css:
  - assets/extra.css

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.mark
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

nav:
{nav}
"""

EXTRA_CSS = """\
/* GitBook-style embeds */
.video-wrapper { position: relative; padding-bottom: 56.25%; height: 0; margin: 1em 0; }
.video-wrapper iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
video { max-width: 100%; border-radius: 4px; }
figure img { max-width: 100%; height: auto; }

/* GitBook stepper */
.gb-step { position: relative; border-left: 2px solid var(--md-primary-fg-color); padding: 0 0 0.5em 1.6em; margin-left: 0.8em; }
.gb-step-num { position: absolute; left: -0.8em; top: 0; width: 1.6em; height: 1.6em; border-radius: 50%;
  background: var(--md-primary-fg-color); color: var(--md-primary-bg-color); text-align: center;
  font-size: 0.8rem; line-height: 1.6em; font-weight: 700; }
"""


def main():
    manifest = json.loads((RAW / "manifest.json").read_text(encoding="utf-8"))
    pages, files, images, embeds = manifest["pages"], manifest["files"], manifest["images"], manifest["embeds"]
    slugs = {p["slug"] for p in pages}
    # space-root aliases (e.g. 'unit-2-data-science') -> the section's first page
    aliases = {"": HOME_SLUG}
    for p in pages:
        aliases.setdefault(p["slug"].split("/")[0], p["slug"])

    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir()
    for sub in ("files", "drive"):
        if (RAW / sub).exists():
            shutil.copytree(RAW / sub, DOCS / "assets" / sub,
                            ignore=shutil.ignore_patterns(*(f"*{e}" for e in VIDEO_EXT)))
    (DOCS / "assets" / "extra.css").write_text(EXTRA_CSS, encoding="utf-8")

    for p in pages:
        slug, doc = p["slug"], doc_path(p["slug"])
        md = (RAW / "pages" / f"{slug}.md").read_text(encoding="utf-8")
        md = re.sub(r"\A> For the complete documentation index.*\n+", "", md)
        md = convert_files(md, files, doc)
        md = convert_embeds(md, embeds, doc)
        md = localise_assets(md, files, images, doc)
        md = convert_code(md)
        md = convert_tabs(md)
        md = convert_steppers(md)
        md = convert_hints(md)
        md = convert_details(md)
        md = convert_marks(md)
        md = convert_links(md, slugs, aliases, manifest["base"], doc)
        for tag in set(re.findall(r"\{%-?\s*(\w+)", md)):
            warnings.append(f"{doc}: unconverted tag {{% {tag} %}}")
        out = DOCS / doc
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md.strip() + "\n", encoding="utf-8")

    nav = "\n".join(yaml_nav(build_nav(pages)))
    (ROOT / "mkdocs.yml").write_text(MKDOCS_YML.format(site_name=SITE_NAME, nav=nav), encoding="utf-8")

    print(f"Converted {len(pages)} pages into {DOCS}")
    for w in warnings:
        print("WARN", w)


if __name__ == "__main__":
    main()
