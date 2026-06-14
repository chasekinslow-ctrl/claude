---
name: research
description: Multi-source research skill. Queries Brave Search, Perplexity AI, Tavily, Exa, and Context7 in parallel then synthesizes a unified answer. Use when the user invokes /research or wants comprehensive research on any topic. Also use when an agent is stuck and needs external knowledge — pass --compact for terse output. Supports flags --brave --perplexity --tavily --exa --docs --compact --setup.
version: 2.1.0
argument-hint: <query> [--brave] [--perplexity] [--tavily] [--exa] [--docs] [--compact] [--setup]
allowed-tools: [WebFetch, Bash, Agent, Read]
---

# Multi-Source Research

You are a research assistant. When invoked, you search multiple sources in parallel and synthesize a single comprehensive answer.

---

## Setup Check

If the user passes `--setup`, OR if this appears to be the first run and no sources are available, run the setup check.

### Step 1: Check environment variables

```bash
echo "=== Research Source Status ==="
echo ""
echo "API Keys:"
echo "  BRAVE:      ${BRAVE_API_KEY:+CONFIGURED}${BRAVE_API_KEY:-MISSING}"
echo "  TAVILY:     ${TAVILY_API_KEY:+CONFIGURED}${TAVILY_API_KEY:-MISSING}"
echo "  EXA:        ${EXA_API_KEY:+CONFIGURED}${EXA_API_KEY:-MISSING}"
echo "  PERPLEXITY: ${PERPLEXITY_API_KEY:+CONFIGURED}${PERPLEXITY_API_KEY:-MISSING}"
echo "  CONTEXT7:   no key needed"
echo ""
echo "Prerequisites:"
echo "  npx: $(command -v npx >/dev/null && echo 'INSTALLED' || echo 'MISSING — install Node.js')"
```

### Step 2: Check MCP tool availability

After checking env vars, also verify the MCP tools are actually loaded. Attempt to list/check for the existence of these MCP tools:
- `brave_web_search` (from brave-search MCP server)
- `tavily_search` (from tavily MCP server)
- `web_search_exa` (from exa MCP server)
- Context7 tools (from context7 MCP server)

A source is only truly ready when BOTH conditions are met:
- The API key is set (env var) — except Context7 which needs no key
- The MCP server is loaded and its tools are available

If a source has the env var set but the MCP tool is missing, tell the user:
> "BRAVE_API_KEY is set, but the brave-search MCP server isn't loaded. Make sure the plugin's .mcp.json includes the brave-search entry and restart Claude Code."

### Step 3: Show setup instructions for missing sources

For any source that isn't fully configured, show:

**Brave Search** (web + news search)
- Sign up at https://brave.com/search/api/ — free tier: 2,000 queries/month
- Add to your shell profile: `export BRAVE_API_KEY="your-key"`

**Tavily** (AI-optimized search)
- Sign up at https://tavily.com — free tier: 1,000 queries/month
- Add to your shell profile: `export TAVILY_API_KEY="your-key"`

**Exa** (semantic search, good for niche/academic content)
- Sign up at https://exa.ai — free tier: 1,000 queries/month
- Add to your shell profile: `export EXA_API_KEY="your-key"`

**Perplexity** (AI-powered answer engine)
- Sign up at https://docs.perplexity.ai — requires paid credits
- Add to your shell profile: `export PERPLEXITY_API_KEY="your-key"`
- No MCP server needed — uses WebFetch directly

**Context7** (programming library docs)
- No API key needed — just requires `npx`
- Should work automatically via this plugin's MCP config

After adding env vars, remind the user to restart their terminal and Claude Code.

### Step 4: Summary

Tell the user which sources are ready and offer to proceed with what's available. The skill works with **any subset of sources** — even a single source is useful.

---

## Parsing the Query

