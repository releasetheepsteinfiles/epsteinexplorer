# Launch Plan — Epstein Files Toolchain

Go-to-market for the four tools, now that they share one visual language
(["Declassified"](brand/DESIGN.md)) and a promo asset set.

| Repo | What it is | Ship state |
|---|---|---|
| [`epsteinexposed`](https://github.com/guilyx/epsteinexposed) | Python client | On PyPI, v0.2.0 |
| [`epsteinexposed-mcp`](https://github.com/guilyx/epsteinexposed-mcp) | MCP server, structured search | Working |
| [`epstein-files-rag-mcp`](https://github.com/guilyx/epstein-files-rag-mcp) | MCP server, semantic search | **In development** |
| [`epsteinexplorer`](https://github.com/guilyx/epsteinexplorer) | Chat app | Working |

---

## 1. Positioning — read this before writing any post

The single biggest risk to this launch is **being read as a conspiracy
project instead of a research tool.** That reading gets you removed from the
subreddits that would actually value the work, and it attaches to the
author's name permanently.

Three rules follow, and they are not optional:

**Lead with the engineering, not the topic.** The interesting thing to
r/Python is a clean sync+async client with typed models. The interesting
thing to r/LocalLLaMA is an MCP server with five well-scoped tools. The
Epstein corpus is the *dataset*, not the *pitch*. A post titled "I built a
Python client for a public-records API, with full async support" survives
moderation everywhere. "The TRUTH about the Epstein files" does not.

**Never imply guilt about anyone.** Every repo already carries the
disclaimer; keep it in the post body too, not just the README. Do not name
individuals in titles, screenshots, promo videos, or replies. The promo
videos deliberately name no one — do not undo that in the copy.

**Stay factual about what ships.** `epstein-files-rag-mcp` has no runnable
code. Announcing four tools when three work is the fastest way to lose the
credibility the rest of the launch depends on. It is listed as roadmap
everywhere, including its own promo video.

### The one-line pitch

> Open-source tooling for querying publicly released Epstein case records —
> a Python client, two MCP servers, and a chat interface. Everything cites
> its source.

---

## 2. Pre-launch checklist

Do not post until all of these are true.

- [ ] All four repos on the shared design system (this PR series).
- [ ] Docs sites deployed and reachable:
      `epsteinexposed` (Vercel), `epsteinexposed-mcp` (VitePress),
      `epsteinexplorer` (Vite), `epstein-files-rag-mcp` (static).
- [ ] `epsteinexplorer` has a **live public demo URL**. This is the single
      highest-leverage item on the list — a chat app nobody can try converts
      far worse than one they can. If it cannot be hosted, lead the launch
      with the MCP server instead.
- [ ] Rate limiting / abuse protection on the public demo before it is
      linked anywhere.
- [ ] `epsteinexposed-mcp` published to PyPI so `pip install` in the video
      is true.
- [ ] READMEs embed the poster image + link the promo video.
- [ ] Disclaimer visible in every README above the fold. ✅ (already true)
- [ ] LICENSE present in all four. ✅ (added to the RAG repo this series)
- [ ] Submitted to MCP directories (see §5).

---

## 3. Sequencing

**Do not launch all four at once.** One artifact per wave, each with its own
video, spaced so each has a clean shot at a front page. Four simultaneous
posts read as spam and cannibalise each other.

| Wave | When | Artifact | Primary channel |
|---|---|---|---|
| 1 | Day 0 (Tue) | `epsteinexposed` — the client | r/Python, PyPI |
| 2 | Day 4 (Sat) | `epsteinexposed-mcp` — MCP server | r/mcp, r/ClaudeAI, r/LocalLLaMA |
| 3 | Day 9 (Thu) | `epsteinexplorer` — the app | Show HN, r/OSINT |
| 4 | Day 16 | `epstein-files-rag-mcp` — when it actually ships | r/LocalLLaMA |

Twitter carries all four waves; it is the connective tissue that presents the
toolchain as one thing rather than four scattered repos.

**The overview clip (`suite-*`) is what does that connecting**, and it is not
a wave of its own — shipping it as a standalone "here are four repos" post
before anything has landed asks people to care about a project they have no
reason to trust yet. Instead it closes each thread, sits in the pinned tweet
from Day 0 onward, and heads every README. By Wave 3 a meaningful share of
readers will have seen it two or three times, which is the point: repetition
is what turns four announcements into one recognisable project.

**Best posting times** (both platforms skew US): Tue–Thu, 13:00–15:00 UTC.
Reddit weekend traffic is lower but so is competition — Wave 2 on Saturday
is deliberate.

---

## 4. Twitter/X

Post the **1:1 crop** — it occupies more vertical space in-feed than 16:9
and autoplays silently, which is what the videos are built for.

### Wave 1 — launch thread

> **1/**
> I've been building open-source tooling for the publicly released Epstein
> case records.
>
> First piece: `epsteinexposed`, a Python client for the public API.
> Persons, documents, flight logs, emails. Sync and async.
>
> `pip install epsteinexposed`
> [attach: exposed-1x1.mp4]

> **2/**
> Typed models throughout, so results are objects rather than dict soup:
> ```python
> flights = client.search_flights(year=1997)
> docs = client.search_documents(q="little st james")
> ```
> Full async client too, same surface.

> **3/**
> All data comes from publicly released government records, court filings
> and verified reporting, via epsteinexposed.com.
>
> Inclusion in these records does not imply guilt or wrongdoing. The tools
> are for reading primary sources, not drawing conclusions.

> **4/**
> Three more pieces coming: an MCP server so agents can query the records,
> a semantic-search server, and a chat interface over the whole thing.
>
> MIT licensed. github.com/guilyx/epsteinexposed
> [attach: suite-1x1.mp4]

Put the disclaimer in tweet 3, not the last tweet — most readers never reach
the end of a thread, and it needs to be seen.

### Pin this

Once Wave 1 is out, pin a standalone tweet carrying the **overview clip**, so
anyone landing on the profile sees the whole project rather than whichever
wave happened to be last:

> Open-source tooling for querying publicly released Epstein case records.
>
> A Python client, two MCP servers, and a chat interface. Everything cites
> its source. MIT licensed.
>
> github.com/guilyx
> [attach: suite-1x1.mp4]

Update the pin as tools ship; the clip itself already marks the RAG server
as planned, so it stays accurate until that changes.

### Wave 2 — MCP server

> Your agent can now query the Epstein case records directly.
>
> `epsteinexposed-mcp` is an MCP server exposing five tools — persons,
> documents, flights, emails, cross-search — to Claude Desktop, Cursor, or
> anything else that speaks MCP.
>
> One line of config:
> [attach: mcp-1x1.mp4]

### Wave 3 — the app

> Ask the Epstein files a question in plain English.
>
> EpsteinExplorer is a chat interface over the released records. Every
> answer links back to the document it came from.
>
> Live: [demo URL] · Source: github.com/guilyx/epsteinexplorer
> [attach: explorer-1x1.mp4]

### Twitter notes

- No hashtags. They read as spam and this subject already attracts the
  wrong crowd.
- **Do not tag journalists or public figures.** It looks like you are
  soliciting attention for allegations rather than shipping software.
- Expect conspiracy replies. Do not engage the topic. One canned reply,
  used consistently: *"This is a tool for reading public records — I'm not
  making any claim about anyone in them."* Then stop.
- Reply to your own thread with the repo link ~2h later for a second
  impression.

---

## 5. Reddit

Reddit is where this converts and where it can go badly wrong. **Read each
sub's rules before posting** — several require flair, and most ban
link-only self-promotion.

### Target subs

| Sub | Wave | Framing | Notes |
|---|---|---|---|
| r/Python | 1 | Client library, typed models, async | Requires substance in the body, not a bare link. Use the **Showcase** flair. |
| r/opensource | 1 | MIT-licensed public-records tooling | Low risk, low ceiling. |
| r/mcp | 2 | MCP server, five tools | Small but exactly on-target. |
| r/ClaudeAI | 2 | Claude Desktop config, what it unlocks | Show the `mcp.json` snippet. |
| r/LocalLLaMA | 2, 4 | Agent tooling over a real corpus | Sharp, technical audience. Expect scrutiny of the retrieval design — that's good. |
| r/OSINT | 3 | Research instrument over primary sources | Best fit for the app. Lead with sourcing and citations. |
| r/datasets | 3 | Programmatic access to a released corpus | Mention API attribution. |
| r/programming | 3 | Only with a genuine writeup | Hostile to thin self-promo. Skip unless you write the engineering post in §7. |

### Do not post to

r/conspiracy, r/Epstein and adjacent communities. Not a moral point — a
strategic one. It reframes the project, poisons the Google results for your
name, and brings an audience that will not read the disclaimer.

### Reddit post template (r/Python, Wave 1)

> **Title:** epsteinexposed — a typed Python client (sync + async) for a
> public-records API
>
> I built a Python client for the Epstein Exposed public API, which serves
> publicly released government records — court filings, flight logs,
> documents and emails.
>
> **What it does**
> - Sync and async clients with identical surfaces
> - Typed Pydantic models, so results are objects not dicts
> - Search across persons, documents, flights, emails, plus cross-type search
> - Handles the upstream Cloudflare quirks via curl_cffi
>
> ```python
> from epsteinexposed import EpsteinExposed
>
> with EpsteinExposed() as client:
>     flights = client.search_flights(year=1997)
>     docs = client.search_documents(q="little st james")
> ```
>
> `pip install epsteinexposed` · MIT · [repo] · [docs]
>
> Built this because the data is public but awkward to query
> programmatically. There's an MCP server and a chat interface on top of it
> coming shortly.
>
> *Disclaimer: all data comes from publicly released government records and
> court filings. Inclusion in this database does not imply guilt or
> wrongdoing on anyone's part.*

Answer every technical comment in the first two hours. Early engagement
drives the ranking far more than the post body does.

---

## 6. Other channels

**Hacker News** — Wave 3, as `Show HN: EpsteinExplorer – chat interface over
released Epstein case records`. Submit Tue–Thu ~14:00 UTC. Post a first
comment explaining the architecture and the sourcing, and link the
**overview clip** there — HN readers who like the app immediately want to
know what else is in the stack. HN will interrogate provenance and
neutrality harder than anywhere else; the disclaimer and citation design are
the strongest cards, so lead with them.

**MCP directories** — free distribution, do all of them:
`modelcontextprotocol/servers` (community list PR), Smithery, mcp.so,
Glama, Cursor's directory, PulseMCP.

**PyPI** — the README is the landing page for `pip` users. Make sure the
poster image renders there (absolute raw.githubusercontent URLs, not
relative paths).

**Lobste.rs** — only if you have an invite; `show` tag.

---

## 7. The multiplier: write the engineering post

The single highest-return thing not yet built. A writeup — *"Building an MCP
server over a public-records API"* — unlocks r/programming and HN on
substance rather than novelty, and it ages into ongoing search traffic.

Angle candidates, best first:
1. **Structured vs. semantic search over the same corpus** — why two MCP
   servers, and how you decide which a question needs. This is a genuinely
   useful post for anyone building retrieval tooling, and it's the honest
   explanation for the RAG server's existence.
2. Designing MCP tool surfaces that agents actually call correctly.
3. Citation-preserving RAG: never return a passage you cannot attribute.

---

## 8. Assets

Rendered by `promo/render.mjs`, output in `promo/out/`. **Five clips**, each
in 16:9 and 1:1 with a poster still:

| Prefix | Presents | Where it earns its place |
|---|---|---|
| `suite-*` | **Toolchain overview** — all four tools | Pinned tweet, HN first comment, repo READMEs, anywhere someone asks "what is this project?" |
| `exposed-*` | Python client | Wave 1 |
| `mcp-*` | MCP server, structured search | Wave 2 |
| `rag-*` | MCP server, semantic search | Wave 4 |
| `explorer-*` | Chat app | Wave 3 |

| Format | Use |
|---|---|
| `-16x9.mp4` | YouTube, docs sites, embeds, HN |
| `-1x1.mp4` | Twitter, Reddit — **the default for social** |
| `-poster.png` | README embeds, link previews, PyPI |

All are silent with burned-in text, 19.6s. Autoplay on both platforms is
muted, so nothing depends on audio.

**The overview clip is the one that does the most work.** Each wave sells one
tool; `suite-*` is what makes the four read as a project rather than four
scattered repos, and it is the right attachment any time the audience is
meeting the work for the first time. Use it in the pinned tweet, the last
tweet of each thread, and the READMEs — not as a replacement for the
tool-specific clip in a wave announcement.

To re-render after a copy change: `cd promo && npm install && npm run render`.

---

## 9. Measuring it

Track weekly for six weeks:

- PyPI downloads (`pypistats recent epsteinexposed`) — the least gameable
  signal that anyone actually adopted it.
- GitHub stars/forks per repo, tagged by wave, to see which framing landed.
- Referrer traffic in GitHub Insights → Traffic.
- Demo sessions, if the Explorer demo is hosted.

The realistic goal for a launch like this is **a few hundred stars and a
handful of real users** who file issues. Treat the engineering post in §7 as
the thing that compounds; the launch is just the introduction.

---

## 10. If it goes wrong

**Post gets removed** — almost always a self-promo or flair rule. Message
the mods, ask which rule, fix and resubmit once. Never resubmit blind.

**Conspiracy pile-on in the replies** — use the canned reply once, then
disengage. Do not argue the subject matter. Do not delete the thread; that
reads as concealment.

**Someone claims the tool defames a named person** — point at the
disclaimer, confirm the tool only surfaces publicly released records with
attribution, and correct anything genuinely inaccurate immediately. This is
exactly why no promo asset names anyone.

**Upstream API changes or rate-limits you** — the client is the dependency
for everything else. Pin behaviour in integration tests (the repo already
has a live-API CI job) and be ready to say so publicly if the demo breaks.
