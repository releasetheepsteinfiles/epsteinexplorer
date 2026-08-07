# Promo renderer — Epstein Files toolchain

This directory is the **master asset set** for all four repos, and the
renderer that produces it. The other three repos carry copies of their own
clips plus the toolchain overview; this is where they come from.

## Output (`out/`)

Five clips, each in 16:9 and 1:1, plus a poster still:

| Prefix | Presents |
|---|---|
| `suite-*` | **Toolchain overview** — all four tools together |
| `exposed-*` | `epsteinexposed` — Python client |
| `mcp-*` | `epsteinexposed-mcp` — MCP, structured search |
| `rag-*` | `epstein-files-rag-mcp` — MCP, semantic search (roadmap) |
| `explorer-*` | `epsteinexplorer` — chat app |

All run 19.6s, H.264 / yuv420p, silent with burned-in text (both Twitter and
Reddit autoplay muted), ~330–430 KB each.

**Which to post when:** lead a repo-specific announcement with that repo's
clip; use `suite-*` when introducing the project as a whole. See
[`LAUNCH.md`](../LAUNCH.md) for the full sequencing.

## Rendering

```bash
npm install
npm run render                  # all five clips, both crops
node render.mjs suite           # one clip, both crops
node render.mjs suite wide      # one clip, one crop
node check-frames.mjs suite     # key frames only, for fast iteration
```

## How it works

`scene.html` exposes `renderAt(ms)` and renders **every visual as a pure
function of time** — no CSS animations, no wall-clock reads. `render.mjs`
steps a virtual clock, screenshots each frame, and pipes the PNGs straight
into ffmpeg via `image2pipe`.

Two consequences worth preserving if you edit this:

- **Output is reproducible.** Same input, same bytes, regardless of machine
  speed or load. A CSS animation would make frames depend on how fast the
  capture loop happened to run.
- **No intermediate files.** Ten clips × ~590 frames would otherwise be
  ~5,900 PNG writes.

Fonts are vendored in `fonts/` rather than fetched from Google Fonts at
capture time — a network fetch lets the first frames paint in a fallback
face and shifts the entire clip. See [`fonts/README.md`](fonts/README.md).

Chromium resolution: uses `PROMO_CHROMIUM`, else `/opt/pw-browsers/chromium`
if present, else Playwright's own download. The override exists because CI
images often ship a Chromium build that doesn't match the pinned Playwright
revision.

## Adding or editing a clip

Content lives in the `TOOLS` object in `scene.html`. Each entry drives the
same five-scene structure (logotype → pitch → demo → install → end card), so
new clips inherit the motion language for free. Three demo-panel variants
exist: code typing (default), `chat: true`, and `suite: true`.

Palette and type come from [`brand/DESIGN.md`](../brand/DESIGN.md) — the
tokens at the top of `scene.html` mirror `brand/tokens.css`.

## A note on content

No promo asset names any individual, and no redaction effect is applied over
a real record. Inclusion in these files is not an accusation. The demo
output is labelled "illustrative" on screen. See `brand/DESIGN.md`
§ Ethical constraints — these are binding, not stylistic preferences.
