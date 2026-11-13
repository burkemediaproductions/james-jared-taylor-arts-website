# James Jared Taylor — ServiceUp 2026 integration

## Status and limitations

**Ready for tenant import and deployment, not yet connected to the production tenant.** This package was built from the user-supplied `Website(5).zip` and `Core App.zip`. A mock of the authenticated-by-tenant public data endpoints was used in the integration test. No production Render/Supabase/Netlify credentials were supplied or used, and no live tenant database has been changed.

The existing root site remains the visual reference. The separate `/serviceup/` tree is generated from published ServiceUp entries at **Netlify build time**. No public-facing content is fetched in the browser.

**Important media limitation:** 584 WordPress media records are migrated as editable Media Reference entries, but that is not the same as uploading binary files into ServiceUp Pixels/Supabase Storage. The 315 currently displayed artwork images are packaged locally and remain visible. To make all old images available in the Pixels picker, import/upload the binaries into the appropriate tenant's Supabase Storage and register Pixels; update Artwork.image when replacing images. Never place service-role keys in the website repository or Netlify browser bundles.

## Deployment order

1. Deploy the supplied API patch (`core-patch/api/routes/publicSite.js`) to the matching **shared Render API**. It adds a read-only, tenant-isolated `GET /api/public/menu/:slug` endpoint and triggers rebuild hooks on Menu, Profile and tenant-import saves. Merge these changes rather than replacing unrelated future core updates. Existing `/api/content/:slug` and `scheduleSiteRebuild` already support published entries and build hooks.
2. Confirm the `james-jared-taylor` tenant exists in ServiceUp. Register the tenant preview/admin domain as appropriate for login. This package does not create a tenant or assign administrator accounts.
3. In **that tenant's** ServiceUp dashboard open **Settings → Import & Export**. Upload `serviceup/james-jared-taylor-import.json` (not the ZIP). Select Content Types, Taxonomies, Menus, and Entries; run a **dry run** first; inspect conflicts; then confirm a real import. Importing into a different tenant slug must fail.
4. In Netlify (website GitHub repo), set `SERVICEUP_API_BASE=https://YOUR-RENDER-API-HOST` and `SERVICEUP_TENANT=james-jared-taylor` as **build environment variables**. The value is the origin, without `/api`. Build: `npm run build:preview`; publish: `dist`; Node: `22`. No API secret is needed; all reads use public, tenant-scoped, published data.
5. Trigger the first Netlify deploy **only after the core patch and content import succeed**. Validate root `.../` is unchanged and the CMS copy appears under `.../serviceup/`.
6. In Netlify, create a build hook for this website's GitHub branch. On shared Render API set or merge `SERVICEUP_SITE_BUILD_HOOKS={"james-jared-taylor":"https://api.netlify.com/build_hooks/YOUR_HOOK"}`. Keep this value server-side on Render only. API content create/update/delete automatically calls the tenant hook, with a 15-second debounce as in the supplied core.
7. Save one safe edit (e.g. homepage tagline or a Page panel) in ServiceUp. Confirm Render schedules the hook and Netlify regenerates `/serviceup/`, while the root static copy stays the same.

**Local review:** `npm run dev` serves the original static version on `http://localhost:4173/`. With the API and content imported, define `SERVICEUP_API_BASE` and run `npm run dev:serviceup` to serve both `/` and `/serviceup/` on the same port. Windows PowerShell: `$env:SERVICEUP_API_BASE='https://YOUR-RENDER-API-HOST'; npm run dev:serviceup`.

## Tenant / privacy / indexing

- Tenant slug: `james-jared-taylor`
- Live domain: `https://jamesjaredtaylorarts.com`
- Preview: `https://YOUR-NETLIFY-SITE.netlify.app/serviceup/`
- `/serviceup/` is deliberately `noindex,nofollow,noarchive`, regardless of `SITE_ENV`. Root preview also defaults to noindex; remove this only as part of the final launch process.
- Tenant specified via `x-serviceup-tenant` on **build-time server-to-server requests**. Shared API middleware resolves tenant and enforces RLS.
- Missing mandatory API data or a failed API request stops the Netlify build (the prior successful Netlify deployment remains live).
- Do not commit `.env` or a copied core API secret to GitHub. This package omits the supplied Core App's `.env` entirely.

## Original frontend interaction inventory

