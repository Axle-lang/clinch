# What is not proved yet

What the code claims, and how far each claim has been checked. Three levels, from the strongest.

## Proved by the compiler

`axle check` and `axle build` pass on Windows and Linux in CI, and `examples/hello` is run there with its exit
status checked. That one program reaches:

- a command with a subcommand, an alias, a long option with a value and a required argument;
- `--version`;
- an unknown option, which prints the message and `did you mean …?` and exits with status 2.

## Only run through the translator

Everything else — the other forms of option, the validation of values, the suggestions for commands and
choices, the order of the sources, every error and its message — is run by the 74 checks in `tools/axpy`, which
translate the sources to Python. The translator is a model of the language, not the compiler, and there is one
thing it does not model: **who owns a string**. That is where the compiler and the executed example found real
bugs the Python never could (see the README's *Honest status*). So a path the example does not reach is
proved by the translator only, and may still meet the compiler's ownership rules.

## Limits by design

- **Numbers.** An integer is decimal with an optional sign and at most 18 digits. A float is decimal with an
  optional fraction: no exponent (`1e3`), no `inf`, no `nan`.
- **Case.** Suggestions ignore the case of ASCII letters only.
- **An option given twice.** If it is not declared `many`, every value is kept, but `text`, `integer` and `number`
  read the last one; `all` returns them all.
- **Strings are copied wherever they are stored.** A string read out of an object cannot be handed to a new
  owner, so `copyOf` makes a value of its own. It costs one allocation per stored string, which a command line can
  afford.

## Not written yet

`--help` text, configuration files, environment variables, completion scripts, JSON and CSV output, prompts,
progress and signal handling. [`doc/ROADMAP.md`](doc/ROADMAP.md) has the order.
