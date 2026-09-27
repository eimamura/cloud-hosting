# static-site

Static test site. Plain HTML/CSS/JS with a zero-dependency build step that writes `info.json`.

## Layout

```
public/        # Source files, deployable as-is (info.json will be missing)
build.mjs      # Copies public/ to dist/ and writes dist/info.json
```

## Build

```bash
npm run build        # -> dist/
npm run preview      # build and serve dist/ locally
```

No `npm install` is required.

## Platform settings

| Setting | Value |
| ------- | ----- |
| Root directory | `workloads/static-site` |
| Build command | `npm run build` (or none, publishing `public/` without `info.json`) |
| Output / publish directory | `dist` |
| 404 page | `404.html` (picked up automatically by GitHub Pages, Netlify, Cloudflare, Vercel, Firebase, Surge) |

See [../README.md](../README.md) for the probe contract and environment variables.
