# Year 9 Computing Technology

Course site for Year 9 Computing Technology (Gosford High School), migrated from GitBook
and built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Edit and preview

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/mkdocs serve        # http://127.0.0.1:8000
```

Course content lives in `docs/`; the sidebar is the `nav:` section of `mkdocs.yml`.
Pushing to `main` publishes the site to GitHub Pages (`.github/workflows/deploy.yml`).

## GitBook migration

| Path | What it is |
| --- | --- |
| `raw/` | Untouched GitBook export: page `.md` + `.html`, attachments, Drive/Slides downloads, `manifest.json` |
| `tools/scrape_gitbook.py` | Re-scrapes the GitBook into `raw/` (skips anything already downloaded) |
| `tools/convert_to_mkdocs.py` | Rebuilds `docs/` and `mkdocs.yml` from `raw/` - **overwrites `docs/`** |

Tutorial videos (3.9 GB) are kept in `raw/drive/` locally but are not committed; the site
plays them from Google Drive.

Once you start editing `docs/` directly, stop running the converter.
