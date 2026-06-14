# Research Plugin for Claude Code

Give Claude the ability to search the web using up to 5 search engines at once, then combine what it finds into a single clear answer. Great for getting up-to-date information, comparing sources, and researching topics that go beyond Claude's training data.

**You don't need all 5 sources to get started.** Even one works. You can add more later.

| Source | What it's good at | Free tier | Paid pricing |
|--------|-------------------|-----------|--------------|
| **Brave Search** | General web + news | $5/month credit (~1,000 searches). Credit card required. | $5 per 1,000 requests |
| **Tavily** | AI-optimized search | 1,000 credits/month. No card required. | $0.008/credit, or $30/month for 4,000 credits |
| **Exa** | Academic + niche content | 1,000 requests/month. No card required. | $7 per 1,000 searches |
| **Perplexity** | AI answers with citations | No free tier. Pay-as-you-go only. | ~$5 per 1,000 requests + token costs |
| **Context7** | Programming docs | 1,000 requests/month. No card required. | $10/month for 5,000 requests |

For most people, **Brave + Tavily + Exa** on free tiers gives you 3,000 searches/month at zero cost. That's plenty for daily use.

---

## Setup (15-20 minutes)

There are 4 steps. You only do this once.

### Step 1: Install the plugin

Open Claude Code and paste this message:

> Install the research plugin from this gist: https://gist.github.com/jarekbird/353b8be575ee3057f73621b44b0e9c02
>
> 1. Download all 4 files from the gist
> 2. Save them into a new plugin at ~/.claude/plugins/personal-plugins/research/ with this layout:
>    - `plugin.json` goes in `.claude-plugin/plugin.json`
>    - `.mcp.json` goes in the root
>    - `README.md` goes in the root
>    - `SKILL.md` goes in `skills/research/SKILL.md`
> 3. Register the personal-plugins marketplace if it doesn't exist yet: `/plugin marketplace add personal-plugins --source directory --path ~/.claude/plugins/personal-plugins`
> 4. Install the plugin: `/plugin install research@personal-plugins`

Claude will handle all the downloading and file setup. Just approve the commands when it asks.

### Step 2: Sign up for search APIs and get your keys

Pick at least one source to start with. **Tavily is the best starting point** — it's free, no credit card required, and quick to set up. You can always add others later.

We recommend setting up **Tavily + Exa** first (both free, no card needed), then adding Brave if you want a third source.

#### Tavily (recommended first source — free, no credit card)

1. Go to https://app.tavily.com/sign-in
2. Sign up with Google or email
3. After signing in, you'll see your dashboard. The API key is displayed on the main page — it starts with `tvly-...`
4. Copy the key — you'll need it in Step 3

Free tier: 1,000 credits/month. A basic search costs 1 credit.

#### Exa (free, no credit card)

1. Go to https://dashboard.exa.ai/login
2. Sign up with Google or email
3. After signing in, click **"API Keys"** in the left sidebar
4. Click **"Create new API key"**
5. Copy the key

Free tier: 1,000 requests/month. Great for finding niche and academic content.

#### Brave Search (free, but requires credit card on file)

1. Go to https://brave.com/search/api/
2. Click **"Get Started for Free"**
3. Create an account or sign in
4. You'll need to add a credit card (required for anti-fraud, you won't be charged if you stay within the free credit)
5. Once logged in, you'll land on the dashboard. Your API key is shown on this page — it starts with `BSA...`
6. Copy the key

Free tier: $5/month credit (~1,000 searches). You can cap your plan at the free credit to avoid any charges.

#### Perplexity (paid only — skip if you want free sources only)

1. Go to https://docs.perplexity.ai
2. Click **"Get API Key"** or go to https://www.perplexity.ai/settings/api
3. Sign in and add billing credits (there is no free tier)
4. Copy your API key — it starts with `pplx-...`

Pricing: ~$5 per 1,000 requests plus token costs. Best for getting AI-synthesized answers with citations.

#### Context7 (free, no signup needed)

Nothing to do here. Context7 works automatically as long as you have Node.js installed (which you do if you're running Claude Code). It has a limit of 1,000 requests/month on the free tier, which is plenty for looking up programming docs.

### Step 3: Save your API keys

You need to add your keys to a config file so they're available every time you open your terminal.

**Tell Claude:**

> Add these API keys to my shell profile (~/.zshrc). Replace the placeholder values with my actual keys:
> ```
> export BRAVE_API_KEY="paste-your-brave-key-here"
> export TAVILY_API_KEY="paste-your-tavily-key-here"
> export EXA_API_KEY="paste-your-exa-key-here"
> export PERPLEXITY_API_KEY="paste-your-perplexity-key-here"
> ```
> Only include the lines for keys I actually have.

(If you only signed up for Brave, just include the BRAVE line. Skip the rest.)

### Step 4: Restart and verify

This is important — the keys won't take effect until you restart.

1. **Quit your terminal app completely** (Cmd+Q, not just close the window)
2. **Reopen your terminal**
3. **Start Claude Code** (`claude` in the terminal)
4. **Type:** `/research --setup`

This will show you which sources are ready. You should see "CONFIGURED" next to each key you added.

If something shows "MISSING" that you expected to be there, double-check that you saved the key correctly in Step 3 and fully restarted the terminal.

---

## Usage

Once setup is complete, just ask Claude to research anything:

```
/research what are the best practices for database indexing?
```

### Search specific sources

```
/research --brave --tavily what is the latest Node.js LTS version?
```

### Look up programming docs

```
/research --docs how do I use React Server Components?
```

### Quick answer mode

Less formatting, just the facts:

```
/research --compact how do I configure ESLint flat config?
```

---

## How it works

1. You ask a question
2. Claude searches all your configured sources at the same time (in parallel)
3. It reads through all the results, removes duplicates, and combines the best information
4. You get one clear answer with references you can click to verify

---

## Troubleshooting

**"/research isn't working"**
- Did you restart Claude Code after installing the plugin? You need to fully exit and reopen.

**"Source shows MISSING but I added the key"**
- Did you restart your terminal (Cmd+Q and reopen, not just a new tab)?
- Check that the export line is in your `~/.zshrc` file — ask Claude: "Show me what's in my ~/.zshrc"

**"Only some sources work"**
- That's fine! The plugin works with whatever you have configured. Add more sources anytime by repeating Steps 2-4 for the new source.

**"I want to add another source later"**
- Sign up for the API (Step 2), add the key to your shell profile (Step 3), restart terminal + Claude Code (Step 4). Done.
