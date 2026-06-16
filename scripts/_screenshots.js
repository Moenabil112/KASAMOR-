// Screenshot capture for KASAMOR validation.
// Run: NODE_PATH=/opt/node22/lib/node_modules PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node scripts/_screenshots.js
const { chromium } = require("playwright");

const SHOTS = [
  // public interface (port 3000)
  ["http://localhost:3000/", "public/01-homepage.png"],
  ["http://localhost:3000/ecosystem", "public/02-ecosystem.png"],
  ["http://localhost:3000/how-it-works", "public/03-how-it-works.png"],
  ["http://localhost:3000/mvp", "public/04-mvp.png"],
  ["http://localhost:3000/partners", "public/05-partners.png"],
  // internal console (port 3001)
  ["http://localhost:3001/", "internal-console/01-overview.png"],
  ["http://localhost:3001/knowledge-base", "internal-console/02-knowledge-base.png"],
  ["http://localhost:3001/field-packets", "internal-console/03-field-packets.png"],
  ["http://localhost:3001/field-packets/KSM-FP-0001", "internal-console/04-field-packet-detail.png"],
  ["http://localhost:3001/review", "internal-console/05-review.png"],
  ["http://localhost:3001/reports", "internal-console/06-reports.png"],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1366, height: 900 } });
  for (const [url, out] of SHOTS) {
    try {
      await page.goto(url, { waitUntil: "networkidle", timeout: 20000 });
      await page.waitForTimeout(600);
      await page.screenshot({ path: `docs/screenshots/${out}`, fullPage: true });
      console.log(`OK   ${out}  <-  ${url}`);
    } catch (e) {
      console.log(`FAIL ${out}  <-  ${url}  (${e.message})`);
    }
  }
  await browser.close();
})();
