#!/usr/bin/env node
import { createHash, randomUUID } from "node:crypto";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { spawn, spawnSync } from "node:child_process";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";

function parseArgs(argv) {
  const out = { sections: [], viewports: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--url") out.url = argv[++i];
    else if (arg === "--output-dir") out.outputDir = argv[++i];
    else if (arg === "--manifest") out.manifest = argv[++i];
    else if (arg === "--chrome") out.chrome = argv[++i];
    else if (arg === "--section") out.sections.push(argv[++i]);
    else if (arg === "--viewport") out.viewports.push(argv[++i]);
    else if (arg === "--wait-ms") out.waitMs = Number(argv[++i]);
    else throw new Error(`unknown argument: ${arg}`);
  }
  if (!out.url) throw new Error("--url is required");
  out.outputDir ||= "outputs/visual-qa";
  out.manifest ||= join(out.outputDir, "visual-manifest.json");
  out.waitMs = Number.isFinite(out.waitMs) ? out.waitMs : 900;
  if (!out.sections.length) throw new Error("at least one --section id=selector is required");
  if (!out.viewports.length) out.viewports = ["1440x1000", "390x844", "320x800"];
  return out;
}

function parsePairs(items, delimiter) {
  return items.map((item) => {
    const idx = item.indexOf(delimiter);
    if (idx <= 0) throw new Error(`invalid value: ${item}`);
    return [item.slice(0, idx), item.slice(idx + delimiter.length)];
  });
}

