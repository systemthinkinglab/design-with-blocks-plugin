# Design with Blocks

A free skill for Claude Code that helps you design an application using 7 universal building blocks.

Describe your app in plain English. The skill walks you through a 10-minute conversation, decomposes your features into blocks, recommends technology per block, and outputs a design doc you can paste into Claude Code or Cursor to build.

**Scope: design only.** The skill stops at architecture. It does not write code, review pull requests, or debug running systems.

## The 7 building blocks

Every system, from Instagram to Stripe, is composed of the same seven primitives:

**Task primitives (blue)**
- **Service** — synchronous; caller waits for the answer
- **Worker** — asynchronous; runs after the caller has moved on

**Storage primitives (pink)**
- **Key-Value Store** — fast lookup by one key
- **File Store** — blob storage for images, videos, documents
- **Queue** — decoupled async messaging
- **Relational Database** — structured data with relationships
- **Vector Database** — similarity search via embeddings

**External entities (green)**
- **User** — human or AI agent calling in
- **External Service** — third-party APIs you call out to
- **Time** — the clock as a system input

## Installation

### Option A: Claude Code

```bash
git clone https://github.com/<owner>/design-with-blocks ~/.claude/skills/design-with-blocks
```

Then in Claude Code, type `/design-with-blocks` to invoke.

### Option B: Claude.ai Project

1. Create a new Project at claude.ai.
2. Upload every file in `knowledge/` as Project Knowledge.
3. Paste the contents of `SKILL.md` as the Project's custom instructions.
4. Start a chat and say "design my app."

## Usage

```
/design-with-blocks
```

The skill will ask two intake questions, walk through the external entities that shape your system, elicit your key features, decompose them into blocks with reasoning shown, recommend technology per block, and output a markdown design doc.

Target session length: 10 to 15 minutes.

## Credits

The 7 building blocks framework is the intellectual work of Kay Ashaolu, founder of Systems Thinking Lab. This skill is a free, public expression of the framework's design-pass logic. If you want pattern literacy — the ability to design any future system without a tool like this — that is what [Course I: Universal Building Blocks](https://systemthinkinglab.ai) teaches.

## License

Apache 2.0. Attribution required. See `LICENSE`.

## Contributing

Issues and pull requests welcome. The knowledge files are designed to stay stable; the skill flow in `SKILL.md` is where iteration will happen as real sessions surface better questions and sharper teaching moments.
