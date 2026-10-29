# Year 9 Computing Technology

Course site for Year 9 Computing Technology (Gosford High School), migrated from GitBook
in October 2026 and built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

- **Live site:** https://vormamim.github.io/y9-computing-tech/
- **Repo:** https://github.com/Vormamim/y9-computing-tech
- **Local folder:** `OneDrive - NSW Department of Education/4-Python_Projects/Y9CT_2026`

---

## Quick reference: the everyday loop

```bash
# 1. Open a terminal in the project folder (VS Code: Terminal > New Terminal)
# 2. Preview the site while you edit (auto-refreshes on save)
.venv/Scripts/mkdocs serve
#    then open http://127.0.0.1:8000   (Ctrl+C to stop)

# 3. Publish
git add -A
git commit -m "Describe what you changed"
git push
```

The site updates by itself about 1–2 minutes after a push. You can watch progress on the
repo's **Actions** tab. A green tick means it's live, and a red cross means the build failed
(see [Troubleshooting](#troubleshooting)).

---

## First-time setup on a new computer

You only need this if `.venv/` is missing, for example on a new PC or after a fresh clone.

```bash
git clone https://github.com/Vormamim/y9-computing-tech.git
cd y9-computing-tech
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

On a Mac or Linux machine, use `.venv/bin/` instead of `.venv/Scripts/`.

---

## How the site is organised

| Path | What it is |
| --- | --- |
| `docs/` | **The course content. This is what you edit.** One `.md` file per page. |
| `docs/assets/files/` | Images and attachments (PDFs etc.) from GitBook |
| `docs/assets/drive/` | Downloaded Google Slides/Docs exports and PDFs |
| `docs/assets/extra.css` | Small style tweaks (video sizing, step lists) |
| `mkdocs.yml` | Site settings **and the sidebar menu** (the `nav:` section) |
| `raw/` | The original GitBook export. Archive only, don't edit. |
| `tools/` | The scripts that did the migration. You won't normally need them. |
| `.github/workflows/deploy.yml` | Builds and publishes the site on every push to `main` |

The page filename matches its old GitBook address. For example,
`docs/unit-3-games-and-simulations/2-modelling-systems/ipo-charts.md` was
`…/9-computing-tech/unit-3-games-and-simulations/2-modelling-systems/ipo-charts`.

---

## Common tasks

### Edit a page
Open the `.md` file in `docs/`, change it, save, and check it in `mkdocs serve`.

### Add a new page
1. Create the file, e.g. `docs/unit-3-games-and-simulations/3-unity-tutorials/12-polish.md`,
   starting with a `# Title` line.
2. **Add it to the sidebar** in `mkdocs.yml` under `nav:`, in the place you want it:
   ```yaml
         - "12 - Polish": unit-3-games-and-simulations/3-unity-tutorials/12-polish.md
   ```
   Indentation matters: copy a neighbouring line and change it. A page not listed in `nav:`
   still builds, but it won't appear in the sidebar.

### Rename, move or delete a page
Change the file **and** its line in `mkdocs.yml`. Then run `.venv/Scripts/mkdocs build --strict`
to find any other pages that still link to the old name (see Troubleshooting).

### Link to another page
Use a relative path to the `.md` file. MkDocs turns it into the right web link:
```markdown
See [IPO Charts](../2-modelling-systems/ipo-charts.md)
```

### Add an image or file (PDF, worksheet)
1. Put the file in `docs/assets/files/`. Avoid spaces in new filenames, or use `-` instead.
2. Link it with a path relative to the page:
   ```markdown
   ![Flowchart example](../../assets/files/flowchart-example.png)

   [:material-file-download: Download the worksheet](../../assets/files/worksheet.pdf){ .md-button }
   ```
   Count the `../` by how many folders deep the page is. The easiest way is to copy an
   existing link from a nearby page.

### Add a video
**Don't put video files in the repo.** GitHub rejects files over 100 MB, and the site has a
1 GB limit. Upload the video to Google Drive (sharing: *Anyone with the link*) or to YouTube
(unlisted), then embed it.

Google Drive: take the ID from the share link `drive.google.com/file/d/<ID>/view`.
```html
<div class="video-wrapper"><iframe src="https://drive.google.com/file/d/<ID>/preview" allow="autoplay" allowfullscreen></iframe></div>
```

YouTube: take the ID from `youtube.com/watch?v=<ID>`.
```html
<div class="video-wrapper"><iframe src="https://www.youtube-nocookie.com/embed/<ID>" allowfullscreen></iframe></div>
```

### Link to Google Slides / Docs
```markdown
[:material-open-in-new: Open the slides](https://docs.google.com/presentation/d/.../edit){ .md-button }
```

---

## Formatting cheat sheet (GitBook → MkDocs equivalents)

| GitBook block | MkDocs Markdown |
| --- | --- |
| Hint (info / success / warning / danger) | `!!! info "Learning Intention"` and then the content **indented 4 spaces** |
| Expandable block | `??? note "Click to reveal"` and then the content indented 4 spaces |
| Tabs | `=== "Tab name"` and then the content indented 4 spaces (repeat for each tab) |
| Code block with a title | ```` ```python title="main.py" ```` |
| Highlighted text | `==highlighted==` |
| Button-style link | `[Text](link){ .md-button }` |
| Icon | `:material-file-download:`, `:material-google-drive:`, `:material-open-in-new:` |

Example hint:
```markdown
!!! success "Success Criteria"

    I can develop IPO charts to plan a process in a game.
```

The **4-space indent** is the thing most likely to trip you up. If a box shows up empty or the
text appears below it, the indent is wrong.

Full reference: https://squidfunk.github.io/mkdocs-material/reference/

---

## Troubleshooting

**Check for broken links before pushing**
```bash
.venv/Scripts/mkdocs build --strict
```
Any `WARNING` line names the page and the broken link. The Actions build doesn't run in strict
mode, so a broken link won't stop the site publishing. It's still worth running this check.

**The Actions tab shows a red cross.** Click into the failed run and read the last red lines.
The cause is usually a typo or a bad indent in `mkdocs.yml`. Fix it, commit, and push again.

**The site doesn't update after a push.** Wait 2 minutes and hard-refresh (Ctrl+F5). If
that doesn't help, check that **Settings → Pages** is still set to *Deploy from a branch:
`gh-pages` / root*.

**`git push` asks you to log in.** Sign in through the browser window that opens, using the
**Vormamim** GitHub account.

**`mkdocs` command not found.** The virtual environment is missing. Do the
[First-time setup](#first-time-setup-on-a-new-computer) steps.

**Git errors about locked files or `index.lock`.** This folder is synced by OneDrive, which
sometimes holds git's files open. Pause OneDrive syncing (tray icon → Pause), retry, and
then resume.

**Python downloads fail with certificate errors on the school network.** The department
network inspects HTTPS. The tools use the `truststore` package to trust the Windows
certificate store, so keep `truststore` installed and don't turn off certificate checking.

---

## About the GitBook migration (archive)

The original course is at https://gosford-high-school.gitbook.io/9-computing-tech. In October
2026 all 104 pages were scraped into `raw/` and converted into `docs/`.

- `raw/pages/`: each page as GitBook's Markdown and as the rendered HTML
- `raw/files/`, `raw/drive/`: attachments, images and Google Drive/Slides downloads
- `raw/manifest.json`: every page, file and embed, with its original URL
- **Tutorial videos (43 files, 3.9 GB)** are in `raw/drive/` **on this PC only**. They're
  excluded from git by `.gitignore`, and the site plays them from Google Drive. **Don't delete
  them from Drive**, or the embeds will break. Back up the local copies if you change PCs.

> ⚠️ **Do not re-run `tools/convert_to_mkdocs.py`.** It deletes and regenerates `docs/` and
> `mkdocs.yml` from the GitBook export, so it would wipe every edit made since the migration.
> `tools/scrape_gitbook.py` only writes to `raw/` and is safe, but it isn't needed any more.
