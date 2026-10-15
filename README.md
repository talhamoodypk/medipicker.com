# MediPicker

Static websites for **medipicker.com** and its product review subdomains.

| Folder | Website | What it is |
|---|---|---|
| `medipicker.com/` | https://medipicker.com | Main site: product directory (119 products), `/blog/` with a review page per product |
| `trimology/` | https://trimology.medipicker.com | In-depth Trimology review |
| `gelatinesculpt.medipicker.com/` | https://gelatinesculpt.medipicker.com | In-depth Gelatine Sculpt review (live: Pages project `gelatinesculpt`, deployed with wrangler) |
| `regenvive/` | https://regenvive.medipicker.com | In-depth RegenVive review |
| `first-version/` | — | Original NuraVive design (not published) |
| `_build/` | — | Product list and scripts that generate `medipicker.com/` (not published) |

## Publish on Cloudflare Pages

Each website is its own Cloudflare Pages project pointing at this repo.

**Main site (medipicker.com)**
1. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git**.
2. Pick the repo `rommeoromi327/Medipicker`, branch **Medipicker**.
3. Build settings: Framework preset **None**, Build command **(leave empty)**, Build output directory **`medipicker.com`**.
4. Save and Deploy, then **Custom domains → Set up a custom domain → `medipicker.com`** (and `www.medipicker.com` if you like).

**Review subdomains** — repeat the same steps for each, changing only:
| Project | Build output directory | Custom domain |
|---|---|---|
| trimology | `trimology` | `trimology.medipicker.com` |
| gelatinesculpt | `gelatinesculpt.medipicker.com` | `gelatinesculpt.medipicker.com` (done) |
| regenvive | `regenvive` | `regenvive.medipicker.com` |

Every push to the `Medipicker` branch redeploys automatically.

## After publishing (Bing)
1. Add each site in Bing Webmaster Tools and paste its code into the `msvalidate.01` meta tag of that site's `index.html`
   (for medipicker.com edit `_build/home_template.html`, then rebuild).
2. Submit each `sitemap.xml` (e.g. https://medipicker.com/sitemap.xml).
3. Ping IndexNow for the review sites (keys are in each folder; see their `keyword-research.md`).

## Updating the product list
1. Edit `_build/products.tsv` — one product per line: `Name<TAB>link`. The first link for a name wins.
2. Change categories in `_build/build_home.py` (`CATEGORY`) and page copy in `_build/content.py`.
3. Rebuild: `py -X utf8 _build/build_site.py`
4. Commit and push.

Products currently left off the site because their links were broken (15 Oct 2026): Bio Fungus Nuker
(domain for sale), VivoTonic (link returns 403), Restolin (lands on a 404 page) — see `DISABLED` in `_build/content.py`.
