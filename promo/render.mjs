#!/usr/bin/env node
/**
 * Renders the promo videos for the Epstein Files toolchain.
 *
 * scene.html exposes renderAt(ms) as a pure function of time, so this
 * driver simply steps a virtual clock and screenshots each frame —
 * output is deterministic and independent of machine speed.
 *
 * Frames are piped straight into ffmpeg (image2pipe) rather than
 * written to disk: ~590 frames per clip × 8 clips would otherwise be
 * ~4,700 PNG writes.
 *
 * Usage:
 *   node promo/render.mjs                 # all tools, both formats
 *   node promo/render.mjs explorer        # one tool
 *   node promo/render.mjs explorer wide   # one tool, one format
 *
 * Requires: playwright, ffmpeg-static (see promo/package.json).
 */
import { spawn } from "node:child_process";
import { mkdirSync, existsSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, "out");

const FPS = 30;

// "suite" is the umbrella clip presenting all four tools; it ships in
// every repo alongside that repo's own clip.
const TOOLS = ["suite", "exposed", "mcp", "rag", "explorer"];

const FORMATS = {
  wide: { w: 1920, h: 1080, label: "16x9" },
  square: { w: 1080, h: 1080, label: "1x1" },
};

/** Poster frame (ms) — picked inside the demo scene, fully settled. */
const POSTER_AT = 13200;

/**
 * Preinstalled Chromium, when the image ships a build that does not match
 * the pinned Playwright revision. Override with PROMO_CHROMIUM; leave unset
 * to use Playwright's own download.
 */
const CHROMIUM_PATH =
  process.env.PROMO_CHROMIUM ||
  (existsSync("/opt/pw-browsers/chromium") ? "/opt/pw-browsers/chromium" : undefined);

async function resolveDeps() {
  const { chromium } = await import("playwright");
  const ffmpegMod = await import("ffmpeg-static");
  const ffmpeg = ffmpegMod.default ?? ffmpegMod;
  if (!ffmpeg) throw new Error("ffmpeg-static did not resolve to a binary path");
  return { chromium, ffmpeg };
}

function encoder(ffmpeg, outFile, fps) {
  const args = [
    "-y",
    "-f", "image2pipe",
    "-framerate", String(fps),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "slow",
    "-crf", "21",
    "-pix_fmt", "yuv420p",
    // Twitter/Reddit inline players want a moov atom up front.
    "-movflags", "+faststart",
    outFile,
  ];
  const proc = spawn(ffmpeg, args, { stdio: ["pipe", "ignore", "pipe"] });
  let stderr = "";
  proc.stderr.on("data", (d) => (stderr += d.toString()));
  const done = new Promise((res, rej) => {
    proc.on("close", (code) =>
      code === 0 ? res() : rej(new Error(`ffmpeg exited ${code}\n${stderr.slice(-2000)}`)),
    );
    proc.on("error", rej);
  });
  return { proc, done };
}

/** Backpressure-aware write. */
function write(stream, buf) {
  return stream.write(buf) ? Promise.resolve() : new Promise((r) => stream.once("drain", r));
}

async function renderClip(browser, ffmpeg, tool, fmtKey) {
  const { w, h, label } = FORMATS[fmtKey];
  const outFile = join(OUT, `${tool}-${label}.mp4`);

  const page = await browser.newPage({
    viewport: { width: w, height: h },
    deviceScaleFactor: 1,
  });

  await page.goto(pathToFileURL(join(HERE, "scene.html")).href, {
    waitUntil: "load",
  });

  // Local woff2s must be parsed before the first paint or early frames
  // silently fall back to DejaVu and the whole clip shifts.
  await page.evaluate(() => document.fonts.ready);

  const duration = await page.evaluate(
    ([t, ww, hh]) => {
      window.buildScene(t, ww, hh);
      return window.SCENE_DURATION;
    },
    [tool, w, h],
  );

  const frames = Math.round((duration / 1000) * FPS);
  const { proc, done } = encoder(ffmpeg, outFile, FPS);

  const stage = page.locator("#stage");

  for (let i = 0; i < frames; i++) {
    const t = (i / FPS) * 1000;
    await page.evaluate((ms) => window.renderAt(ms), t);
    const buf = await stage.screenshot({ type: "png", animations: "disabled" });
    await write(proc.stdin, buf);

    if (i % 120 === 0) {
      process.stdout.write(`    ${tool}/${label}  frame ${i}/${frames}\r`);
    }
  }

  proc.stdin.end();
  await done;

  // Poster still, for README embeds and link previews.
  if (fmtKey === "wide") {
    await page.evaluate((ms) => window.renderAt(ms), POSTER_AT);
    const poster = await stage.screenshot({ type: "png", animations: "disabled" });
    writeFileSync(join(OUT, `${tool}-poster.png`), poster);
  }

  await page.close();
  return outFile;
}

async function main() {
  const [argTool, argFmt] = process.argv.slice(2);
  const tools = argTool ? [argTool] : TOOLS;
  const formats = argFmt ? [argFmt] : Object.keys(FORMATS);

  for (const t of tools) {
    if (!TOOLS.includes(t)) throw new Error(`unknown tool "${t}" (want: ${TOOLS.join(", ")})`);
  }
  for (const f of formats) {
    if (!FORMATS[f]) throw new Error(`unknown format "${f}" (want: ${Object.keys(FORMATS).join(", ")})`);
  }

  if (!existsSync(OUT)) mkdirSync(OUT, { recursive: true });

  const { chromium, ffmpeg } = await resolveDeps();
  const browser = await chromium.launch({
    executablePath: CHROMIUM_PATH,
    args: ["--force-color-profile=srgb", "--disable-lcd-text"],
  });

  try {
    for (const tool of tools) {
      for (const fmt of formats) {
        const started = process.hrtime.bigint();
        const file = await renderClip(browser, ffmpeg, tool, fmt);
        const secs = Number(process.hrtime.bigint() - started) / 1e9;
        console.log(`  ✓ ${file.replace(HERE + "/", "")}  (${secs.toFixed(1)}s)`);
      }
    }
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
