import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readdir, readFile, stat } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = process.env.COMPENDIUM_ROOT || join(__dirname, "..", "..");

const CHAPTER_RE = /^chapter (\d{2})(?::| -) (.+)$/;
const ZH_CHAPTER_RE = /^第(\d{2})章 - (.+)$/;
const SECTION_RE = /^(\d{2})\. (.+)\.md$/;

type Lang = "en" | "zh";

const ZH_META_FILES: Record<string, string> = {
  glossary: "GLOSSARY.md",
  guide: "TRANSLATION_GUIDE.md",
  qa: "QA_REPORT.md",
  bibliography: "BIBLIOGRAPHY.md",
  index: "INDEX.md",
  learning_objectives: "LEARNING_OBJECTIVES.md",
  reader_report: "READER_REPORT_v2.md",
  fact_check: "FACT_CHECK_REPORT.md",
};

interface Chapter {
  number: number;
  name: string;
  path: string;
}

interface Section {
  number: number;
  name: string;
  path: string;
}

interface SectionMeta {
  chapter: number;
  chapterName: string;
  section: number;
  sectionName: string;
  description: string;
}

async function getChapters(lang: Lang = "en"): Promise<Chapter[]> {
  const baseDir = lang === "zh" ? join(ROOT, "zh") : ROOT;
  const re = lang === "zh" ? ZH_CHAPTER_RE : CHAPTER_RE;
  const entries = await readdir(baseDir);
  return entries
    .map((entry) => {
      const match = entry.match(re);
      if (!match) return null;
      return { number: parseInt(match[1], 10), name: match[2], path: join(baseDir, entry) };
    })
    .filter((ch): ch is Chapter => ch !== null)
    .sort((a, b) => a.number - b.number);
}

async function getSections(chapterPath: string): Promise<Section[]> {
  const entries = await readdir(chapterPath);
  return entries
    .map((entry) => {
      const match = entry.match(SECTION_RE);
      if (!match) return null;
      return { number: parseInt(match[1], 10), name: match[2], path: join(chapterPath, entry) };
    })
    .filter((s): s is Section => s !== null)
    .sort((a, b) => a.number - b.number);
}

