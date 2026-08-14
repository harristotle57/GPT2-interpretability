# AI Use Policy

This is a solo portfolio project, and I use Claude (Anthropic) throughout it for writing 
code, debugging, documenting, and quick prototyping. This document is here so anyone 
reading the repo knows where I've used it and how I think about ownership.

## Default assumption
I use Claude as a tool throughout this project the same way I'd use an IDE's autocomplete
or a linter. The workflow varies. Sometimes I write a draft and have Claude edit and refine.
Sometimes I ideate with Claude, then have Claude write the first draft, once it has context.
I don't think tagging every AI-touched character is meaningful, so with that in mind, this is
the policy.

**Unless a file says otherwise, assume it's `ai-assisted`:** I wrote it, drove the decisions
in it, or substantially reworked what Claude drafted. This covers most of the repo and isn't
called out file by file.

File-level tags only appear when a file deviates from that default (i.e. when I want to flag
something as *less* mine than the baseline):

- `# AI-DISCLOSURE: ai-generated` — Claude wrote the bulk of this, I've reviewed and understand
  it, but I didn't substantially rework it.
- `# AI-DISCLOSURE: ai-autonomous` — Claude-drafted and not yet fully reviewed by me. Treat with
  more skepticism than the rest of the repo. This tag is temporary by design: as I review a
  file, I either rewrite it toward `ai-assisted` or relabel it `ai-generated` and drop the tag.

This applies to prose as much as code. Interpretation and analysis I draft with Claude under
my direction, then review and rewrite, is `ai-assisted` like everything else. If something is
sitting in the repo as an unreviewed AI draft of an interpretation, it's tagged
`ai-autonomous`, same as unreviewed code, and isn't presented as a finished conclusion until
that tag comes off.

## Examples of where I use it

- **Translating papers → code.** When I'm implementing a method from a reference paper, I use 
  Claude to draft an initial version of what I understand the method to be, then work through 
  it until I can explain why it's right or fix it if it isn't.
- **Debugging.** Pasting errors, stack traces, unexpected outputs.
- **Boilerplate.** Plotting code, docstrings, trivial infrastructure/glue code.
- **Prototyping.** Fast throwaway scripts to test an idea before committing to it.
- **Documentation maintenance.** Keeping the README and docstrings current as the project evolves.

## Examples of where I don't

- **Research decisions.** I'm driving decisions such as what to try next, how to interpret a
  result, and whether an approach is working. Claude helps me execute an idea faster; it doesn't
  choose the idea.
- **Final judgment.** Nothing ships because Claude proposed it. It ships because I
  decided it was right. If I don't have a solution handy, I'll iterate with Claude until one
  surfaces, but I still evaluate and select the outcome.

## Conclusion

I don't have any particular hardline "AI will never touch X" position. While I'm still learning
how best to use AI assistence, I think it's counterproductive to take any strong position. My
understanding of the tool is still developing and the details of how exactly AI should be used
is extremely fuzzy. Currently the guiding principal is that I am making the decisions for this
project and using AI to accomplish those goals as efficiently as possible. This document will
inevitably evolve as I see how I want to use AI in my process.

_Last updated: 2026-08-13_