- Header with desktop links, Current Work and Archive dropdowns, SVG chevrons, keyboard support and focus states.
- Animated full-screen mobile menu, submenu links, Escape-to-close and `inert` behavior.
- Homepage two parallax/artwork background images, overlay links, and scroll hint; supporting About, Featured Work, artist quote and journal CTA sections.
- Responsive two-up Current Work/Archive collection category cards with hover transforms.
- Painting/sculpture grids for Current Work and Archive with artwork cards, images, titles and series/year.
- Per-artwork detail page with metadata, image enlarge buttons, thumbnail strip, previous/next-like artwork navigation and overlay lightbox with Escape/arrow/button operation.
- About biography, portrait, artist statement, education and CTA.
- Journal listing and article detail routes, date, source link and related navigation.
- Links listing and email/social contact CTA, semantic footer.
- Scroll reveal animations, reduced-motion accommodations, original CSS and JS kept intact.
- Original frontend has **no contact form, background video or accordion** to wire into ServiceUp. No Netlify Forms were removed.

## Content types and entries

| ServiceUp type | Initial entries | Notes |
|---|---:|---|
| `artwork` | 315 | James Jared Taylor artworks |
| `journal-post` | 9 | James Jared Taylor journal posts |
| `page` | 10 | James Jared Taylor pages |
| `artist-settings` | 1 | James Jared Taylor artist settings |
| `collection` | 4 | James Jared Taylor collections |
| `artist-link` | 4 | James Jared Taylor artist links |
| `education` | 3 | James Jared Taylor education |
| `exhibition` | 2 | James Jared Taylor exhibitions |
| `press` | 3 | James Jared Taylor press |
| `media-reference` | 584 | Legacy WordPress media inventory; actual managed Pixels must be uploaded separately. |

`Page.panels` uses the **built-in Panels** field, with fixed Page Templates and stable panel IDs. No layout HTML is saved in `entries.data`. Custom Panel Types use structured fields and select frontend components. Artworks, journals, education, links, press, exhibitions and media are ordinary entries, not duplicated in Page panels.

## Panels and frontend mapping

Every row below is **fixed**, preserving the original order and preventing accidental removal/rearrangement in the ServiceUp editor. `jjt-gallery-grid`/`jjt-featured-artwork` reference ordinary Artwork/Collection entries by slug, not embedded copies.

| Frontend route | Frontend section | Panel type | Data fields | Reusable reference |
|---|---|---|---|---|
| `/` | `home-hero` | `jjt-home-hero` | `eyebrow`, `bottom_text`, `left_artwork_slug`, `right_artwork_slug`, `home_links` | Artwork/Collection |
| `/` | `home-introduction` | `jjt-image-text` | `eyebrow`, `heading`, `body`, `image`, `image_alt`, `button_label`, `button_destination` | — |
| `/` | `featured-section` | `jjt-featured-artwork` | `eyebrow`, `heading`, `summary`, `collection_slug`, `button_label`, `button_destination`, `featured_artwork_slugs` | Artwork/Collection |
| `/` | `quote-section` | `jjt-artist-quote` | `quotation`, `attribution` | — |
| `/` | `journal-feature` | `jjt-editorial-cta` | `eyebrow`, `heading`, `summary`, `button_label`, `button_destination` | — |
| `/about/` | `page-intro` | `jjt-page-intro` | `eyebrow`, `heading`, `summary` | — |
| `/about/` | `about-layout` | `jjt-biography` | `eyebrow`, `heading`, `summary`, `portrait_image`, `portrait_alt`, `paragraph_2`, `paragraph_3`, `paragraph_4` | — |
| `/about/` | `statement-section` | `jjt-artist-statement` | `eyebrow`, `heading`, `quotation`, `closing` | — |
| `/about/` | `education-section` | `jjt-education` | `eyebrow`, `heading`, `education_ids`, `supporting_text` | Education |
| `/about/` | `closing-note` | `jjt-editorial-cta` | `summary`, `button_label`, `button_destination` | — |
| `/current-work/` | `page-intro` | `jjt-page-intro` | `eyebrow`, `heading`, `summary` | — |
| `/current-work/` | `category-grid` | `jjt-category-grid` | `collection_slug` | Artwork/Collection |
| `/current-work/` | `closing-note` | `jjt-editorial-cta` | `summary`, `button_label`, `button_destination` | — |
| `/archive/` | `page-intro` | `jjt-page-intro` | `eyebrow`, `heading`, `summary` | — |
| `/archive/` | `category-grid` | `jjt-category-grid` | `collection_slug` | Artwork/Collection |
| `/archive/` | `closing-note` | `jjt-editorial-cta` | `summary`, `button_label`, `button_destination` | — |
| `/blog/` | `page-intro` | `jjt-page-intro` | `eyebrow`, `heading`, `summary` | — |
| `/blog/` | `journal-grid` | `jjt-journal-list` | `source_type` | Journal Post |
| `/blog/` | `closing-note` | `jjt-editorial-cta` | `button_label`, `button_destination`, `summary` | — |
| `/links/` | `page-intro` | `jjt-page-intro` | `eyebrow`, `heading`, `summary` | — |
| `/links/` | `links-list` | `jjt-links-list` | `source_type` | Artist Link |
| `/links/` | `contact-section` | `jjt-contact` | `eyebrow`, `heading`, `summary` | — |
| `/current-work/paintings/` | `page-intro` | `jjt-page-intro` | `heading`, `collection_slug`, `summary` | Artwork/Collection |
| `/current-work/paintings/` | `artwork-grid` | `jjt-gallery-grid` | `collection_slug`, `category` | Artwork/Collection |
| `/current-work/paintings/` | `closing-note` | `jjt-editorial-cta` | `button_label`, `button_destination`, `summary` | — |
| `/current-work/sculptures/` | `page-intro` | `jjt-page-intro` | `heading`, `collection_slug`, `summary` | Artwork/Collection |
| `/current-work/sculptures/` | `artwork-grid` | `jjt-gallery-grid` | `collection_slug`, `category` | Artwork/Collection |
| `/current-work/sculptures/` | `closing-note` | `jjt-editorial-cta` | `button_label`, `button_destination`, `summary` | — |
| `/archive/paintings/` | `page-intro` | `jjt-page-intro` | `heading`, `collection_slug`, `summary` | Artwork/Collection |
| `/archive/paintings/` | `artwork-grid` | `jjt-gallery-grid` | `collection_slug`, `category` | Artwork/Collection |
| `/archive/paintings/` | `closing-note` | `jjt-editorial-cta` | `button_label`, `button_destination`, `summary` | — |
| `/archive/sculptures/` | `page-intro` | `jjt-page-intro` | `heading`, `collection_slug`, `summary` | Artwork/Collection |
| `/archive/sculptures/` | `artwork-grid` | `jjt-gallery-grid` | `collection_slug`, `category` | Artwork/Collection |
| `/archive/sculptures/` | `closing-note` | `jjt-editorial-cta` | `button_label`, `button_destination`, `summary` | — |

