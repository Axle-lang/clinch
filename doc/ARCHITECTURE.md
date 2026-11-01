# Architecture

Layers, bottom to top. A module imports from below, never from above or from a sibling
(`tools/check.py` holds that sentence).

| Layer | Holds | Knows the operating system |
|---|---|---|
| `core` | the vocabulary and the logic: text, errors, the declaration, suggestions, parsing, help, configuration, output, completion | no |
| `raw` | raw memory, for the seams — *not written; nothing needs it yet* | no |
| `sys` | one answer per port (`win32`, `linux`): terminal, signals — *not written; `src/sys/` does not exist yet* | yes — the only place |
| `term` | prompts, progress, cancellation, over `sys` — *not written* | through `sys` |
| `app` | `Args` (written): the process's own command line. `App::run` (planned): parse, resolve configuration, run, report | `Args` asks `std` for the process's arguments and nothing else |

The point of the split is the tests: everything in `core` runs as Python over the translated sources, with
no terminal. The terminal and the signals are behind a seam that a fake answers.

## What it shares with a terminal UI library, and what it does not

A later library for full-screen interfaces will want the same arguments, the same configuration and the same
errors. It will depend on `clinch::core` for those. It will **not** share a renderer: `clinch` writes lines;
a full-screen interface owns the screen. Keeping the output of `clinch` to lines is what keeps the two
independent.
