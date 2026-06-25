# IEEE-CIS-NNTC-TF-SL Website

Static GitHub Pages version of the IEEE CIS Neural Networks Technical Committee Task Force on Secure Learning website.

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

## Structure

- `index.html` - home page shell
- `pages/` - secondary page shells
- `data/site-data.js` - editable website content
- `assets/css/styles.css` - shared styling
- `assets/js/app.js` - shared renderer
- `assets/images/` - copied visual assets
- `source/` - source snapshots and extracted reference text from the original Google Sites pages

## Content updates

Most text, links, people, news, and activity entries live in `data/site-data.js`. Update that file first; the page templates reuse it automatically.
