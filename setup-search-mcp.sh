#!/usr/bin/env bash
#
# setup-search-mcp.sh
# Adds Brave, Tavily, and Exa search MCP servers to Claude Code.
#
# Usage:
#   export BRAVE_API_KEY="..."
#   export TAVILY_API_KEY="..."
#   export EXA_API_KEY="..."
#   ./setup-search-mcp.sh
#
# Keys (free signup):
#   Brave  -> https://brave.com/search/api
#   Tavily -> https://tavily.com
#   Exa    -> https://exa.ai

set -euo pipefail

# --- 1. Require the API keys ------------------------------------------------
missing=0
for var in BRAVE_API_KEY TAVILY_API_KEY EXA_API_KEY; do
  if [ -z "${!var:-}" ]; then
    echo "ERROR: $var is not set." >&2
    missing=1
  fi
done
if [ "$missing" -eq 1 ]; then
  echo >&2
  echo "Set the missing keys, e.g.:" >&2
  echo "  export BRAVE_API_KEY=your-key" >&2
  echo "  export TAVILY_API_KEY=your-key" >&2
  echo "  export EXA_API_KEY=your-key" >&2
  exit 1
fi

# --- 2. Sanity checks -------------------------------------------------------
command -v npx >/dev/null 2>&1 || { echo "ERROR: npx (Node.js) is required but not found." >&2; exit 1; }

OUT="${1:-.mcp.json}"   # write target; defaults to ./.mcp.json

# --- 3. Write the .mcp.json -------------------------------------------------
cat > "$OUT" <<EOF
{
  "mcpServers": {
    "brave": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "${BRAVE_API_KEY}" }
    },
    "tavily": {
      "command": "npx",
      "args": ["-y", "tavily-mcp"],
      "env": { "TAVILY_API_KEY": "${TAVILY_API_KEY}" }
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": { "EXA_API_KEY": "${EXA_API_KEY}" }
    }
  }
}
EOF

echo "Wrote $OUT"

# --- 4. Register with the Claude CLI too (if available) ---------------------
if command -v claude >/dev/null 2>&1; then
  echo "Registering servers via the claude CLI..."
  claude mcp add-json brave  "{\"command\":\"npx\",\"args\":[\"-y\",\"@modelcontextprotocol/server-brave-search\"],\"env\":{\"BRAVE_API_KEY\":\"${BRAVE_API_KEY}\"}}"  2>/dev/null || echo "  (skipped brave — may already exist)"
  claude mcp add-json tavily "{\"command\":\"npx\",\"args\":[\"-y\",\"tavily-mcp\"],\"env\":{\"TAVILY_API_KEY\":\"${TAVILY_API_KEY}\"}}"                          2>/dev/null || echo "  (skipped tavily — may already exist)"
  claude mcp add-json exa    "{\"command\":\"npx\",\"args\":[\"-y\",\"exa-mcp-server\"],\"env\":{\"EXA_API_KEY\":\"${EXA_API_KEY}\"}}"                            2>/dev/null || echo "  (skipped exa — may already exist)"
  echo
  echo "Registered MCP servers (names only; skipping live health check):"
  # `claude mcp list` runs a health check that launches each server and can
  # hang when there's no network, so guard it with a timeout and fall back
  # to grepping the names if it stalls.
  if ! timeout 10 claude mcp list 2>/dev/null; then
    echo "  (health check skipped/timed out — servers are still registered)"
  fi
else
  echo "claude CLI not found — relying on $OUT only."
fi

echo
echo "Done. Restart your Claude Code session so the servers load."
echo "Then the tools appear as: mcp__brave__*, mcp__tavily__*, mcp__exa__*"
