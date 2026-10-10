# techsutralabs.com

Website of **TechSutraLabs Ventures (OPC) Private Limited** (TechSutra Labs Ventures).

Plain static HTML/CSS/JS: no build step, no dependencies.

| Path | What it is |
|---|---|
| `*.html` | The pages that are published |
| `assets/` | Stylesheet, script, logo, icons, social preview image |
| `robots.txt`, `sitemap.xml` | Search-engine files |
| `.htaccess` | Only used if the site is ever moved to Apache/cPanel hosting |
| `tools/generate.py` | Generator the pages were built from: `python3 tools/generate.py .` rewrites every page (overwrites hand edits to the HTML) |
| `tools/og-image.html` | Source of `assets/og-image.png` |

## Publishing

- Every push to `main` deploys to GitHub Pages via `.github/workflows/deploy.yml`
  (everything except `tools/`, `.github/` and this README is published).
- On the owner's Mac, a launchd job (`com.techsutralabs.autosync`) watches this folder and
  automatically commits and pushes any change, which then deploys. Log:
  `~/Library/Logs/techsutralabs-autosync.log`.

Anything saved into this folder becomes public on the live website.
