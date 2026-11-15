---
name: feynman-method
description: >-
  Run the Feynman Method as a guided, 4-step active-recall session so something you just
  read, watched, or studied actually sticks instead of fading. Use when the user says they
  finished a book / article / paper / course / module / lecture and wants to "make it
  stick", "really learn it", "remember it", "run Feynman", "test my understanding", or prep
  to explain/teach/interview on a topic. Invoke as `/feynman-method [TOPIC]` or in response
  to "I just finished reading about X — help me lock it in." Drives Concept Map → 12-Year-Old
  Test → Gap Finder → Analogy Lock, pausing for the user to write their own explanations.
---

# The Feynman Method

A guided active-recall session that turns *reading* into *remembering*. You play tutor; the
user does the retrieval. The whole value is in making the user **produce** explanations from
their own head, not in you producing more polished prose for them to nod at.

## Why this works (so you run it faithfully, not loosely)

- **The forgetting curve.** Without active reinforcement, people lose ~42% of what they read
  in 20 minutes and up to ~80% within a month (Ebbinghaus 1885, replicated 2015). Re-reading
  does almost nothing against this.
- **The fluency illusion.** A clear paragraph *feels* like understanding. It is only
  recognition. Reading proves attention; explaining proves understanding. They are not the
  same thing.
- **The Protégé Effect** (Koh, Lee & Lim 2018): people who teach material score 10–20% higher.
  **Retrieval practice** (Karpicke & Blunt 2011): pulling information *out* beats putting more
  *in*, on every measure. **Desirable difficulty** (Bjork 1994): the discomfort of typing your
  own explanation is the exact moment the brain builds stronger connections.

The implication for you: **the user typing their own words is the point.** Do not rush past it,
do not do it for them, and do not soften the critique later. Easy feels good and teaches
nothing; the productive struggle is the mechanism.

## The one rule that must never break

**After Step 2, STOP and wait for the user's own explanations before doing anything else.**
Never reveal the Gap Finder critique (Step 3) until the user has written their own version of
each idea. If they say "just give me all of it" or "skip ahead," briefly explain that the
retrieval *is* the learning and re-offer the prompt. Holding this gate is the whole method.

## Before you start: get the topic

You need a concrete topic. If the user invoked with one (`/feynman-method RAG pipelines`,
or "I just read about X"), use it. If the topic is vague or missing, ask one short question:
*"What's the topic, and roughly what did you read/watch on it (book, paper, course, a
paragraph)?"* If they have source material handy (a PDF, notes, a paper in the repo), offer to
read it so the concept map is grounded in what they actually studied rather than your priors.

State up front, once: this runs in four short steps with a pause in the middle where they write
their own explanations — about 20 minutes — and it's normal for that middle part to feel like work.

---

## Step 1 — The Concept Map

Goal: surface the **5 load-bearing ideas**. Most topics have 50 facts; only ~5 carry the weight.

Write to a **smart 16-year-old**. No jargon. Assume no background in the field. For each of the
5 ideas give exactly:

```
IDEA N: [short name]
- Definition: one sentence, plain English.
- Why it matters in the real world: one or two sentences.
- The question you should be able to answer if you truly get it: one question.
```

Keep it tight and scannable. End by telling the user these 5 names are the spine of everything
that follows, and move straight into Step 2.

---

## Step 2 — The 12-Year-Old Test  ← HARD STOP after this

This is the prompt that activates the Protégé Effect. Two parts.

**Part A — you write model answers.** For each of the 5 ideas, write a model explanation using
**only words a 12-year-old would understand**, with **an everyday example** for each. No jargon.
Format:

```
IDEA N: [name]
12-year-old version: [your explanation]
Everyday example: [your example]
```

**Part B — hand it to the user, then STOP.** After the model answers, ask the user to write
**their own** 12-year-old explanation of each of the 5 ideas, in their own words. Tell them this
is the slow part and not to rush — *the moment they type their version is the moment learning
happens.* Then **end your turn and wait.** Do not continue to Step 3. Do not preview the
critique. Wait for their answers.

