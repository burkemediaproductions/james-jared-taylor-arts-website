# WordPress media and content migration — Version 2

Imported from the WordPress XML export dated November 12, 2026 and seven uploaded ZIP archives.

## Counts

- 584 attachment records matched to filenames in archives (100%).
- 315 images were classified from WordPress titles/captions, converted to optimized WebP and included in the portfolio gallery.
- 267 media records require review or are supporting items, duplicate imagery, installation photos, and site assets; their metadata is preserved in `content/wordpress-media-inventory.json`.
- 2 attachment images could not be decoded for WebP conversion (WordPress attachment IDs 700 and 701); their original files remain in the user's uploaded archives.
- 9 published blog posts imported with original dates and text extracted to structured paragraph arrays.
- 335 generated HTML pages include the homepage, galleries, artwork records, blog entries and 404.

## Important editorial review

The original site did not consistently store Current Work vs Archive as separate fields for every attachment. This version provisionally assigns 2015–2016 uploads to Archive and later uploads to Current Work. **Upload dates are not artwork creation dates**, and artwork title, medium, series or caption may be incomplete. Ask James to review the split and labels before going live.

Some WordPress attachments represent alternate images of the same sculpture or piece. Each currently appears as its own record where caption/title classification suggests art. Consolidate related views as `images[]` on the same future ServiceUp artwork entry, based on a review of the photographs.

No private SQL/user data was bundled into this ZIP. The site does not connect to ServiceUp yet. All metadata and media paths are local; original images from the supplied archives can be retrieved without WordPress.

## Structure

- `content/works.json`: structured artworks, source WordPress IDs, original captions, local image paths and provisional category/collection.
- `content/posts.json`: published WordPress posts, dates and content.
- `content/wordpress-media-inventory.json`: full attachment manifest with source URLs and original filenames.
- `content/migration-report.json`: audit summary.
- `public/assets/images/works/`: WebP images for the new galleries and artwork pages.
- `dist/`: static HTML output for upload/deployment.

## Local development

With Node.js 20+: run `npm run dev` and visit the local URL reported by the terminal. Run `npm run build` and `npm run check` after making content changes.

For a staging deploy, use `SITE_ENV=staging` at build time to apply `noindex` metadata and robots policy. No ServiceUp API keys or build hooks should be added until integration is explicitly requested.
