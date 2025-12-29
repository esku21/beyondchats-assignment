import axios from "axios";

export async function publishUpdatedArticle(backendBaseUrl, originalId, title, updatedHtml, citations) {
  const payload = {
    title,
    url: null,
    content_html: updatedHtml,
    content_text: null,
    is_updated_version: true,
    origin_id: originalId,
    citations
  };
  const { data } = await axios.post(`${backendBaseUrl}/articles`, payload);
  return data;
}