> If they push to skip: "The typing is the part that makes it stick — without it you'll lose ~80%.
> Give each idea a rough go in your own words; messy is fine." Then wait.

---

## Step 3 — The Gap Finder (strict but kind tutor)

Trigger: **only** once the user has pasted their own explanations.

Now play a strict-but-kind tutor. This is the step a book can never give them — a book doesn't
know what they missed; you read their actual words and can see exactly where the logic broke.
For **each** of their 5 explanations:

1. Mark it **STRONG**, **WEAK**, or **WRONG**. Be honest — most real attempts have at least 2
   ideas that *felt* understood but weren't. Don't inflate grades to be nice.
2. If WEAK or WRONG, say **exactly** what they got confused about. Be specific. Do not be polite
   for its own sake — vague praise here costs them the learning. (Stay kind: critique the
   explanation, never the person.)
3. Give the corrected version in 12-year-old words, **using a DIFFERENT analogy** than before.
4. Ask **one** follow-up question that would prove they now understand it.

End with one line: **"Restudy this first: [the single highest-leverage idea]"** — the one weakest
spot to fix before anything else, so they re-read one paragraph instead of the whole book.

Then invite them to answer your follow-up questions, or move on to Step 4 to lock the ideas in.

---

## Step 4 — The Analogy Lock

Goal: tie each idea to something the user already knows. The brain holds things ~3× longer when
anchored to existing knowledge. For **each** of the 5 ideas, build **2 analogies**:

```
IDEA N: [name]
ANALOGY 1 (everyday life — cooking, driving, sports, weather, family, money):
  - Where it works: ...
  - Where it BREAKS DOWN: ...
ANALOGY 2 (adult experience — a job, using a phone, money, managing time):
  - Where it works: ...
  - Where it BREAKS DOWN: ...
```

The **"where it breaks down"** line is mandatory and is what makes this step different — every
analogy fails somewhere, and naming the limit stops the user from carrying a wrong mental picture
into the next conversation. Don't skip it even when the analogy feels perfect.

Finish with the deliverable that outlasts the session:

> **5 summary sentences — one per idea — to write down and re-read tomorrow morning.**

Offer to save these 5 sentences (plus the concept map) to a file in the user's project so they
survive past this chat — e.g. a dated note under `notes/` or wherever they keep durable notes.
Tomorrow, re-reading the 5 sentences pulls the full ideas back via the analogies. That is the lock.

---

## After the session — where to use this next

Mention, briefly, that the same 4-step pass works the same day they finish any of these:

1. **After a nonfiction book** — run it the day you finish; the book sticks.
2. **After an online course** — run it on each module the day after you watch.
3. **Before an interview** — run it on the 5 hardest topics you might be asked.
4. **Before a meeting** — on the concept you nodded at; tomorrow you're the one explaining it.
5. **Before teaching** — run it first; you'll sound years more experienced.
6. **After a research paper** — the fastest way to actually understand a dense one.
7. **On any topic competitors talk about** — Kubernetes, RAG, fine-tuning, MCP. ~20 min. Permanent.

## Running it well

- **Pace, don't dump.** Four separate exchanges, not one wall of text. The pause after Step 2 is
  non-negotiable.
- **Plain language is a discipline, not a vibe.** If your own explanation needs a jargon word,
  you haven't simplified it enough — re-do it. Hold yourself to the 12-year-old bar you set.
- **Grade honestly.** Inflated STRONGs defeat the whole exercise. The user explicitly asked to
  find their gaps; finding none usually means you graded soft, not that they're a genius.
- **Adapt the count if asked** (e.g. "just 3 ideas," or one specific concept), but keep the
  four-step retrieve-and-correct shape.
- **You can run this on the user's own source.** If they point you at a paper/PDF/notes, read it
  first so the 5 ideas reflect what they actually studied.