1. Extract the research question from the user's input (everything after `/research` that isn't a flag).
2. Check for source flags: `--brave`, `--perplexity`, `--tavily`, `--exa`, `--docs`, `--compact`.
3. If source flags are present, query ONLY those sources (skip any that aren't configured — warn the user).
4. If no source flags are present, query ALL CONFIGURED sources in parallel (except Context7 — only include it if the query is clearly about a programming library, framework, or API).

## Source Availability Detection

Before launching agents, determine which sources are actually available:

- **Brave**: available if the `brave_web_search` MCP tool exists AND responds
- **Tavily**: available if the `tavily_search` MCP tool exists AND responds
- **Exa**: available if the `web_search_exa` MCP tool exists AND responds
- **Perplexity**: available if `PERPLEXITY_API_KEY` env var is set (check via Bash: `echo ${PERPLEXITY_API_KEY:+yes}`)
- **Context7**: available if Context7 MCP tools exist

**Only launch agents for sources that are available.** Do not attempt to use unconfigured sources — it wastes time and produces errors.

If no sources are available, tell the user to run `/research --setup` and stop.

If only some sources are available, proceed with what's available. Do NOT warn about missing sources on every run — only mention it if the user specifically asks or uses `--setup`.

---

## Executing Searches

Launch one Agent subagent per available source, in parallel. Each agent should be given the research question and instructed to use its specific tool.

### Brave Search Agent
Use the `brave_web_search` MCP tool with the query. If the query seems time-sensitive or news-related, also call `brave_news_search`. Return the top 5-8 results with titles, URLs, and snippet summaries.

### Perplexity Agent
Use WebFetch to POST to the Perplexity API:

```
URL: https://api.perplexity.ai/chat/completions
Method: POST
Headers:
  Authorization: Bearer <PERPLEXITY_API_KEY value>
  Content-Type: application/json
Body:
{
  "model": "sonar",
  "messages": [
    {"role": "user", "content": "<the research question>"}
  ]
}
```

Read the API key from the environment: run `echo $PERPLEXITY_API_KEY` via Bash to get the value before building the request.

Extract the response content and any citations.

### Tavily Agent
Use the `tavily_search` MCP tool with the query. Request `include_raw_content: false` and `max_results: 8` for efficiency. Return results with titles, URLs, and content snippets.

### Exa Agent
Use the `web_search_exa` MCP tool with the query. This is especially valuable for finding niche content, academic papers, and semantically similar results that keyword search misses. Return the top results with titles, URLs, and content.

### Context7 Agent (conditional)
Only run this agent if:
- The `--docs` flag is present, OR
- The query explicitly mentions a library, framework, SDK, or API by name

AND the Context7 MCP tools are available.

Use the Context7 MCP tools to look up relevant documentation.

---

## Synthesizing Results

After all agents return, combine their findings. The output format depends on whether `--compact` was passed.

### Standard mode (default — for humans)

1. **Direct Answer** — Lead with a clear, concise answer to the question. Do not start with "Based on my research" or similar preamble.

2. **Key Findings** — Bullet points of the most important facts, deduplicated across sources. When multiple sources agree on something, that increases confidence. When they disagree, note the disagreement.

3. **Source Comparison** — A brief note on which sources were most useful for this particular query. This helps the user understand which sources to use for similar questions in the future.

4. **References** — List the most relevant URLs grouped by source, so the user can dig deeper.

5. **Confidence** — End with a confidence indicator:
   - HIGH: Multiple sources converge on the same answer
   - MEDIUM: Sources partially agree or the topic is nuanced
   - LOW: Sources disagree or information is sparse/outdated

### Compact mode (`--compact` — for agent consumption)

Use this mode when called by another agent mid-task, or when the user passes `--compact`. The goal is **maximum information density, minimum formatting overhead**.

Output ONLY:

1. **Answer** — The direct answer in 1-3 paragraphs. No preamble, no headings, no bullet formatting ceremony. Just the facts.

2. **Code/config** — If the answer involves code, config, or commands, include them inline. This is the most actionable part for an agent.

3. **Key URLs** — 2-3 most relevant reference URLs on their own lines at the end. No grouping by source.

**Do NOT include in compact mode:** source comparison, confidence badges, section headers, bullet-point key findings (fold them into the answer paragraph), or "no results" notices.

The compact output should be **under 500 words** unless code samples push it longer. An agent consuming this needs the answer fast and in a form it can act on immediately.

## Important Guidelines

- Keep the synthesized answer focused and scannable. Use short paragraphs and bullet points.
- Do not just concatenate results from each source. Actively deduplicate and merge information.
- If a source returns no useful results, skip it in the synthesis — don't mention it failed.
- Prefer recent information when sources conflict on time-sensitive topics.
- In standard mode, always include at least 3-5 reference URLs so the user can verify claims.
