# IEEE-CIS-NNTC-TF-SL Website

GitHub Pages/Jekyll version of the IEEE CIS Neural Networks Technical Committee Task Force on Secure Learning website. The original Google Sites content has been migrated into local Markdown files so the Google Sites version can be retired.

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

If this is the first local run, install the GitHub Pages/Jekyll dependencies first:

```bash
bundle install
```

## Structure

- `index.md` - editable Markdown source for the home page
- `pages/*.md` - editable Markdown source for secondary pages
- `_layouts/default.html` - shared page layout
- `_config.yml` - GitHub Pages/Jekyll configuration
- `assets/css/styles.css` - shared styling
- `assets/images/` - copied visual assets
- `source/` - source snapshots and extracted reference text from the original Google Sites pages

## Content updates

Edit `index.md` or the Markdown files under `pages/`. GitHub Pages will build the HTML automatically from these Markdown files.
