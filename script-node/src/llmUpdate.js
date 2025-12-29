import OpenAI from "openai";

export async function generateUpdatedArticle(original, references, apiKey) {
  const client = new OpenAI({ apiKey });
  const prompt = `
You are updating an article to closely match the formatting and quality of two reference articles that rank on Google.

Original Article Title: ${original.title}
Original Article Content (plain text):
${original.content_text}

Reference A (URL: ${references[0].url}):
${references[0].content_text.slice(0, 4000)}

Reference B (URL: ${references[1].url}):
${references[1].content_text.slice(0, 4000)}

Instructions:
- Keep the original topic and intent.
- Improve structure: add headings, subheadings, bullet points where useful.
- Align formatting style with references (tone, paragraphing, headings).
- Maintain factual integrity; do not invent data.
- Produce clean HTML with semantic tags (<h2>, <p>, <ul>, <li>, <blockquote>).
- At bottom, add a "References" section with links to Reference A and B.

Output:
Return only HTML for the updated article body (no external CSS/JS).
  `.trim();

  const resp = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: "You are an expert editor and formatter for web articles." },
      { role: "user", content: prompt }
    ],
    temperature: 0.4
  });

  const html = resp.choices[0].message.content;
  return html;
}
