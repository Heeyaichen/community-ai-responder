# Community AI Responder - Development Guide

## Project Overview

Apify Actor for scraping community posts from Skool.com using PlaywrightCrawler. Filters out admin posts and extracts post metadata for AI response automation.

## Commands

```bash
# Development
npm start                    # Run the Actor locally
npx apify run                # Run via Apify CLI (requires apify-cli)

# Code Quality
npm run lint                 # Check code with ESLint (run npx eslint . if npm fails)
npm run lint:fix             # Auto-fix ESLint issues
npm run format               # Format code with Prettier
npm run format:check         # Check formatting without modifying

# Testing
npm test                     # No tests yet (placeholder exits with error)

# Deployment
npx apify login              # Authenticate with Apify
npx apify push               # Deploy to Apify platform
```

## Code Style

### Language & Modules

- **JavaScript ES Modules** (`"type": "module"` in package.json)
- Use top-level `await` at entry points
- Always include `.js` extension in local imports: `import { router } from './routes.js'`

### Imports

```javascript
// External packages first (named imports preferred)
import { PlaywrightCrawler } from "@crawlee/playwright";
import { Actor, Dataset } from "apify";
// Then local modules
import { router } from "./routes.js";
import fs from "fs";
```

### Formatting

- **Prettier** handles all formatting
- Run `npm run format` before committing
- No manual formatting debates - prettier wins

### Naming Conventions

| Type            | Convention                   | Example                                    |
| --------------- | ---------------------------- | ------------------------------------------ |
| Variables       | camelCase                    | `cleanAuthor`, `pagesToScrape`, `postUrl`  |
| Functions       | camelCase                    | `normalizeName()`, `convertRelativeTime()` |
| Constants       | camelCase for arrays/objects | `adminMembers`, `baseFeed`                 |
| Data properties | snake_case                   | `post_date`, `raw_date`, `post_url`        |
| Files           | lowercase with dot extension | `main.js`, `routes.js`                     |

### Async/Await

- Always use `async/await`, never `.then()` chains
- Use `try/catch` for error handling in async functions

## Architecture Patterns

### Router Pattern

Use `createPlaywrightRouter()` for organizing handlers:

```javascript
import { createPlaywrightRouter } from "@crawlee/playwright";

export const router = createPlaywrightRouter();

router.addDefaultHandler(async ({ page, log }) => {
  // Handler logic
});
```

### Main Entry Point

```javascript
import { PlaywrightCrawler } from "@crawlee/playwright";
import { Actor } from "apify";
import { router } from "./routes.js";

await Actor.init();

const crawler = new PlaywrightCrawler({
  launchContext: { launchOptions: { headless: true } },
  requestHandler: router,
});

await crawler.run(["https://example.com"]);
await Actor.exit();
```

### Error Handling

```javascript
// Use log methods from context, not console
router.addDefaultHandler(async ({ page, log }) => {
  try {
    // Risky operation
  } catch (err) {
    log.warning(`Skipping item: ${err.message}`);
  }
});
```

## Data Output

Push data using `Dataset.pushData()` with snake_case properties:

```javascript
await Dataset.pushData({
  author: post.author.trim(),
  post_date: isoDate,
  post_url: post.postUrl,
  scraped_at: new Date().toISOString(),
});
```

## Playwright-Specific Notes

- Wait for content after navigation: `await page.waitForTimeout(ms)`
- Scroll dynamic content: `await page.mouse.wheel(0, pixels)`
- Use `page.$$eval()` for batch element extraction
- Set `waitUntil: 'domcontentloaded'` for faster page loads

## Important Rules

### Do

- Run `npm run format` and `npm run lint` before committing
- Use `log.info()`, `log.warning()`, `log.error()` from handler context
- Validate/filter data before pushing to Dataset
- Handle pagination and rate limiting explicitly

### Don't

- Don't use `console.log` - use Apify's log methods
- Don't skip `await Actor.init()` at startup or `await Actor.exit()` at end
- Don't store sensitive data (tokens, credentials) in code or logs
- Don't use browser crawlers when HTTP/Cheerio would work (performance)

## Project Structure

```
src/
├── main.js      # Entry point, crawler setup, Actor lifecycle
└── routes.js    # Router definitions, scraping logic, data processing
storageState.json # Cookie state for authenticated scraping
Dockerfile       # Apify container definition
eslint.config.mjs # ESLint configuration (extends @apify/eslint-config)
```

## Dependencies

- `apify` - Apify SDK for Actor lifecycle, Dataset, logging
- `@crawlee/playwright` - Crawlee's Playwright integration
- `playwright` - Browser automation

## Resources

- [Crawlee Documentation](https://crawlee.dev)
- [Apify SDK Docs](https://docs.apify.com/sdk/js)
- [Playwright Docs](https://playwright.dev)
