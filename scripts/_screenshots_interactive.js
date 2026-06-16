// Interactive functional captures.
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1366, height: 900 } });

  // Reports: click "Generate report" and capture the rendered Markdown.
  await page.goto("http://localhost:3001/reports", { waitUntil: "networkidle" });
  await page.getByRole("button", { name: /generate report/i }).click();
  await page.waitForSelector("pre", { timeout: 10000 });
  await page.waitForTimeout(500);
  await page.screenshot({ path: "docs/screenshots/internal-console/07-reports-generated.png", fullPage: true });
  console.log("OK   internal-console/07-reports-generated.png");

  // Knowledge base: run a search and capture results.
  await page.goto("http://localhost:3001/knowledge-base", { waitUntil: "networkidle" });
  await page.getByRole("button", { name: /^search$/i }).click();
  await page.waitForTimeout(800);
  await page.screenshot({ path: "docs/screenshots/internal-console/08-knowledge-search.png", fullPage: true });
  console.log("OK   internal-console/08-knowledge-search.png");

  await browser.close();
})();