### Non-panel templates

- Individual Artwork routes are rendered by the original `singleWork()` component, using `Artwork` fields and computed siblings.
- Individual Journal routes are rendered by the original article template, using `Journal Post` fields.
- Header and footer remain original frontend components; Menu is read via `main` and site identity/contact text from the Artist Settings entry.
- The two homepage background paintings are specifically editable in **Home → `jjt-home-hero` → `left_artwork_slug` / `right_artwork_slug`**. Choose existing published Artwork slugs. The homepage title/link subtitle content also lives in this panel.

## QA / build results

- Original root built: **335 HTML files including 404**, zero HTML validator errors.
- Simulated ServiceUp tenant build: **335 HTML files including 404**, zero HTML validator errors.
- Full normalized HTML audit: **335/335** original routes matched after stripping only the `/serviceup/` URL prefix; zero broken local links or assets found.
- Responsive offline headless checks: **1440px desktop**, **820px tablet**, **390px mobile**. Home/About/Paintings/Blog were checked for equal section sizes, heading content, link/image counts and horizontal overflow. Mobile menu and artwork lightbox open/close keyboard behaviors passed.
- Test edited Page panel reflected in generated static HTML, then default seed rebuilt to check exact parity.
- Negative test: unreachable API returned nonzero and left the previous generated homepage unchanged.
- Supplied Core App API tests: **30 passed, 0 failed**.

The browser runner here blocked local HTTP navigation, so responsive checks used directly injected generated HTML/CSS/JS and placeholder image pixels. This does **not** replace a final visual QA pass on the deployed Netlify URL with actual image loading and browser network requests. Live tenant import, Supabase Pixel uploads and Render/Netlify hook integration remain to be verified after deployment.

## Intentional differences

1. All ServiceUp URLs and asset paths live under `/serviceup/`. The original root copy stays unchanged.
2. ServiceUp copy is unindexable and its canonical URLs include `/serviceup/`.
3. Its static build reads published data from the tenant-scoped API; the original root copy still uses bundled source JSON.
4. The API receives a read-only public-menu endpoint plus Menu/Profile/import build-hook scheduling, without exposing admin credentials.
5. WordPress media reference metadata is available for editorial audit; original images are not yet registered in the live Pixels media library.

No intentional CSS, HTML section design, responsive rule, animation or JS interaction differences were introduced.
