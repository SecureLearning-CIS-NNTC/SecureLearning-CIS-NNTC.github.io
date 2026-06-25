# IEEE-CIS-NNTC-TF-SL Website

Static GitHub Pages version of the IEEE CIS Neural Networks Technical Committee Task Force on Secure Learning website. The original Google Sites content has been migrated into local Markdown files so the Google Sites version can be retired.

## Local preview

```bash
./scripts/serve.sh
```

Then open:

```text
http://127.0.0.1:8000/
```

Use another port if needed:

```bash
./scripts/serve.sh 8080
```

The serve script runs `scripts/build.py` first, so Markdown edits are regenerated before the local server starts.

## Structure

- `content/pages/` - editable Markdown source files for all pages
- `index.html` - generated home page
- `pages/` - generated secondary pages
- `assets/css/styles.css` - shared styling
- `assets/images/` - copied visual assets
- `scripts/build.py` - Markdown-to-HTML build script
- `source/` - source snapshots and extracted reference text from the original Google Sites pages

## Content updates

Edit the Markdown files under `content/pages/`, then run:

```bash
python3 scripts/build.py
```

The generated HTML files are committed for GitHub Pages publishing.
