import { createPlaywrightRouter } from '@crawlee/playwright';
import { Dataset } from 'apify';

export const router = createPlaywrightRouter();

const adminMembers = [
"yashee gupta","ritik wankhede","saswat gewali","heeyaichen konsam",
"aryaman pal","ritesh mahour","deepshi chopra","arti sharma",
"milind kuwar","shiv shrivastava","aryan tiwari","kritika aggarwal",
"kaynat mehdi","saurabh yadav","shubhangi anand","varsha deshpande",
"perminder kaur","supriya shrivastava","aniket gawandar","manish verma",
"pranjal aggarwal","mallika ghosh","richa sharma","gauri singhal",
"support ai data and cloud school","siram karthik",
"atul kumar","atisha sharma","sumti mehta"
];

function normalizeName(n){
  if(!n) return '';
  return String(n)
    .replace(/\u00A0/g,' ')
    .replace(/\s+/g,' ')
    .trim()
    .toLowerCase();
}

function convertRelativeTime(timeText){
  if(!timeText) return new Date().toISOString();

  const clean = String(timeText).replace(/\u00A0/g,' ').trim();
  const num = parseInt(clean,10);

  if(isNaN(num)) return new Date().toISOString();

  const now = new Date();

  if(clean.includes('m')) now.setMinutes(now.getMinutes()-num);
  else if(clean.includes('h')) now.setHours(now.getHours()-num);
  else if(clean.includes('d')) now.setDate(now.getDate()-num);

  return now.toISOString();
}

router.addDefaultHandler(async ({ page, log }) => {

  const baseFeed = 'https://www.skool.com/k21academy?c=&s=newest&fl=';

  const pagesToScrape = 2;
  const seenUrls = new Set();
  let saved = 0;

  for(let p=1;p<=pagesToScrape;p++){

    const pageUrl = `${baseFeed}&p=${p}`;

    log.info(`Scraping page ${p}`);

    await page.goto(pageUrl,{waitUntil:'domcontentloaded'});

    for(let i=0;i<5;i++){
      await page.mouse.wheel(0,2000);
      await page.waitForTimeout(800);
    }

    const posts = await page.$$eval(
      'a[href*="/k21academy/"]',
      links => {

        const data = [];

        for(const link of links){

          const container = link.closest('div');
          if(!container) continue;

          const txt = container.innerText || '';
          if(txt.length < 120) continue;

          const lines = txt
            .split('\n')
            .map(x=>x.trim())
            .filter(Boolean);

          if(lines.length < 4) continue;

          const likes = parseInt(lines[0]) || 0;
          const author = lines[1] || '';
          const rawDate = lines[2] || '';
          const category = lines[3] || '';

          const comments = parseInt(lines[lines.length-2]) || 0;

          const body = lines
            .slice(4,lines.length-2)
            .join('\n')
            .trim();

          const href = link.getAttribute('href');

          if(!href) continue;
          if(href.includes('?')) continue;

          data.push({
            author,
            rawDate,
            category,
            likes,
            comments,
            body,
            postUrl: href.startsWith('http')
              ? href
              : 'https://www.skool.com'+href
          });

        }

        return data;

      }
    );

    log.info(`Posts detected: ${posts.length}`);

    for(const post of posts){

      try{

        const cleanAuthor = normalizeName(post.author);

        if(!cleanAuthor) continue;

        if(adminMembers.includes(cleanAuthor)){
          log.info(`Skipping admin post: ${post.author}`);
          continue;
        }

        if(!post.postUrl) continue;

        if(seenUrls.has(post.postUrl)) continue;

        seenUrls.add(post.postUrl);

        const isoDate = convertRelativeTime(post.rawDate);

        await Dataset.pushData({
          author: post.author.trim(),
          category: post.category?.trim() || null,
          post_date: isoDate,
          raw_date: post.rawDate,
          likes: post.likes,
          comments_count: post.comments,
          post_url: post.postUrl,
          post_text: post.body,
          source_page: pageUrl,
          scraped_at: new Date().toISOString()
        });

        saved++;

      }catch(err){
        log.warning(`Skipping post error: ${err.message}`);
      }

    }

    log.info(`Finished page ${p}`);

  }

  log.info(`Scraping completed. Total saved: ${saved}`);

});