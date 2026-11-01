# Roadmap

Each slice is pushed on its own, with its tests, and leaves the tree green.

1. **Declaration and parsing** — `Command`, `Opt`, `Arg`, `Parser`, suggestions, errors, exit statuses. *Done.*
   - **1b. The process's own line** — `Args::parse(spec)`, so a program never walks `argc()`/`argAt()`; `UsageError::report()`; `Parsed::versionLine()`. *Written and run; awaiting the compiler.*
2. **Help and version** — `--help`, `--version`, usage lines, examples, aligned columns by terminal width.
3. **Configuration** — a TOML subset and JSON, `APP_*` environment variables, the order argv > env > file >
   default, and `--explain-config`.
4. **Output** — text, JSON and CSV from one description of the rows.
5. **Completion** — Bash, Zsh, Fish and PowerShell scripts generated from the `Command`.
6. **Terminal** — `sys` ports (`win32`, `linux`): is it a terminal, how wide, ANSI on Windows, Ctrl-C and
   SIGTERM; then `term`: confirmation, choice, progress and cancellation.
7. **`app::App::run`** — the front door tying it together; netaudit migrated to it as the demonstration.
