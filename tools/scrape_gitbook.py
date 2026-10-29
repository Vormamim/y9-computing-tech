"""Scrape the Y9 Computing Technology GitBook into raw/ (pages, attachments, images, embeds).

Usage:
    python tools/scrape_gitbook.py [--force] [--skip-media]

Everything lands in raw/ untouched; tools/convert_to_mkdocs.py turns it into docs/.
"""

import argparse
import html
import json
import mimetypes
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs

import truststore

truststore.inject_into_ssl()  # use the Windows cert store (department TLS inspection)

import requests

BASE = "https://gosford-high-school.gitbook.io/9-computing-tech"
EXPECTED_PAGES = 104
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
PAGES = RAW / "pages"
FILES = RAW / "files"
DRIVE = RAW / "drive"
MANIFEST = RAW / "manifest.json"

SESSION = requests.Session()
SESSION.headers["User-Agent"] = "Mozilla/5.0 (Y9CT GitBook export)"
SM_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def get(url, **kwargs):
    """GET with retries and a polite delay."""
    for attempt in range(4):
        try:
            r = SESSION.get(url, timeout=60, **kwargs)
            if r.status_code < 500 and r.status_code != 429:
                time.sleep(0.5)
                return r
        except requests.RequestException as e:
            print(f"  ! {e.__class__.__name__} on {url}")
        time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to fetch {url}")


def page_slug(url):
    """Page URL -> path relative to the site root ('' for the home page)."""
    return url[len(BASE):].strip("/")


def sitemap_urls():
    index = ET.fromstring(get(f"{BASE}/sitemap.xml").content)
    urls = []
    for sm in index.findall("sm:sitemap/sm:loc", SM_NS):
        child = ET.fromstring(get(sm.text).content)
        urls += [loc.text for loc in child.findall("sm:url/sm:loc", SM_NS)]
    return urls


def discover_pages(llms_text):
    """Ordered pages from llms.txt: [{section, title, url}] in sidebar order.

    The sitemap lists each space's root URL (an alias that has no .md), so
    llms.txt is the canonical list; the sitemap is only used as a count check.
    """
    pages, section = [], None
    for line in llms_text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        elif m := re.match(r"- \[(.+?)\]\((https://\S+?)\.md\)", line):
            pages.append({"section": section, "title": m.group(1), "url": m.group(2)})
    return pages


def fetch_pages(urls, force):
    for i, url in enumerate(urls, 1):
        slug = page_slug(url)
        for ext, src in ((".md", f"{url}.md"), (".html", url)):
            dest = PAGES / f"{slug}{ext}"
            if dest.exists() and not force:
                continue
            r = get(src)
            if r.status_code != 200:
                print(f"  ! {r.status_code} {src}")
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(r.text, encoding="utf-8")
        print(f"[{i}/{len(urls)}] {slug}")


# --- assets ---------------------------------------------------------------

FILE_TAG = re.compile(r'\{%\s*file\s+src="([^"]+)"')
EMBED_TAG = re.compile(r'\{%\s*embed\s+url="([^"]+)"')
MD_IMG = re.compile(r'!\[[^\]]*\]\(<?([^)\s>]+)>?')
HTML_IMG = re.compile(r'<img[^>]*\ssrc="([^"]+)"')
# RSC payload: ..."href":"<download url>",...,"kind":"file","file":"<id>"
RSC_FILE = re.compile(r'"href":"(https://[^"]+)"(?:(?!"href").){0,400}?"kind":"file","file":"(\w+)"')
GITBOOK_FILE_URL = re.compile(r'https://[\w.-]*files\.gitbook\.io/~/files/v0/b/[^"\s\\]+')


def rsc_text(page_html):
    """Unescape the Next.js flight payload so its JSON is greppable."""
    return page_html.replace('\\"', '"').replace("\\u0026", "&").replace("&amp;", "&")


