# clinch

**The command line of an Axle program, declared once.**

Subcommands, options, positional arguments, validation with *"did you mean…?"*, and exit codes that mean
something — all read from one description of what the program accepts.

```axle
let serve : Command = Command::create("serve", "Run the server");
serve.alias("run");
serve.add(Opt::integer("-p, --port <n>", "Port to listen on", "8080"));
serve.add(Opt::choice("--format <fmt>", "Output", "text|json|csv", "text"));
serve.arg(Arg::required("root", "Folder to serve"));

let parsed : Parsed = Parser::parse(root, words);
let port : i64 = parsed.integer("port");
```

```
$ tool serve --prot 80 site
error: unknown option `--prot`
  did you mean `--port`?
$ echo $?
2
```

> **Status — slice 1.** What exists today: the declaration (`Command`, `Opt`, `Arg`), the parser, the
> suggestions, the errors and the exit statuses, with 67 checks over the translated sources. `--help`,
> configuration files, environment variables, completion scripts, structured output, prompts and signals
> are next; [`doc/ROADMAP.md`](doc/ROADMAP.md) says in which order, and
> [`LIMITATIONS.md`](LIMITATIONS.md) says what is not proved yet.

## What it reads

| Form | Example |
|---|---|
| long option | `--port 80`, `--port=80` |
| short option | `-p 80`, `-p80` |
| cluster of flags | `-vq`, `-vqp 80` |
| repeated option | `-I a -I b` → `parsed.all("include")` |
| subcommand and its alias | `serve`, `run` |
| end of options | `--` |
| a lone `-` | a positional (stdin, by convention) |

Every value is checked against the kind its option declares (`integer`, `number`, `path`, `text`,
`choice`) and a mistake says what was expected. Where a value came from — the command line, the
environment, a file or the default — is kept: `parsed.source("port")`.

## Layout

```
src/core/   the vocabulary and the logic, with no operating system   (text, error, spec, suggest, parse)
tools/      the checker, the wiring generator, the Axle→Python translator the tests run through
examples/   hello — the smallest program with a command line
```

## Build & check

```sh
python3 tools/check.py             # layers, seams, names, 110 columns
python3 tools/axpy/test_core.py    # the logic, run
cd examples/hello && axle build
```

MIT licensed.
