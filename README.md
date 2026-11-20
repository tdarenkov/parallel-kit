# parallel-kit

**[Parallel](https://parallel.ai), set up for agents.**

A Claude Code plugin that puts the best of Parallel's web tools in one place, so your sessions and subagents use the right one at the right time without you thinking about it.

> Not affiliated with Parallel Web Systems. This kit is built on their [MCP server](https://docs.parallel.ai/integrations/mcp/quickstart), their [`parallel-cli`](https://docs.parallel.ai/integrations/cli) and their own [agent skills](https://github.com/parallel-web/parallel-agent-skills), and keeps their texts word for word wherever it can.

## Why I built this

Parallel is the best web platform for agents I've used. It has already solved most of what makes agents bad at the web:

| Problem | What Parallel ships |
| --- | --- |
| Search results are links, not answers | `web_search` returns ranked excerpts written to be answered from directly |
| Reading a page means pulling the whole page | `web_fetch` returns the parts that matter, from articles, PDFs and JavaScript-heavy sites |
| A broad question needs a real report | [Deep research](https://github.com/parallel-web/parallel-agent-skills/blob/main/skills/parallel-deep-research/SKILL.md): a cited report, from cents to a few dollars by processor |
| "Find every X that Y" | [FindAll](https://github.com/parallel-web/parallel-agent-skills/blob/main/skills/parallel-findall/SKILL.md): a structured list of matching entities, with evidence |
| A list that needs facts filled in | [Enrichment](https://github.com/parallel-web/parallel-agent-skills/blob/main/skills/parallel-data-enrichment/SKILL.md): web-sourced columns added to your rows |

The problem isn't the tools. It's knowing which one to use, and when.

### #1: It's hard to know what to use

**The Problem**: Parallel's [plugin](https://github.com/parallel-web/parallel-agent-skills) is all or nothing: fifteen skills, an agent and an MCP server. How to use each product lives in its own skill. And Parallel really has two sides:

| | Quick lookups | Deep runs |
| --- | --- | --- |
| What | Search the web, read a page | Deep research, FindAll, enrichment |
| Gives you | Facts, docs, a page's content | A cited report, every X that Y, new columns for your rows |
| Costs | Fractions of a cent | Cents to a few dollars |
| Takes | Seconds | Minutes |
| In this kit, started by | Any session or subagent | Only you, after a brief |

A session left to itself sticks to the first side and forgets the second exists, or reaches for the second when a search would do.

**The Fix**: one router, [`parallel`](./skills/parallel/SKILL.md), that the main session reaches for when a question may need the web. It decides between nothing (it already knows), a lookup, or a paid run, and says what each costs.

### #2: Going deep should be a conversation

**The Problem**: a deep research or FindAll run is only as good as its brief, and it costs real money. An agent that starts one on its own guesses the question, the tier and the output, and you find out afterwards.

**The Fix**: [`brief`](./skills/brief/SKILL.md). When a question needs to go deep, the session writes the brief with you: what you need and why, the exact input Parallel will get, the processor and its price. Nothing runs until you say yes. The run polls in the background, and the result lands in `parallel-results/` in your repo, not in `/tmp`.

**Follow-ups**, as Parallel designed them: a deep research run returns an `interaction_id`, and a follow-up ("drill deeper into X") reuses that run's context, often on a cheaper processor. Enrichment can start from an earlier research run's context, and a FindAll run can be extended when you want more matches. Each follow-up is a new paid run, so it gets its own brief and your yes. A deep research run's file in `parallel-results/` keeps its `interaction_id`, and a FindAll run's file keeps its `findall_id`, so a later session can pick them up there.

### #3: Subagents should search too, but never spend

**The Problem**: the agents doing the work need the web as much as you do. But `parallel-cli` is signed in for the whole machine, so any subagent could start a paid run, and Parallel's spend limits only notify you; they don't stop the run.

**The Fix**: two parts.

- [`lookup`](./skills/lookup/SKILL.md) gives every session and subagent Parallel's search and fetch. It runs in its own agent, [`lookup-agent`](./agents/lookup-agent.md), which has only those two tools, and hands back a short answer with its sources. The pages it read never fill your context.
- A [guard](./hooks/parallel_subagent_guard.py) on every Bash call: a subagent may run `parallel-cli` search, extract and fetch, and nothing that spends. The main session is never blocked.

## How it fits together

```mermaid
flowchart LR
    Q[Question] --> R{parallel}
    R --> A[Answer directly]
    R --> L[lookup: search + fetch]
    R --> B[brief: deep run, after your yes]
```

### A lookup: the same from your session or any subagent

```mermaid
flowchart LR
    C[Your session or a subagent] -->|question| L[lookup]
    L --> A[lookup-agent searches and reads with Parallel]
    A -->|short answer with sources| C
```

### A deep run: only from your session, only when you ask

```mermaid
flowchart LR
    Q[Your session sees a question that needs a deep run] -->|suggests| Y[You type /parallel-kit:brief]
    Y --> B[Brief and price]
    B -->|your yes| P[Parallel runs it]
    P --> R[Result in parallel-results/]
```

A subagent can't start a deep run. If its lookup finds the question needs one, it says so, and your session takes it from there. The guard refuses any paid `parallel-cli` call a subagent tries.

### Going deep, without a paid run

Out of the box, Parallel's `web_search` always runs in `fast` mode with 10 results. The kit connects to Parallel's server with a configuration header, `x-parallel-mcp-config`, that hands two choices to the agent: the search `mode` and `max_results`. So the lookup agent starts cheap (`fast`, 10 results) and moves to `advanced` with up to 20 results only when you say "go deep" or the first results come back thin. It's still a lookup, priced in fractions of a cent, not a paid run.

### What I kept from Parallel, and what I left out

| Parallel's skill | In the kit |
| --- | --- |
| `parallel-deep-research`, `parallel-findall`, `parallel-data-enrichment`, `status`, `result` | Kept word for word, as the references `brief` follows |
| Task API guides and the pricing page | Kept word for word, minus the docs site's navigation note at the top of each page |
| `parallel-web-search`, `parallel-web-extract` | Replaced by `lookup`, on Parallel's own MCP tools |
| `parallel-subagent` | Replaced by `lookup-agent`: MCP tools only, no Bash |
| `parallel-cli-setup` | Replaced by `setup` |
| `parallel-monitor`, `parallel-memory`, `parallel-mcp-setup`, `parallel-search-setup`, `parallel-search-evaluation`, `parallel-api`, `migrate-to-parallel` | Left out: for building on Parallel, not for using it in a session |

## Installation

You need Claude Code v2.1.299 or later, a [Parallel account](https://platform.parallel.ai), and `python3`.

### 1. Get the plugin

```bash
claude plugin marketplace add tdarenkov/claude-plugins
claude plugin install parallel-kit@tdarenkov
```

### 2. Run `/parallel-kit:setup`

In a Claude Code session, once per machine. It will:

- Remove any other Parallel server that would hide the plugin's
- Install and sign in `parallel-cli`, if needed
- Send you to `/mcp` to sign in to Parallel
- Offer to fix your named agents, so they can use the lookup (below)
- Run one real lookup to show it works

Run it again any time; it redoes only what failed.

**Why named agents need fixing:** a skill that runs in its own agent only gets the tools its caller has. A subagent with a fixed `tools:` list can use `lookup` only if that list includes `Skill` and Parallel's two tools, so setup offers to add them.

### 3. That's it.

## Updating

```bash
claude plugin update parallel-kit@tdarenkov
```

Then `/reload-plugins`, or start a new session. Updates are not automatic.

## Reference

**User-invoked**

- **[setup](./skills/setup/SKILL.md)**: set up the plugin on this machine, or check it again.
- **[brief](./skills/brief/SKILL.md)**: write, price and run a deep research, FindAll or enrichment run, after your yes.

**Model-invoked**

- **[parallel](./skills/parallel/SKILL.md)**: the router: nothing, a lookup or a paid run, and what each costs. You can also type it.
- **[lookup](./skills/lookup/SKILL.md)**: every web search and page read, in its own agent, back as a short cited answer.

Issues are welcome. Changes: [CHANGELOG.md](CHANGELOG.md). Security problems: [SECURITY.md](SECURITY.md). License: [MIT](LICENSE).