def filename_from_url(url):
    path = unquote(urlparse(url).path)
    return path.rsplit("/", 1)[-1] or "file"


def safe(name):
    return re.sub(r'[<>:"/\\|?*]+', "_", name).strip() or "file"


def upload_id(url):
    """GitBook storage URL -> its upload id (the folder after 'uploads/')."""
    m = re.search(r"uploads%2F([\w-]+)%2F", url)
    return m.group(1) if m else None


def collect_refs(urls):
    """Scan raw pages for every file, image and embed reference.

    files:  key = the string as written in the .md ('/files/<id>' or an absolute
            files.gitbook.io URL); value has the download url and pages using it.
    images: external (non-GitBook) image URLs.
    """
    refs = {"files": {}, "images": {}, "embeds": {}}
    for url in urls:
        slug = page_slug(url)
        md = (PAGES / f"{slug}.md").read_text(encoding="utf-8")
        page_html = rsc_text((PAGES / f"{slug}.html").read_text(encoding="utf-8"))
        id_to_url = {fid: u for u, fid in RSC_FILE.findall(page_html)}

        def add_file(key, download_url):
            entry = refs["files"].setdefault(key, {"pages": []})
            if download_url:
                entry["url"] = download_url
            if slug not in entry["pages"]:
                entry["pages"].append(slug)

        for src in FILE_TAG.findall(md):
            fid = src.rstrip("/").rsplit("/", 1)[-1]
            add_file(src, id_to_url.get(fid))

        for raw_url in GITBOOK_FILE_URL.findall(md):
            add_file(raw_url, html.unescape(raw_url))

        for src in MD_IMG.findall(md) + HTML_IMG.findall(md):
            src = html.unescape(src)
            if src.startswith("http") and "files.gitbook.io" not in src:
                entry = refs["images"].setdefault(src, {"pages": []})
                if slug not in entry["pages"]:
                    entry["pages"].append(slug)

        for u in EMBED_TAG.findall(md):
            u = html.unescape(u).strip("<>")
            entry = refs["embeds"].setdefault(u, {"kind": classify_embed(u), "pages": []})
            entry["pages"].append(slug)
    return refs


def classify_embed(url):
    host = urlparse(url).netloc
    if "drive.google.com" in host:
        return "drive"
    if "docs.google.com" in host:
        kind = urlparse(url).path.split("/")[1]  # presentation / document / spreadsheets / forms
        return f"google-{kind}"
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    return "other"


def download(url, dest_dir, name=None):
    """Stream a URL to dest_dir; returns the saved Path."""
    r = SESSION.get(url, stream=True, timeout=120)
    r.raise_for_status()
    if not name:
        cd = r.headers.get("Content-Disposition", "")
        m = re.search(r"filename\*=UTF-8''([^;]+)", cd) or re.search(r'filename="?([^";]+)"?', cd)
        name = unquote(m.group(1)) if m else filename_from_url(url)
    if "." not in name[-6:]:
        name += mimetypes.guess_extension(r.headers.get("Content-Type", "").split(";")[0]) or ""
    dest = dest_dir / safe(name)
    dest_dir.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(1 << 20):
            f.write(chunk)
    return dest


def download_files(refs, force):
    """Download GitBook uploads and external images into raw/files/<upload id>__<name>."""
    failed = []
    jobs = [(k, e, e.get("url")) for k, e in refs["files"].items()]
    jobs += [(k, e, k) for k, e in refs["images"].items()]
    for key, entry, url in jobs:
        if not url:
            failed.append({"type": "file", "ref": key, "pages": entry["pages"], "error": "no URL in page HTML"})
            continue
        uid = upload_id(url) or re.sub(r"\W", "", url)[-20:]
        existing = list(FILES.glob(f"{uid}__*"))
        if existing and not force:
            entry["local"] = existing[0].relative_to(RAW).as_posix()
            continue
        try:
            name = filename_from_url(url) if upload_id(url) else None
            dest = download(url, FILES, f"{uid}__{safe(name)}" if name else None)
            if not name:  # external image: prefix the id after Content-Disposition naming
                dest = dest.rename(FILES / f"{uid}__{dest.name}")
            entry["local"] = dest.relative_to(RAW).as_posix()
            print(f"  file {entry['local']}")
        except Exception as e:
            failed.append({"type": "file", "ref": key, "url": url, "error": str(e)})
            print(f"  ! file failed {url[:100]}: {e}")
    return failed


