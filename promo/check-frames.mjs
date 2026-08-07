#!/usr/bin/env node
/**
 * Captures a handful of key frames so the composition can be eyeballed
 * without paying for a full ~590-frame render.
 *
 * Usage: node promo/check-frames.mjs [tool] [wide|square]
 */
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, "out", "check");

const SIZES = { wide: [1920, 1080], square: [1080, 1080] };

// One frame from the middle of each scene, plus the two busiest moments.
const MARKS = [1600, 2400, 4800, 8200, 11800, 13600, 15900, 18600];

const tool = process.argv[2] || "explorer";
const fmt = process.argv[3] || "wide";

// Guard the easy mistake of passing the output *label* ("16x9") rather than
// the format key ("wide"), which otherwise dies with an opaque
// "SIZES[fmt] is not iterable".
if (!SIZES[fmt]) {
  console.error(
    `unknown format "${fmt}" — expected one of: ${Object.keys(SIZES).join(", ")}`,
  );
  process.exit(1);
}

const [w, h] = SIZES[fmt];

const { chromium } = await import("playwright");

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({
  executablePath:
    process.env.PROMO_CHROMIUM ||
    (existsSync("/opt/pw-browsers/chromium") ? "/opt/pw-browsers/chromium" : undefined),
  args: ["--force-color-profile=srgb", "--disable-lcd-text"],
});
const page = await browser.newPage({ viewport: { width: w, height: h } });

await page.goto(pathToFileURL(join(HERE, "scene.html")).href, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
await page.evaluate(([t, ww, hh]) => window.buildScene(t, ww, hh), [tool, w, h]);

const stage = page.locator("#stage");
for (const t of MARKS) {
  await page.evaluate((ms) => window.renderAt(ms), t);
  const buf = await stage.screenshot({ type: "png", animations: "disabled" });
  const file = join(OUT, `${tool}-${fmt}-${String(t).padStart(5, "0")}.png`);
  writeFileSync(file, buf);
  console.log("wrote", file);
}

await browser.close();
