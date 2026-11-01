# What is not proved yet

This file says what the code claims and how far that has been checked.

- **What the compiler has and has not seen.** `axle check` and `axle build` pass on Windows and Linux in CI, and
  `examples/hello` runs there with its exit status checked. That is one program exercising the parser, the
  suggestions and the errors. The 68 checks in `tools/axpy` run the *translated* sources: a model of the language,
  which does not model who owns a string (see the README's Honest status). Anything not reached by
  `examples/hello` is proved by the translator only.
- **Chaining starts from a `static fn`.** `Command::create(...).add(...)` is checked on the compiler; `new Command(...)
  .add(...)` is not valid Axle (`new X()` without parentheses reads as a statement), so the library offers
  `create` and never asks for the other form.
- **Numbers.** Integers are decimal with an optional sign and at most 18 digits. Floats are decimal with an
  optional fraction; there is no exponent (`1e3`) and no `inf` or `nan`.
- **Case.** Suggestions ignore the case of ASCII letters only.
- **A repeated option that is not declared `many`** keeps every value but `text`/`integer` read the last.
- **Strings are copied wherever they are stored.** A string read out of an object cannot be handed to a new
  owner, and a constructor that keeps its parameter keeps somebody else's memory. `Str::copy` is the answer; it
  costs an allocation per stored string, which a command line can afford.
- **Not there yet:** `--help` text, configuration files, environment variables, completion scripts, JSON and
  CSV output, prompts, progress and signal handling. See `doc/ROADMAP.md`.
