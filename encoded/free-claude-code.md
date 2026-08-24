# Encoded repository — `Alishahryar1/free-claude-code`

> A plain-text, greppable encoding of an external GitHub repository, captured
> for reference. This is **not** part of the EXSTO ERGO SUM manuscript; it lives
> under `encoded/` to keep it isolated from the submission deliverables, in the
> same spirit as the `derived/*.txt` mirrors (a readable capture of an
> out-of-repo source).
>
> - **Source:** https://github.com/Alishahryar1/free-claude-code
> - **Captured:** 2026-08-24
> - **Method:** public web/README/ARCHITECTURE fetch (the repo's `.tex`-style
>   sources are not vendored here; this is a summary encoding, not a byte mirror).
> - **Fidelity note:** quoted strings are the project's own wording; structural
>   descriptions are paraphrased from its `README.md` and `ARCHITECTURE.md`.

## Identity

| Field | Value |
|---|---|
| Full name | `Alishahryar1/free-claude-code` |
| Description | "Use Claude Code, Codex, Pi, and OpenCode for free (1.3B+ free tokens) from your terminal, app, IDE, or phone" |
| Primary language | Python |
| License | MIT |
| Default branch | `main` |
| Stars / forks (at capture) | ~48.6k / ~8.0k |

Trademark note carried by the project: "Claude and Claude Code are trademarks of
Anthropic"; the project is independent of Anthropic's official offerings.

## What it is

**Free Claude Code (FCC)** is an independent, open-source **local proxy for
agent clients**. It accepts requests from multiple coding tools — Claude Code,
Codex, Pi, OpenCode, Cline, and others (nine agents in total) — and routes them
to configured upstream model providers while preserving each client's wire
protocol. It advertises access to "50 ToS-friendly providers" and "1.3B+ free
tokens every month" from a single searchable UI spanning free, paid,
subscription, and local models.

### Headline features

- **Provider fallback** — automatically switches to an alternate model when a
  provider fails *before any output is committed*.
- **Token optimization** — reduces terminal-output tokens by up to ~90% via
  filtering plus five built-in optimizations (RTK filtering is optional).
- **Multi-surface access** — terminal, VS Code, JetBrains IDEs, Discord,
  Telegram; native desktop launchers on Windows and macOS.
- **Voice input** — local Whisper or NVIDIA NIM transcription.
- **Model-tier routing** — independent configuration per Claude tier
  (Fable / Opus / Sonnet / Haiku); reasoning-level controls on compatible models.
- **Admin UI** — configure API keys and select models from a searchable dropdown;
  50+ providers from NVIDIA NIM and OpenRouter to local Ollama / LM Studio.

## Top-level layout

```
.github/            # CI / repo automation
.env.example        # sample environment configuration
.gitignore
.python-version
AGENTS.md           # agent integration notes
ARCHITECTURE.md     # system design (summarized below)
CLAUDE.md           # Claude Code project guidance
CONTRIBUTING.md
LICENSE             # MIT
README.md
assets/
e2e/                # end-to-end tests
pyproject.toml      # packaging / deps (uv)
scripts/
smoke/              # smoke tests
src/                # source root
tests/
uv.lock
src/
  free_claude_code/ # the package
```

## Architecture

Purpose: "a local proxy for agent clients" that ingests messages from many
coding tools and routes them to upstream providers while maintaining wire
protocol compatibility.

### Runtime layers (packages under `src/free_claude_code/`)

| Package | Responsibility |
|---|---|
| `api/` | FastAPI HTTP adapter — routes, product handlers, protocol conversion |
| `application/` | Core routing, model resolution, provider execution |
| `providers/` | Provider implementations and upstream communication |
| `core/` | Protocol-neutral logic (Anthropic ↔ OpenAI Responses conversion) |
| `config/` | Settings, provider metadata, filesystem paths, `admin/` UI |
| `cli/` | Console entrypoints and client launchers |
| `messaging/` | Optional Discord / Telegram adapters |
| `runtime/` | Process composition and lifecycle management |

### Request flow

1. **Ingress** — HTTP request hits a FastAPI route with authentication.
2. **Routing** — `ModelRouter` resolves the client's model name to a provider
   target via tier-based mapping (fable / opus / sonnet / haiku).
3. **Execution** — `ProviderExecutor` runs `preflight_stream()` validation,
   acquires a provider generation lease, then streams to the upstream.
4. **Fallback** — if the primary provider fails *before output*, the executor
   advances to the next model in `MODEL_FALLBACKS`.
5. **Egress** — response is converted to the target protocol (Anthropic SSE or
   OpenAI Responses) before returning to the client.

### Provider model

- `ProviderRuntimeManager` constructs and publishes provider "generations" at
  startup and after Admin config changes; owns admission control, retry
  budgeting, recovery episodes, and model-catalog discovery; issues request
  leases bound to response streaming.
- Each provider implements two operations: synchronous `preflight_stream()`
  validation and lazy `stream_response()` execution.
- Most providers use declarative `OpenAIChatProfile` config; specialized adapters
  handle quirks (e.g. Groq reasoning vocabularies, Vertex credentials).
- `ResolvedModelRoute` owns the public model, one canonical primary
  `ProviderModelTarget`, and the ordered canonical fallback targets.

### Admin UI & config

- Lives under `config/admin/`; Admin routes verify loopback access and apply
  sparse updates to a managed `~/.fcc/.env` file.
- Config changes trigger provider replacement: `ProviderRuntimeManager` retires
  old generations and drains existing leases before publishing new ones.

### Design principles

- **Ownership boundaries** — each package owns its concern; cross-package
  dependencies follow explicit allowlists.
- **Credential safety** — diagnostics redact secrets; the proxy auth token is
  kept separate from provider keys.
- **Failure handling** — a canonical `ExecutionFailure` with semantic "kind"
  classification maps errors consistently across protocols.
- **Streaming contracts** — commit boundaries separate early preflight failures
  (non-2xx JSON) from mid-stream failures (terminal protocol events).

## Install & integration (as documented upstream)

- One-command install scripts for macOS/Linux and a Windows PowerShell script.
- Configure keys and pick models through the Admin UI.
- **VS Code** — set a custom base URL and auth token via environment variables.
- **Discord / Telegram** — bot setup with commands such as `/stats`, `/stop`,
  `/clear`.
- **Desktop** — native launcher shortcuts on Windows and macOS.

## Provenance

Encoded on 2026-08-24 from the repository's public `README.md`,
`ARCHITECTURE.md`, and GitHub file listing. Figures (stars, forks) are
point-in-time. For authoritative, current detail always consult the source
repository.
