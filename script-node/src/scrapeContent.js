import axios from "axios";
import cheerio from "cheerio";

export async function scrapeMainContent(url) {
  const { data: html } = await axios.get(url, { timeout: 20000 });
  const $ = cheerio.load(html);
  let contentEl = $("article").first();
  if (!contentEl.length) contentEl = $("main").first();
  if (!contentEl.length) contentEl = $(".post-content, .entry-content").first();
  if (!contentEl.length) contentEl = $("body");

  const contentHtml = contentEl.html() || "";
  const contentText = contentEl.text().trim();

  const title = $("h1").first().text().trim() || $("title").text().trim();
  return { title, url, contentHtml, contentText };
}
