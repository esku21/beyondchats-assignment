import axios from "axios";

export async function searchTopBlogs(query, apiKey, cseId, maxResults = 5) {
  const params = {
    key: apiKey,
    cx: cseId,
    q: query
  };
  const url = "https://www.googleapis.com/customsearch/v1";
  const { data } = await axios.get(url, { params });
  const items = (data.items || []).filter(it => {
    const link = (it.link || "").toLowerCase();
    return link.includes("/blog") || link.includes("/article") || link.includes("/posts");
  });
  return items.slice(0, maxResults).map(it => ({ title: it.title, link: it.link }));
}
