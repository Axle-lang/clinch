# Architecture

Layers, bottom to top. A module imports from below, never from above or from a sibling
(`tools/check.py` holds that sentence).

| Layer | Holds | Knows the operating system |
|---|---|---|
| `core` | the vocabulary and the logic: text, errors, the declaration, suggestions, parsing, help, configuration, output, completion | no |
| `raw` | raw memory, for the seams — *not written; nothing needs it yet* | no |
| `sys` | one answer per port (`win32`, `linux`): terminal, signals — *not written; `src/sys/` does not exist yet* | yes — the only place |
| `term` | prompts, progress, cancellation, over `sys` — *not written* | through `sys` |
| `app` | `parseProcess` (written): the process's own command line. `App::run` (planned): parse, resolve configuration, run, report | `parseProcess` asks `std` for the process's arguments and nothing else |

The point of the split is the tests: everything in `core` runs as Python over the translated sources, with
no terminal. The terminal and the signals are behind a seam that a fake answers.

## What it shares with a terminal UI library, and what it does not

A later library for full-screen interfaces will want the same arguments, the same configuration and the same
errors. It will depend on `clinch::core` for those. It will **not** share a renderer: `clinch` writes lines;
a full-screen interface owns the screen. Keeping the output of `clinch` to lines is what keeps the two
independent.

## Which structure for what

| Kind | Used for | Here |
|---|---|---|
| `const` | a number with a name | the `EXIT_*` statuses |
| `enum` | a closed set of named cases | `Kind`, `Source` |
| `struct` | plain data, copied on assignment, no identity | `Opt`, `Arg` |
| `class` | an identity and a state that changes | `Command`, `Parsed`, `Commands`, `Values`, `List` |
| `exception` | a failure a caller acts on | `CliError` and its reasons |
| free `fn` | a computation with no state | `core::text`, `core::suggest`, `parseLine`, `parseProcess` |

`Commands` exists because a `List` asks its rows to be `Copy`, and a `Command` cannot say so of itself while it
is still being declared: the subcommands of a command are kept by a small sequence of their own.

## Decisions worth knowing

- **A declaration is built by chaining from `Command::create(...)`.** The chain starts at a `static fn` because
  Axle reads `new Command(...).add(...)` as a statement; every method that continues it returns the command.
- **The parser is a free function, not a method of `Command`.** `parseProcess(root)` and `parseLine(root, words)`
  take the command; `root.parse(words)` was tried and dropped. It makes `core::spec` call `core::parse`, which
  already imports `spec`: the compiler accepts that import cycle but type-checks the generic parameter that
  crosses it (`Values<string>`) as a bare `Values`, and rejects the call (E0001). A non-generic `Words` type would
  lift it, at the price of one more type for the rare path; it is not worth it while `parseProcess` is the way in.
