# Agents

A four-agent content-production team plus three additional team templates,
set up per the scheme suggested by khairallah.

Every agent is built from four pieces:

- **Role** — one specific job, narrowly scoped
- **Instructions** — process, quality standard, output format
- **Tools** — what the agent can access (filesystem, web, connectors)
- **Memory** — `context.md` plus prior outputs in the output folders

## The four core agents

| # | Agent | System prompt | Reads from | Writes to |
|---|-------|---------------|------------|-----------|
| 1 | Research | `01-research-agent.md` | topic prompt | `Research/` |
| 2 | Outline | `02-outline-agent.md` | `Research/` | `Outlines/` |
| 3 | Writer | `03-writer-agent.md` | `Outlines/` | `Drafts/` |
| 4 | Editor | `04-editor-agent.md` | `Drafts/` | `Published/` |

Each agent's output is the next agent's input. The handoffs are the only
glue you need.

## Running the team

### Manual handoff (one agent at a time)

1. Open Claude Desktop → Cowork (or any agent runtime).
2. Start a new session, paste the contents of `01-research-agent.md` as the
   system prompt, give the agent access to this repo, then ask:
   *"Research [topic]."*
3. When the brief lands in `Research/`, start a new session with
   `02-outline-agent.md` and ask: *"Create an outline from
   `Research/<file>.md`."*
4. Repeat for Writer and Editor.

### Chained workflow (end-to-end)

In Cowork, after loading all four agent prompts, run:

> Take the topic "<your topic>", run the full pipeline:
> research → outline → write → edit. Save all intermediate files.
> Deliver the final article to `/Published`.

### Scheduled workflow

Use `/schedule` in Cowork to fire the Research Agent on a recurring
cadence (e.g., Monday 7am) and have it drop briefs into `Research/`
automatically.

## Shared context

`context.md` defines audience, tone, banned phrases, and formatting
defaults. Every agent's instructions tell it to read `context.md` before
starting work — that is how consistency holds across the team.

Edit `context.md` to retune voice and standards in one place rather than
re-editing four prompts.

## Feedback loops

After each major output, append a short note to the bottom of the relevant
agent's `*.md` file under a `## Standing feedback` heading. The agent
reads its own prompt at the start of every session, so corrections
compound instead of evaporating.

## Other team templates

`templates/` contains three additional team configurations you can adapt:

- `business-intelligence-team.md` — collection → analysis → report → recommendation
- `customer-research-team.md` — survey → processing → patterns → insight
- `social-media-team.md` — trend → planning → writing → optimization