function chromeBinary(explicit) {
  if (explicit) return explicit;
  if (process.env.CHROME) return process.env.CHROME;
  for (const candidate of ["google-chrome", "chromium", "chromium-browser"]) {
    const found = spawnSync("which", [candidate], { encoding: "utf8" });
    if (found.status === 0 && found.stdout.trim()) return found.stdout.trim();
  }
  throw new Error("Chrome/Chromium not found; use --chrome or CHROME");
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function waitForJson(url, attempts = 60) {
  let lastError;
  for (let i = 0; i < attempts; i += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch (error) {
      lastError = error;
    }
    await sleep(150);
  }
  throw lastError || new Error(`timed out waiting for ${url}`);
}

class Cdp {
  constructor(webSocketUrl) {
    this.socket = new WebSocket(webSocketUrl);
    this.pending = new Map();
    this.seq = 0;
  }

  async connect() {
    await new Promise((resolve, reject) => {
      this.socket.addEventListener("open", resolve, { once: true });
      this.socket.addEventListener("error", reject, { once: true });
    });
    this.socket.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      if (!message.id || !this.pending.has(message.id)) return;
      const { resolve, reject } = this.pending.get(message.id);
      this.pending.delete(message.id);
      if (message.error) reject(new Error(JSON.stringify(message.error)));
      else resolve(message.result);
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = ++this.seq;
      this.pending.set(id, { resolve, reject });
      this.socket.send(JSON.stringify({ id, method, params }));
    });
  }

  close() {
    this.socket.close();
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const sections = parsePairs(args.sections, "=").map(([id, selector]) => ({ id, selector }));
  const viewports = args.viewports.map((value) => {
    const match = /^(\d+)x(\d+)$/.exec(value);
    if (!match) throw new Error(`invalid viewport: ${value}`);
    return { width: Number(match[1]), height: Number(match[2]) };
  });

  const outDir = resolve(args.outputDir);
  await mkdir(outDir, { recursive: true });
  const profileDir = await mkdtemp(join(tmpdir(), "agentic-factory-chrome-"));
  const port = 9222 + Math.floor(Math.random() * 500);
  const chrome = spawn(
    chromeBinary(args.chrome),
    [
      "--headless=new",
      "--no-sandbox",
      "--disable-gpu",
      "--disable-dev-shm-usage",
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${profileDir}`,
      "about:blank",
    ],
    { stdio: ["ignore", "ignore", "pipe"] },
  );

  try {
    const targets = await waitForJson(`http://127.0.0.1:${port}/json/list`);
    if (!targets.length) throw new Error("Chrome did not expose a page target");
    const cdp = new Cdp(targets[0].webSocketDebuggerUrl);
    await cdp.connect();
    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");

    const captures = [];
    const captureRunId = `browser-probe-${randomUUID()}`;
    const sectionAnchors = {};

    for (const section of sections) {
      const anchor = section.selector.startsWith("#") ? section.selector.slice(1) : section.id;
      sectionAnchors[section.id] = anchor;
    }

    for (const viewport of viewports) {
      await cdp.send("Emulation.setDeviceMetricsOverride", {
        width: viewport.width,
        height: viewport.height,
        deviceScaleFactor: 1,
        mobile: false,
        screenWidth: viewport.width,
        screenHeight: viewport.height,
      });

      for (const section of sections) {
        await cdp.send("Page.navigate", { url: args.url });
        await sleep(args.waitMs);

        const expression = `(() => {
          const selector = ${JSON.stringify(section.selector)};
          const el = document.querySelector(selector);
          if (!el) return { error: "missing_section", selector };
          el.scrollIntoView({ block: "start", inline: "nearest", behavior: "instant" });
          const heading = el.querySelector("h1,h2,h3,h4") || el;
          const bodyText = el.querySelector("p,li,figcaption") || document.body;
          const headingStyle = getComputedStyle(heading);
          const bodyStyle = getComputedStyle(bodyText);
          const box = el.getBoundingClientRect();
          const images = [...el.querySelectorAll("img")].map((img) => {
            const r = img.getBoundingClientRect();
            return {
              src: img.currentSrc || img.src || "",
              natural_width: img.naturalWidth,
              natural_height: img.naturalHeight,
              rendered_width: r.width,
              rendered_height: r.height,
              object_fit: getComputedStyle(img).objectFit,
            };
          });
          return {
            observed_heading: (heading.textContent || "").trim().replace(/\\s+/g, " ").slice(0, 240),
            document_metrics: {
              scroll_width: document.documentElement.scrollWidth,
              client_width: document.documentElement.clientWidth,
            },
            section_box: {
              left: box.left,
              right: box.right,
              width: box.width,
              height: box.height,
            },
            typography: {
              heading_tag: heading.tagName.toLowerCase(),
              heading_font_px: parseFloat(headingStyle.fontSize) || 0,
              body_font_px: parseFloat(bodyStyle.fontSize) || 0,
            },
            images,
          };
        })()`;

        const measured = await cdp.send("Runtime.evaluate", {
          expression,
          returnByValue: true,
          awaitPromise: true,
        });
        const metrics = measured?.result?.value;
        if (!metrics || metrics.error) {
          throw new Error(`section probe failed for ${section.id}: ${metrics?.error || "unknown"}`);
        }
        await sleep(160);

        const shot = await cdp.send("Page.captureScreenshot", {
          format: "png",
          fromSurface: true,
          captureBeyondViewport: false,
        });
        const bytes = Buffer.from(shot.data, "base64");
        const filename = `${viewport.width}-${section.id}.png`;
        const path = join(outDir, filename);
        await writeFile(path, bytes);

        captures.push({
          viewport_width: viewport.width,
          viewport_height: viewport.height,
          section_id: section.id,
          dom_anchor: sectionAnchors[section.id],
          artifact_ref: path,
          content_sha256: createHash("sha256").update(bytes).digest("hex"),
          observed_heading: metrics.observed_heading,
          reviewer_id: "browser-probe",
          review_run_id: captureRunId,
          status: "pass",
          document_metrics: metrics.document_metrics,
          section_box: metrics.section_box,
          typography: metrics.typography,
          images: metrics.images,
        });
      }
    }

    cdp.close();
    const manifest = {
      candidate_ref: args.url,
      require_geometry: true,
      required_viewports: viewports.map((item) => item.width),
      required_sections: sections.map((item) => item.id),
      section_anchors: sectionAnchors,
      constraints: {
        horizontal_overflow_tolerance_px: 2,
        max_image_aspect_ratio_delta: 0.04,
        min_heading_body_ratio: 1.4,
        max_heading_body_ratio: 7.5,
      },
      captures,
    };
    await mkdir(dirname(resolve(args.manifest)), { recursive: true });
    await writeFile(resolve(args.manifest), JSON.stringify(manifest, null, 2) + "\n");
    process.stdout.write(JSON.stringify({ manifest: resolve(args.manifest), captures: captures.length }) + "\n");
  } finally {
    chrome.kill("SIGTERM");
    await sleep(250);
    if (chrome.exitCode === null) chrome.kill("SIGKILL");
    await sleep(100);
    await rm(profileDir, { recursive: true, force: true }).catch(() => {});
  }
}

main().catch((error) => {
  console.error(error?.stack || String(error));
  process.exit(1);
});
