# Traceformer

A collection of geometric tools for transformer interpretation. Examples are currently only built on GPT-2, but the infrastructure should generalize.

## Why this exists

This was inspired by reading Anthropic's
["When Models Manipulate Manifolds"](https://transformer-circuits.pub/2025/linebreaks/index.html)
paper, which found that Claude 3.5 Haiku tracks its position in a line of
fixed-width text as a curved, low-dimensional manifold in the residual
stream, and manipulates that manifold's curvature and rotation to decide
when to insert a newline. The idea that knowledge can be encoded as geometry
within a transformer model seemed elegant in a way I couldn't let go of. So
now I'm building a library as I try to understand how far I can take this idea.

## Near-term goal

Use GPT-2 as the test bed for building intuition about how these models
represent capability geometrically. GPT-2 is small enough to run on my laptop
locally, so I can quickly test ideas, even if my initial algorithms aren't
efficient. These ideas will mostly live in `studies/` as demo files that show
the motivation and examples of usage. As I better understand GPT-2, I expect
to develop ideas for new approaches to interpret transformers, which will go
in the `traceformer` package to be used elsewhere.

## Long-term goal

I intend for `traceformer`, the library at the root of this repo, to outgrow
GPT-2. As patterns solidify out of the studies into reusable infrastructure,
they move into `traceformer`, where the ultimate goal is to be a general,
geometry-flavored toolkit for tracing structure through transformer
internals, not just a tool for GPT-2-specific interpretation.

## Getting started

```
uv sync                                       # install dependencies + this package
uv run python studies/gpt2_spacing_check.py   # run a study
uv run traceformer                            # the packaged entry point (currently a stub)
```

`traceformer.loading.load_gpt2()` tries to load GPT-2's weights/tokenizer
from the local `huggingface-hub` cache first, without touching the
network. If they aren't cached yet, it prints a notice and automatically
falls back to downloading them, so the first run just works.

## Repo layout

- `traceformer/` — the installable library. This is where the production
  code goes. Anything that seems generally useful to interpretation
  will go here. There won't be any infrastructure for specific experiments
  here (those still live in `studies/`). It's just for tools that should be
  general enough to apply to any transformer model.
- `studies/` — standalone research scripts and common tools for their setup,
  not a package. Each one is a self-contained experiment that applies
  `traceformer` to study a concept or test an algorithm. It's meant to be
  readable as a record of the reasoning, not just the code.

## A Note on AI Use
I use Claude to help write, debug, and document this project. See [AI-USE.md](./AI-USE.md) 
for specifics on what that looks like and where I draw the line on authorship.
