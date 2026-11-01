"""The portable parts of clinch, run through the translated source: no terminal behind them."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from axpy.run import load  # noqa: E402
from axpy import rt  # noqa: E402

g = load()
fails = []
checks = [0]


def check(name, cond, extra=""):
    checks[0] += 1
    print(("ok   " if cond else "FAIL ") + name + (" " + str(extra) if extra and not cond else ""))
    if not cond:
        fails.append(name)


def thrown(fn):
    """The exception `fn` raises, or None."""
    try:
        fn()
    except Exception as e:
        return e
    return None


def words(*ws):
    v = g.Values()
    for w in ws:
        v.add(w)
    return v


def strs(v):
    return [v.at(i) for i in range(v.size())]


# --- text ------------------------------------------------------------------------------------
check("Str::toInt reads signed decimals", g.parseInt("-42") == (True, -42) and g.parseInt("+7") == (True, 7))
check("Str::toInt refuses words and empties", not g.parseInt("4x")[0] and not g.parseInt("")[0] and not g.parseInt("-")[0])
check("Str::toFloat reads fractions", g.parseFloat("3.25") == (True, 3.25) and g.parseFloat("-0.5")[1] == -0.5)
check("Str::toFloat refuses lone dots", not g.parseFloat(".")[0] and not g.parseFloat("1.x")[0] and g.parseFloat("2")[0])
check("Str::pad counts codepoints", g.padRight("é", 3) == "é  " and g.padRight("abcd", 2) == "abcd")
check("Str::repeat", g.repeatText("ab", 3) == "ababab" and g.repeatText("x", 0) == "")

# --- suggestions -----------------------------------------------------------------------------
check("distance is 0 for equal words", g.editDistance("abc", "abc") == 0)
check("distance counts a substitution", g.editDistance("kitten", "sitten") == 1)
check("distance counts a swap of neighbours as one", g.editDistance("serve", "sevre") == 1)
check("distance against empty is the length", g.editDistance("", "abc") == 3 and g.editDistance("ab", "") == 2)
check("distance of kitten and sitting is 3", g.editDistance("kitten", "sitting") == 3)
cands = words("--verbose", "--version", "--output")
check("nearest finds the near miss", g.nearestWord("--verbos", cands) == "--verbose")
check("nearest says nothing for a far word", g.nearestWord("--zzzzzz", cands) == "")
check("nearest ignores case", g.nearestWord("--OUTPUT", cands) == "--output")
check("a short word may be one edit away", g.nearestWord("lst", words("list", "add")) == "list")

# --- the spec --------------------------------------------------------------------------------
o = g.Opt.integer("-j, --jobs <n>", "Parallel jobs", "4")
check("an option is read from its declaration", (o.name, o.letter, o.value) == ("jobs", "j", "n"), (o.name, o.letter, o.value))
check("label writes it back", o.label() == "-j, --jobs <n>", o.label())
check("a long-only option aligns", g.Opt.flag("--color", "x").label() == "    --color")
check("a value name defaults to its kind", g.Opt.path("--out", "x", "").value == "path")
check("integer accepts whole numbers only", o.accepts("12") and o.accepts("-3") and not o.accepts("1.5") and not o.accepts("x"))
ch = g.Opt.choice("--format <fmt>", "Output", "text|json|csv", "text")
check("choice lists its words", strs(ch.words()) == ["text", "json", "csv"])
check("choice accepts only its words", ch.accepts("json") and not ch.accepts("xml"))
check("choice says what it expects", ch.expects() == "one of text, json, csv", ch.expects())
check("a flag takes no value", not g.Opt.flag("-v", "x").takesValue() and o.takesValue())
check("positional usage text", g.Arg.required("root", "x").usage() == "<root>" and g.Arg.optional("a", "x").usage() == "[a]" and g.Arg.rest("f", "x").usage() == "[f...]")


def app():
    serve = (g.Command.create("serve", "Run the server")
             .alias("run")
             .add(g.Opt.integer("-p, --port <n>", "Port", "8080"))
             .add(g.Opt.many("-I, --include <dir>", "Search path"))
             .add(g.Opt.flag("-q, --quiet", "Quiet"))
             .arg(g.Arg.required("root", "Folder"))
             .arg(g.Arg.rest("extra", "More")))
    return (g.Command.create("tool", "A tool")
            .version("1.2.0")
            .add(g.Opt.flag("-v, --verbose", "More output"))
            .add(g.Opt.choice("--format <fmt>", "Output", "text|json|csv", "text"))
            .sub(serve)
            .sub(g.Command.create("list", "List things").arg(g.Arg.optional("filter", "Filter"))))


def run(*argv):
    return g.parseLine(app(), words(*argv))


c = g.Command.create("a", "x")
check("declarations chain on the same object", c.version("1").alias("b").add(g.Opt.flag("-f", "x")) is c and c.opts.size() == 1)

# --- parsing ---------------------------------------------------------------------------------
p = run("serve", "site")
check("a subcommand is found", p.path() == "tool serve", p.path())
check("a positional is read", p.arg("root") == "site")
check("a default fills in", p.integer("port") == 8080 and p.source("port") == g.Source.Default)
check("the root default is inherited", p.text("format") == "text")
p = run("serve", "--port", "9000", "site")
check("long option, separate value", p.integer("port") == 9000 and p.source("port") == g.Source.Argv)
check("long option with =", run("serve", "--port=81", "s").integer("port") == 81)
check("short option, separate value", run("serve", "-p", "82", "s").integer("port") == 82)
check("short option, glued value", run("serve", "-p83", "s").integer("port") == 83)
p = run("serve", "-qp", "84", "s")
check("a cluster ends with a value option", p.flag("quiet") and p.integer("port") == 84)
check("an alias names its command", run("run", "s").path() == "tool serve")
check("options of the parent work after the subcommand", run("serve", "s", "--verbose").flag("verbose"))
check("options of the parent work before it", run("-v", "serve", "s").flag("verbose"))
check("an absent flag is off", not run("serve", "s").flag("verbose"))
p = run("serve", "-I", "a", "-I", "b", "-Ic", "s")
check("a repeated option keeps all its values", strs(p.all("include")) == ["a", "b", "c"], strs(p.all("include")))
p = run("serve", "s", "x", "y", "z")
check("the rest argument takes what remains", strs(p.rest("extra")) == ["x", "y", "z"], strs(p.rest("extra")))
p = run("serve", "--", "-weird", "--name")
check("-- makes the rest positional", p.arg("root") == "-weird" and strs(p.rest("extra")) == ["--name"], p.arg("root"))
check("a lone - is a positional", run("serve", "-").arg("root") == "-")
check("a negative number is a value", run("serve", "-p", "-5", "s").integer("port") == -5)
check("--flag=false switches a flag off", not run("serve", "--quiet=false", "s").flag("quiet"))
check("--help stops the reading", run("serve", "--help").helpAsked and run("-h").helpAsked)
p = run("serve", "-h")
check("--help names the command it was asked of", p.helpAsked and p.path() == "tool serve")
check("--version is answered when the root has one", run("--version").versionAsked and run("-V").versionAsked)
check("the choice is checked", run("--format", "json", "list").text("format") == "json")

# --- refusals --------------------------------------------------------------------------------
e = thrown(lambda: run("serve", "--prot", "1", "s"))
check("an unknown option is refused with a suggestion", isinstance(e, g.UnknownOption) and e.suggestion == "--port", e)
check("an unknown option is a UsageError with status 2", isinstance(e, g.UsageError) and e.code == 2)
check("the hint reads as a sentence", e.hint == "did you mean `--port`?", e.hint)
e = thrown(lambda: run("sevre", "x"))
check("an unknown command is refused", isinstance(e, g.UnknownCommand) and e.name == "sevre", e)
check("an unknown command suggests the nearest", e.suggestion == "serve", e.suggestion)
e = thrown(lambda: run("serve", "--port"))
check("a missing value is refused", isinstance(e, g.MissingValue) and e.option == "--port", e)
e = thrown(lambda: run("serve", "--port", "--quiet", "s"))
check("a value that is an option is a missing value", isinstance(e, g.MissingValue), e)
e = thrown(lambda: run("serve", "--port", "abc", "s"))
check("a value of the wrong kind is refused", isinstance(e, g.InvalidValue) and e.expected == "a whole number", e)
e = thrown(lambda: run("--format", "jsno", "list"))
check("a near-miss choice is suggested", isinstance(e, g.InvalidValue) and e.suggestion == "json", e)
check("the message names the choices", "one of text, json, csv" in e.message, e.message)
e = thrown(lambda: run("serve"))
check("a missing required argument is refused", isinstance(e, g.MissingArgument) and e.argument == "root", e)
e = thrown(lambda: run("list", "a", "b"))
check("one argument too many is refused", isinstance(e, g.UnexpectedArgument) and e.value == "b", e)
e = thrown(lambda: run("serve", "-z", "s"))
check("an unknown short option is refused", isinstance(e, g.UnknownOption) and e.name == "-z", e)
e = thrown(lambda: run("list", "--quiet"))
check("an option of a sibling command is unknown here", isinstance(e, g.UnknownOption), e)
e = thrown(lambda: run())
check("a bare call of a command group asks for a command", isinstance(e, g.UsageError), e)

# --- the process's own command line ----------------------------------------------------------
rt.ARGV[:] = ["tool", "serve", "--port", "9000", "site"]
check("the process's words skip the program's name", strs(g.processWords()) == ["serve", "--port", "9000", "site"], strs(g.processWords()))
p = g.parseProcess(app())
check("Args::parse reads the process's own line", p.path() == "tool serve" and p.integer("port") == 9000 and p.arg("root") == "site")
rt.ARGV[:] = ["tool", "serve", "--prot", "1", "s"]
e = thrown(lambda: g.parseProcess(app()))
check("a mistake on the process's line is reported", isinstance(e, g.UsageError) and e.report() == "error: unknown option `--prot`\n  did you mean `--port`?", e)
rt.ARGV[:] = ["tool"]
check("no words is no words", g.processWords().size() == 0)
rt.ARGV[:] = ["tool", "--version"]
check("the version line names the program", g.parseProcess(app()).versionLine() == "tool 1.2.0")
check("a report without a hint is one line", g.UsageError("boom", "").report() == "error: boom")

# --- exit codes ------------------------------------------------------------------------------
check("exit statuses follow sysexits", (g.EXIT_OK, g.EXIT_USAGE, g.EXIT_CONFIG, g.EXIT_INTERRUPTED) == (0, 2, 78, 130))
c = g.ConfigError("app.toml", "line 3: expected `=`")
check("a config error names its source and exits 78", "app.toml" in c.message and c.code == 78 and isinstance(c, g.CliError))

# --- precedence ------------------------------------------------------------------------------
p = g.readLine(app(), words("serve", "s"))
p.offer("port", "7000", g.Source.Config)
p.offer("port", "7100", g.Source.Env)
p.offer("port", "7200", g.Source.Config)
p.seal()
check("env beats config, which beats the default", p.integer("port") == 7100 and p.source("port") == g.Source.Env, p.text("port"))
p = g.readLine(app(), words("serve", "-p", "1", "s"))
p.offer("port", "7100", g.Source.Env)
p.seal()
check("the command line beats the environment", p.integer("port") == 1 and p.source("port") == g.Source.Argv)

print("\n%d checks, %d failed" % (checks[0], len(fails)))
sys.exit(1 if fails else 0)
