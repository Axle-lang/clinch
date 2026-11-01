# What is not proved yet

This file says what the code claims and how far that has been checked.

- **Not compiled yet.** The sources were written against the Axle
  documentation and run through the Axle→Python translator in `tools/axpy`, which is a model of the
  language, not the compiler. CI runs `axle check` and `axle build` on Windows and Linux; until those jobs
  are green the compiler's word is the only one that counts.
- **Fluent chaining is not used.** Options are added with `cmd.add(...)` statements, not
  `cmd.add(...).add(...)`, because returning `self` from a `mut self` method is not something the
  documentation shows. If it works, an API like that can follow.
- **Numbers.** Integers are decimal with an optional sign and at most 18 digits. Floats are decimal with an
  optional fraction; there is no exponent (`1e3`) and no `inf` or `nan`.
- **Case.** Suggestions ignore the case of ASCII letters only.
- **A repeated option that is not declared `many`** keeps every value but `text`/`integer` read the last.
- **Not there yet:** `--help` text, configuration files, environment variables, completion scripts, JSON and
  CSV output, prompts, progress and signal handling. See `doc/ROADMAP.md`.
