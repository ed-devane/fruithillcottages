# Fruit Hill Cottages — static site

A plain HTML/CSS copy of the Squarespace site, ready for GitHub Pages (free hosting).
Same page addresses as before (`/coach-house`, `/kirbys-1`, `/about-us`, …), so old links and Google results keep working.

## Do this first (while Squarespace is still live)

```bash
bash get-images.sh
```

Downloads all 30 photos from Squarespace into `images/`. It prints `Downloaded 30 images, 0 failed.` when done. Don't cancel Squarespace until this has worked.

## Put it on GitHub Pages

1. Create a new repository on GitHub (e.g. `fruithillcottages`), public.
2. Upload everything in this folder, including `images/`, `CNAME` and `.nojekyll`:
   ```bash
   git init && git add -A && git commit -m "Fruit Hill Cottages site"
   git branch -M main
   git remote add origin https://github.com/ed-devane/fruithillcottages.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages → Source: Deploy from a branch → `main` / root → Save.**
4. After a minute, check it at `https://ed-devane.github.io/fruithillcottages/`.

## Point the domain at it

Wherever the domain's DNS is managed (Squarespace Domains if it was bought through Squarespace):

| Type  | Host | Value |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| CNAME | www  | ed-devane.github.io |

Delete the old Squarespace A/CNAME records for `@` and `www` first. Then in GitHub **Settings → Pages**, enter `www.fruithillcottages.com` as the custom domain and tick **Enforce HTTPS** once it's offered (can take up to a day).

The domain itself can stay registered with Squarespace (you only cancel the *website* plan), or be transferred to another registrar.

## Editing text later

All the wording lives in `build.py`. Edit it, then run `python3 build.py` to regenerate the pages, and push.

## Files

- `index.html`, `*/index.html` — the pages
- `assets/` — stylesheet, menu/gallery script, favicon
- `images/` — photos (filled by `get-images.sh`)
- `images.tsv` — photo list and their Squarespace source URLs
- `CNAME` — tells GitHub Pages the domain name
- `404.html` — "page not found" page
