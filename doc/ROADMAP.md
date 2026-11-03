# Roadmap

Each slice is pushed on its own, with its checks.

1. **Declaration and listening** — `Command`, `Opt`, `Arg`, `listen`, `listenTo`, suggestions, errors, statuses. *Done.*
2. **Help and version** — `--help` and `--version` written from the declaration: usage, aligned columns, examples. *Done.*
3. **Configuration** — a TOML subset and JSON, `APP_*` environment variables, the order argv > env > file > default.
4. **Output** — text, JSON and CSV from one description of the rows.
5. **Completion** — Bash, Zsh, Fish and PowerShell scripts generated from the declaration.
6. **Terminal** — is it a terminal, how wide, ANSI on Windows, Ctrl-C; confirmation, choice, progress, cancellation.
7. **netaudit** moved onto it, as the demonstration.
