# Miller Pool and Spa site (mockup)

Static site. No build step on the host. `public/` is what gets served.

## Cloudflare Pages
- Framework preset: None
- Build command: (empty)
- Build output directory: `public`
- Production branch: `main`

## Editing
Copy, header, footer and page structure live in `build/build.py`. Don't hand-edit `public/`.

```
python3 build/build.py public /tmp/preview.html build/miller-logo-source.png
git add -A && git commit -m "Update copy" && git push
```

Cloudflare redeploys on every push to `main`.

## Before launch
- `public/_headers` sets `noindex` so the mockup stays out of Google. Remove it when this goes live on millerpoolandspausa.com.
- Real photos for the grey photo slots, call-tracking number, CSLB license, original logo, form endpoint, Parker's OK on the About copy.
