# Shine Online Shop Specific Product Pages

This folder contains standalone GitHub Pages product display pages for Canva Website links.

## Pages

Product pages are generated from `tools/product_data.json` into `products/*.html`.

## Link List

Use `docs/page-links.md` or `docs/page-links.docx` to copy the final page links into Canva.

GitHub Pages root URL:

```text
https://po-kwong.github.io/shine-online-shop-specific-products-pages/
```

## Image Access

The pages display local optimized WebP images generated from the Google Drive source files. The "open original image" links still point to Google Drive.

## Updating The Site

For manual updates, say `refresh` or `更新` in this project and follow `AGENTS.md`.

For direct local refresh after `tools/product_data.json` has been updated, run:

```powershell
& 'C:\Users\Jason\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'tools\refresh_site.py'
```

See `docs/update-workflow.md` for the full future update workflow.

There is no scheduled GitHub Actions Drive sync. This avoids Google Drive credential setup; updates are done when Jason asks Codex to `refresh` / `更新`.