def drive_id(url):
    m = re.search(r"/d/([\w-]{20,})", url) or re.search(r"[?&]id=([\w-]{20,})", url)
    return m.group(1) if m else None


def download_embeds(refs, force):
    import gdown

    failed = []
    for url, entry in refs["embeds"].items():
        kind, gid = entry["kind"], drive_id(url)
        if not gid or kind not in ("drive", "google-presentation", "google-document", "google-spreadsheets"):
            continue
        existing = list(DRIVE.glob(f"{gid}__*"))
        if existing and not force:
            entry["local"] = [p.relative_to(RAW).as_posix() for p in existing]
            continue
        DRIVE.mkdir(parents=True, exist_ok=True)
        try:
            if kind == "drive":
                out = gdown.download(id=gid, output=str(DRIVE) + "/", quiet=True)
                if not out:
                    raise RuntimeError("gdown returned nothing (private or quota exceeded?)")
                p = Path(out)
                saved = [p.rename(DRIVE / f"{gid}__{safe(p.name)}")]
            else:
                doc = url.split("/d/")[0]  # https://docs.google.com/presentation
                fmts = {"google-presentation": ["pptx", "pdf"],
                        "google-document": ["docx", "pdf"],
                        "google-spreadsheets": ["xlsx"]}[kind]
                saved = []
                for fmt in fmts:
                    r = SESSION.get(f"{doc}/d/{gid}/export?format={fmt}", timeout=120)
                    if r.status_code != 200 or "text/html" in r.headers.get("Content-Type", ""):
                        raise RuntimeError(f"export {fmt} -> {r.status_code}")
                    p = DRIVE / f"{gid}__export.{fmt}"
                    p.write_bytes(r.content)
                    saved.append(p)
            entry["local"] = [p.relative_to(RAW).as_posix() for p in saved]
            print(f"  embed {entry['local']}")
        except Exception as e:
            failed.append({"type": "embed", "kind": kind, "url": url, "pages": entry["pages"], "error": str(e)})
            print(f"  ! embed failed {url}: {e}")
    return failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download everything")
    ap.add_argument("--skip-media", action="store_true", help="pages only, no attachments/embeds")
    args = ap.parse_args()

    RAW.mkdir(exist_ok=True)
    llms = get(f"{BASE}/llms.txt").text
    (RAW / "llms.txt").write_text(llms, encoding="utf-8")
    pages = discover_pages(llms)
    urls = [p["url"] for p in pages]
    n_sitemap = len(sitemap_urls())
    print(f"Discovered {len(urls)} pages (sitemap lists {n_sitemap})")
    if not len(urls) == n_sitemap == EXPECTED_PAGES:
        print(f"WARNING: expected {EXPECTED_PAGES} pages", file=sys.stderr)

    fetch_pages(urls, args.force)
    refs = collect_refs(urls)
    failed = []
    if not args.skip_media:
        failed += download_files(refs, args.force)
        failed += download_embeds(refs, args.force)

    manifest = {
        "base": BASE,
        "pages": [{**p, "slug": page_slug(p["url"])} for p in pages],
        **refs,
        "failed_downloads": failed,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nPages: {len(urls)}  files: {len(refs['files'])}  images: {len(refs['images'])}  "
          f"embeds: {len(refs['embeds'])}  failed: {len(failed)}")


if __name__ == "__main__":
    main()
