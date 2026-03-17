import { PlaywrightCrawler } from '@crawlee/playwright';
import { Actor } from 'apify';
import { router } from './routes.js';
import fs from 'fs';

await Actor.init();

const storageState = JSON.parse(
  fs.readFileSync('./storageState.json','utf8')
);

const crawler = new PlaywrightCrawler({

    launchContext: {
        launchOptions: {
            headless: true
        }
    },

    preNavigationHooks: [
        async ({ page }) => {
            await page.context().addCookies(storageState.cookies);
        }
    ],

    requestHandler: router

});

await crawler.run([
    "https://www.skool.com/k21academy?c=&s=newest&fl="
]);

await Actor.exit();