async function parseLlmsTxt(): Promise<SectionMeta[]> {
  const content = await readFile(join(ROOT, "llms.txt"), "utf-8");
  const results: SectionMeta[] = [];
  let currentChapter = 0;
  let currentChapterName = "";

  for (const line of content.split("\n")) {
    const chapterMatch = line.match(/^### Chapter (\d+): (.+)$/);
    if (chapterMatch) {
      currentChapter = parseInt(chapterMatch[1], 10);
      currentChapterName = chapterMatch[2];
      continue;
    }

    const sectionMatch = line.match(/^- \[(.+?)\]\(.+?\): (.+)$/);
    if (sectionMatch && currentChapter > 0) {
      results.push({
        chapter: currentChapter,
        chapterName: currentChapterName,
        section: results.filter((r) => r.chapter === currentChapter).length + 1,
        sectionName: sectionMatch[1],
        description: sectionMatch[2],
      });
    }
  }
  return results;
}

const STOP_WORDS = new Set([
  "the", "and", "for", "are", "but", "not", "you", "all", "can", "had", "her", "was", "one",
  "our", "out", "has", "how", "its", "may", "who", "did", "get", "got", "let", "say", "she",
  "too", "use", "what", "why", "when", "where", "which", "with", "would", "could", "should",
  "about", "after", "been", "being", "between", "both", "does", "doing", "during", "each",
  "from", "have", "into", "just", "know", "like", "make", "more", "most", "much", "need",
  "only", "other", "over", "some", "such", "take", "than", "that", "them", "then", "there",
  "these", "they", "this", "very", "want", "well", "were", "will", "work", "your",
  "understand", "learn", "explain", "tell", "help",
]);

const server = new McpServer({
  name: "compendium",
  version: "1.0.0",
});

server.registerTool(
  "list_topics",
  {
    description: "List all chapters and sections in the compendium, or filter to a specific chapter",
    inputSchema: {
      chapter: z.number().optional().describe("Filter to a specific chapter number (1-20)"),
      lang: z.enum(["en", "zh"]).optional().describe("Language: 'en' (default) or 'zh' for Chinese"),
    },
  },
  async ({ chapter, lang }) => {
    const language: Lang = lang ?? "en";
    const chapters = await getChapters(language);
    const filtered = chapter ? chapters.filter((ch) => ch.number === chapter) : chapters;

    if (filtered.length === 0) {
      return { content: [{ type: "text", text: `Chapter ${chapter} not found. Valid chapters: 1-${chapters.length}.` }] };
    }

    const lines: string[] = [];
    for (const ch of filtered) {
      const sections = await getSections(ch.path);
      if (language === "zh") {
        lines.push(`\n## 第 ${ch.number} 章:${ch.name}`);
      } else {
        lines.push(`\n## Chapter ${ch.number}: ${ch.name}`);
      }
      for (const sec of sections) {
        lines.push(`  ${sec.number}. ${sec.name}`);
      }
    }

    return { content: [{ type: "text", text: lines.join("\n").trim() }] };
  },
);

server.registerTool(
  "read_section",
  {
    description: "Read the full content of a specific section from the compendium",
    inputSchema: {
      chapter: z.number().describe("Chapter number (1-20)"),
      section: z.number().describe("Section number (typically 0-7, varies by chapter)"),
      lang: z.enum(["en", "zh"]).optional().describe("Language: 'en' (default) or 'zh' for Chinese"),
    },
  },
  async ({ chapter, section, lang }) => {
    const language: Lang = lang ?? "en";
    const chapters = await getChapters(language);
    const ch = chapters.find((c) => c.number === chapter);
    if (!ch) {
      return { content: [{ type: "text", text: `Chapter ${chapter} not found. Valid chapters: 1-${chapters.length}.` }] };
    }

    const sections = await getSections(ch.path);
    const sec = sections.find((s) => s.number === section);
    if (!sec) {
      const valid = sections.map((s) => s.number).join(", ");
      return { content: [{ type: "text", text: `Section ${section} not found in Chapter ${chapter}: ${ch.name}. Valid sections: ${valid}.` }] };
    }

    const content = await readFile(sec.path, "utf-8");
    const header = language === "zh"
      ? `# 第 ${ch.number} 章:${ch.name} — ${sec.name}`
      : `# Chapter ${ch.number}: ${ch.name} — ${sec.name}`;
    return { content: [{ type: "text", text: `${header}\n\n${content}` }] };
  },
);

server.registerTool(
  "search",
  {
    description: "Search across all compendium sections for a term or phrase",
    inputSchema: {
      query: z.string().describe("Search term or phrase to find across all sections"),
      lang: z.enum(["en", "zh"]).optional().describe("Language: 'en' (default) or 'zh' for Chinese"),
    },
  },
  async ({ query, lang }) => {
    const language: Lang = lang ?? "en";
    const chapters = await getChapters(language);
    const results: string[] = [];
    const lowerQuery = query.toLowerCase();

    for (const ch of chapters) {
      const sections = await getSections(ch.path);
      for (const sec of sections) {
        const content = await readFile(sec.path, "utf-8");
        const lines = content.split("\n");
        const matches: string[] = [];

        for (let i = 0; i < lines.length; i++) {
          if (lines[i].toLowerCase().includes(lowerQuery)) {
            const start = Math.max(0, i - 2);
            const end = Math.min(lines.length - 1, i + 2);
            const excerpt = lines.slice(start, end + 1).join("\n");
            matches.push(`  Line ${i + 1}:\n${excerpt}`);
          }
        }

        if (matches.length > 0) {
          const label = language === "zh"
            ? `### 第 ${ch.number} 章:${ch.name} — ${sec.name}`
            : `### Chapter ${ch.number}: ${ch.name} — ${sec.name}`;
          results.push(`${label}\n${matches.slice(0, 3).join("\n\n")}`);
        }
      }

      if (results.length >= 20) break;
    }

    if (results.length === 0) {
      return { content: [{ type: "text", text: `No results found for "${query}".` }] };
    }

    return { content: [{ type: "text", text: `Found matches in ${results.length} sections:\n\n${results.join("\n\n")}` }] };
  },
);

server.registerTool(
  "recommend",
  {
    description: "Given a learning goal or question, recommend the most relevant compendium sections in suggested reading order",
    inputSchema: {
      query: z.string().describe("A learning goal or question, e.g. 'How do transformers work?' or 'What math do I need for ML?'"),
      lang: z.enum(["en", "zh"]).optional().describe("Language: 'en' (default, uses llms.txt) or 'zh' for Chinese (uses chapter/section names)"),
    },
  },
  async ({ query, lang }) => {
    const language: Lang = lang ?? "en";
    let meta: SectionMeta[];
    if (language === "zh") {
      const chapters = await getChapters("zh");
      meta = [];
      for (const ch of chapters) {
        const sections = await getSections(ch.path);
        for (const sec of sections) {
          meta.push({
            chapter: ch.number,
            chapterName: ch.name,
            section: sec.number,
            sectionName: sec.name,
            description: sec.name,
          });
        }
      }
    } else {
      meta = await parseLlmsTxt();
    }

    const keywords = query
      .toLowerCase()
      .split(/\W+/)
      .filter((w) => w.length > 2 && !STOP_WORDS.has(w));

    if (keywords.length === 0 && language === "en") {
      return { content: [{ type: "text", text: "Could not extract meaningful keywords from your query. Try using specific technical terms." }] };
    }

    // For zh, also include CJK-aware fallback: match raw substring against name/description
    const rawQuery = query.toLowerCase();
    const scored = meta.map((entry) => {
      const descLower = entry.description.toLowerCase();
      const nameLower = `${entry.chapterName} ${entry.sectionName}`.toLowerCase();

      let score = 0;
      for (const kw of keywords) {
        if (descLower.includes(kw)) score += 2;
        if (nameLower.includes(kw)) score += 3;
      }
      if (language === "zh" && rawQuery.length > 0) {
        if (nameLower.includes(rawQuery)) score += 5;
        if (descLower.includes(rawQuery)) score += 3;
      }
      return { ...entry, score };
    });

    const matches = scored
      .filter((s) => s.score > 0)
      .sort((a, b) => b.score - a.score || a.chapter - b.chapter)
      .slice(0, 15);

    if (matches.length === 0) {
      return { content: [{ type: "text", text: `No relevant sections found for "${query}". Try broader terms or use search for exact matches.` }] };
    }

    const byChapter = new Map<number, typeof matches>();
    for (const m of matches) {
      if (!byChapter.has(m.chapter)) byChapter.set(m.chapter, []);
      byChapter.get(m.chapter)!.push(m);
    }

    const lines: string[] = ["Recommended sections (in suggested reading order):\n"];
    for (const [chNum, sections] of [...byChapter.entries()].sort((a, b) => a[0] - b[0])) {
      const ch = sections[0];
      sections.sort((a, b) => a.section - b.section);
      if (language === "zh") {
        lines.push(`## 第 ${chNum} 章:${ch.chapterName}`);
      } else {
        lines.push(`## Chapter ${chNum}: ${ch.chapterName}`);
      }
      for (const sec of sections) {
        lines.push(`  ${sec.section}. ${sec.sectionName} — ${sec.description}`);
      }
      lines.push("");
    }

    return { content: [{ type: "text", text: lines.join("\n").trim() }] };
  },
);

server.registerTool(
  "get_examples",
  {
    description: "Extract code examples from the compendium, optionally filtered by topic or language. Returns implementation code with surrounding explanation.",
    inputSchema: {
      query: z.string().optional().describe("Topic to find examples for, e.g. 'attention mechanism' or 'CUDA kernel'"),
      language: z.string().optional().describe("Filter by programming language, e.g. 'python', 'cpp', 'bash'"),
      chapter: z.number().optional().describe("Filter to a specific chapter number (1-20)"),
      lang: z.enum(["en", "zh"]).optional().describe("Content language: 'en' (default) or 'zh' for Chinese"),
    },
  },
  async ({ query, language, chapter, lang }) => {
    const contentLang: Lang = lang ?? "en";
    const chapters = await getChapters(contentLang);
    const filtered = chapter ? chapters.filter((ch) => ch.number === chapter) : chapters;
    const lowerQuery = query?.toLowerCase();
    const results: string[] = [];

    for (const ch of filtered) {
      const sections = await getSections(ch.path);
      for (const sec of sections) {
        const content = await readFile(sec.path, "utf-8");
        const lines = content.split("\n");

        for (let i = 0; i < lines.length; i++) {
          const openMatch = lines[i].match(/^```(\w*)$/);
          if (!openMatch) continue;

          const lang = openMatch[1] || "text";
          if (language && lang !== language) continue;

          let end = i + 1;
          while (end < lines.length && lines[end] !== "```") end++;

          const code = lines.slice(i + 1, end).join("\n");
          if (!code.trim()) continue;

          const ctxStart = Math.max(0, i - 3);
          const context = lines.slice(ctxStart, i).filter((l) => l.trim()).join("\n");

          if (lowerQuery) {
            const searchable = `${context} ${code}`.toLowerCase();
            if (!searchable.includes(lowerQuery)) continue;
          }

          const label = contentLang === "zh"
            ? `### 第 ${ch.number} 章:${ch.name} — ${sec.name}`
            : `### Chapter ${ch.number}: ${ch.name} — ${sec.name}`;
          results.push(
            `${label}\n` +
              (context ? `${context}\n\n` : "") +
              `\`\`\`${lang}\n${code}\n\`\`\``,
          );

          if (results.length >= 10) break;
          i = end;
        }
        if (results.length >= 10) break;
      }
      if (results.length >= 10) break;
    }

    if (results.length === 0) {
      const filters = [query && `topic "${query}"`, language && `language "${language}"`, chapter && `chapter ${chapter}`].filter(Boolean).join(", ");
      return { content: [{ type: "text", text: `No code examples found for ${filters || "the given filters"}.` }] };
    }

    return { content: [{ type: "text", text: `Found ${results.length} code examples:\n\n${results.join("\n\n---\n\n")}` }] };
  },
);

server.registerTool(
  "list_zh_meta",
  {
    description: "List Chinese-version meta files (glossary, translation guide, QA report, etc.) with their existence status and file sizes.",
    inputSchema: {},
  },
  async () => {
    const zhDir = join(ROOT, "zh");
    const lines: string[] = ["Chinese meta files under zh/:\n"];
    for (const [shortName, filename] of Object.entries(ZH_META_FILES)) {
      const filePath = join(zhDir, filename);
      try {
        const st = await stat(filePath);
        const sizeKb = (st.size / 1024).toFixed(1);
        lines.push(`  ${shortName.padEnd(22)} ${filename.padEnd(28)} ${sizeKb} KB`);
      } catch {
        lines.push(`  ${shortName.padEnd(22)} ${filename.padEnd(28)} (missing)`);
      }
    }
    lines.push("\nUse read_zh_meta with the short name (e.g. 'glossary', 'guide', 'qa') to fetch content.");
    return { content: [{ type: "text", text: lines.join("\n") }] };
  },
);

server.registerTool(
  "read_zh_meta",
  {
    description: "Read a Chinese-version meta file. Use short names: glossary, guide, qa, bibliography, index, learning_objectives, reader_report, fact_check.",
    inputSchema: {
      filename: z
        .enum(["glossary", "guide", "qa", "bibliography", "index", "learning_objectives", "reader_report", "fact_check"])
        .describe("Short name mapping to a meta file under zh/"),
    },
  },
  async ({ filename }) => {
    const target = ZH_META_FILES[filename];
    if (!target) {
      return { content: [{ type: "text", text: `Unknown short name "${filename}". Valid: ${Object.keys(ZH_META_FILES).join(", ")}` }] };
    }
    const filePath = join(ROOT, "zh", target);
    try {
      const content = await readFile(filePath, "utf-8");
      return { content: [{ type: "text", text: `# ${target}\n\n${content}` }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Failed to read ${target}: ${err instanceof Error ? err.message : String(err)}` }] };
    }
  },
);

server.registerTool(
  "search_glossary",
  {
    description: "Search the Chinese glossary (zh/GLOSSARY.md) for a term. Matches bidirectionally against Chinese and English entries.",
    inputSchema: {
      term: z.string().describe("Term to search for (Chinese or English)"),
    },
  },
  async ({ term }) => {
    const filePath = join(ROOT, "zh", "GLOSSARY.md");
    let content: string;
    try {
      content = await readFile(filePath, "utf-8");
    } catch (err) {
      return { content: [{ type: "text", text: `Failed to read GLOSSARY.md: ${err instanceof Error ? err.message : String(err)}` }] };
    }

    const lower = term.toLowerCase();
    const lines = content.split("\n");
    const matches: string[] = [];

    for (let i = 0; i < lines.length; i++) {
      if (lines[i].toLowerCase().includes(lower)) {
        const start = Math.max(0, i - 1);
        const end = Math.min(lines.length - 1, i + 1);
        matches.push(`Line ${i + 1}:\n${lines.slice(start, end + 1).join("\n")}`);
      }
    }

    if (matches.length === 0) {
      return { content: [{ type: "text", text: `No glossary entries found for "${term}".` }] };
    }

    return { content: [{ type: "text", text: `Found ${matches.length} glossary matches for "${term}":\n\n${matches.slice(0, 30).join("\n\n")}` }] };
  },
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Compendium MCP server running on stdio");
}

main().catch((err) => {
  console.error("Failed to start server:", err);
  process.exit(1);
});
