# Miller Pool and Spa site (mockup)

Static site. No build step on the host. `public/` is the site.

The root `_redirects` and `_headers` files make it work even when the Cloudflare build output directory is left at `/` (clean URLs are rewritten to `public/`). If the output directory is set to `public`, they are simply not deployed.

## Cloudflare Pages
- Framework preset: None
- Build command: (empty)
- Build output directory: `public`
- Production branch: `main`

## Pages
Home, pool repair hub, 6 repair service pages, 6 city pages, weekly service, about, contact, reviews, service area, privacy, and a blog (`/blog/` plus one folder per post). Posts live in the `posts` list in `build/build.py`; add a dict there and rebuild.

## Editing
Copy, header, footer and page structure live in `build/build.py`. Don't hand-edit `public/`.

```
python3 build/build.py public /tmp/preview.html build/miller-logo-source.png
git add -A && git commit -m "Update copy" && git push
```

Cloudflare redeploys on every push to `main`.

## Before launch
- `public/_headers` sets `noindex` so the mockup stays out of Google. Remove it when this goes live on millerpoolandspausa.com.
- Real photos for the grey photo slots, call-tracking number, CSLB license, original logo, form endpoint, Parker's OK on the About page and on the price ranges in the heater-cost blog post.
