<p align="center">
  <img src="static/images/logo.png" alt="Hypergraphx-data" width="260">
</p>

This repository hosts the generated GitHub Pages website for the Hypergraphx-data dataset catalog.

Live site: https://hgx-team.github.io/hypergraphx-data/

## Source Repository

Do not edit generated files in this repository directly.

The source dataset metadata, templates, build scripts, and maintenance tools live in:

https://github.com/HGX-Team/hypergraphx-data-backend

Changes should be made in the backend repository and deployed from there.

## What Is Published Here

- `index.html`: dataset catalog homepage
- `datasets/`: generated per-dataset pages
- `statistics.html`: generated catalog statistics page
- `about.html`: static about page
- `static/`: generated CSS, JavaScript, images, and figures
- `reproducibility/`: public reproducibility notes and scripts copied from the backend repository

## Deployment

The site is deployed from the backend repository with:

```bash
scripts/deploy_pages.sh --push
```

That command builds the static site, copies the generated output into this repository, copies `reproducibility/`, commits the result, and pushes to GitHub Pages.

## Reporting Issues

Please report dataset, metadata, website, or attribution issues in the backend repository:

https://github.com/HGX-Team/hypergraphx-data-backend/issues
