import dotenv from "dotenv";
dotenv.config();

import axios from "axios";
import { searchTopBlogs } from "./src/googleSearch.js";
import { scrapeMainContent } from "./src/scrapeContent.js";
import { generateUpdatedArticle } from "./src/llmUpdate.js";
import { publishUpdatedArticle } from "./src/publishUpdated.js";

const BACKEND = process.env.BACKEND_BASE_URL;
const GOOGLE_API_KEY = process.env.GOOGLE_API_KEY;
const GOOGLE_CSE_ID = process.env.GOOGLE_CSE_ID;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

async function getOriginalArticles() {
  const { data } = await axios.get(`${BACKEND}/articles?limit=50`);
  return data.filter(a => !a.is_updated_version);
}

async function run() {
  const originals = await getOriginalArticles();
  for (const orig of originals) {
    console.log("Processing:", orig.title);

    // 1) Search Google by title
    const results = await searchTopBlogs(orig.title, GOOGLE_API_KEY, GOOGLE_CSE_ID, 5);
    const topTwo = results.slice(0, 2);
    if (topTwo.length < 2) {
      console.log("Skipping; less than two suitable results.");
      continue;
    }

    // 2) Scrape both references
    const refs = [];
    for (const r of topTwo) {
      const scraped = await scrapeMainContent(r.link);
      refs.push({ title: scraped.title || r.title, url: r.link, content_html: scraped.contentHtml, content_text: scraped.contentText });
    }

    // 3) Call LLM to update original content
    const updatedHtml = await generateUpdatedArticle(orig, refs, OPENAI_API_KEY);

    // 4) Add citations footer if not present
    const refsBlock = `
<section>
  <h3>References</h3>
  <ul>
    <li><a href="${refs[0].url}" target="_blank" rel="noopener">${refs[0].title || "Reference 1"}</a></li>
    <li><a href="${refs[1].url}" target="_blank" rel="noopener">${refs[1].title || "Reference 2"}</a></li>
  </ul>
</section>`;
    const finalHtml = `${updatedHtml}\n${refsBlock}`;

    // 5) Publish via backend API, linking to origin
    const citations = [
      { title: refs[0].title, url: refs[0].url },
      { title: refs[1].title, url: refs[1].url }
    ];

    const published = await publishUpdatedArticle(BACKEND, orig.id, `Updated: ${orig.title}`, finalHtml, citations);
    console.log("Published updated article ID:", published.id);
  }
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
