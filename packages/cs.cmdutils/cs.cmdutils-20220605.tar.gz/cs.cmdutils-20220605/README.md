Convenience functions for working with the Cmd module,
the BaseCommand class for constructing command line programmes,
and other command line related stuff.

*Latest release 20220605*:
* BaseCommand: new popopts(argv,...) compact getopt wrapper.
* BaseCommand: new poparg(argv,...) compact validating argument consumer.
* BaseCommand: drop run_argv, provided no utility.
* BaseCommand.run: get the RunState signal list from self.options.runstate_signals.
* BaseCommand.apply_opts: support multiple individual options raising GetoptError, as I hate commands which abort at the first bad option.
* Assorted other small things.

## Class `BaseCommand`

A base class for handling nestable command lines.

This class provides the basic parse and dispatch mechanisms
for command lines.
To implement a command line
one instantiates a subclass of `BaseCommand`:

    class MyCommand(BaseCommand):
        GETOPT_SPEC = 'ab:c'
        USAGE_FORMAT = r"""Usage: {cmd} [-a] [-b bvalue] [-c] [--] arguments...
          -a    Do it all.
          -b    But using bvalue.
          -c    The 'c' option!
        """
        ...

and provides either a `main` method if the command has no subcommands
or a suite of `cmd_`*subcommand* methods, one per subcommand.

Running a command is done by:

    MyCommand(argv).run()

Modules which implement a command line mode generally look like this:

    ... imports etc ...
    def main(argv=None):
        """ The command line mode.
        """
        return MyCommand(argv).run()
    ... other code ...
    class MyCommand(BaseCommand):
    ... other code ...
    if __name__ == '__main__':
        sys.exit(main(sys.argv))

Instances have a `self.options` attribute on which optional
modes are set,
avoiding conflict with the attributes of `self`.

Subclasses with no subcommands
generally just implement a `main(argv)` method.

Subclasses with subcommands
should implement a `cmd_`*subcommand*`(argv)` instance method
for each subcommand.
If a subcommand is itself implemented using `BaseCommand`
then it can be a simple attribute:

    cmd_subthing = SubThingCommand

Returning to methods, if there is a paragraph in the method docstring
commencing with `Usage:`
then that paragraph is incorporated automatically
into the main usage message.
Example:

    def cmd_ls(self, argv):
        """ Usage: {cmd} [paths...]
              Emit a listing for the named paths.

            Further docstring non-usage information here.
        """
        ... do the "ls" subcommand ...

The subclass is customised by overriding the following methods:
* `apply_defaults()`:
  prepare the initial state of `self.options`
  before any command line options are applied.
* `apply_opt(opt,val)`:
  apply an individual getopt global command line option
  to `self.options`.
* `apply_opts(opts)`:
  apply the `opts` to `self.options`.
  `opts` is an `(option,value)` sequence
  as returned by `getopot.getopt`.
  The default implementation iterates over these and calls `apply_opt`.
* `cmd_`*subcmd*`(argv)`:
  if the command line options are followed by an argument
  whose value is *subcmd*,
  then the method `cmd_`*subcmd*`(subcmd_argv)`
  will be called where `subcmd_argv` contains the command line arguments
  following *subcmd*.
* `main(argv)`:
  if there are no command line arguments after the options
  or the first argument does not have a corresponding
  `cmd_`*subcmd* method
  then method `main(argv)`
  will be called where `argv` contains the command line arguments.
* `run_context()`:
  a context manager to provide setup or teardown actions
  to occur before and after the command implementation respectively,
  such as to open and close a database.

Editorial: why not arparse?
Primarily because when incorrectly invoked
an argparse command line prints the help/usage messgae
and aborts the whole programme with `SystemExit`.

*Method `BaseCommand.__init__(self, argv=None, *, cmd=None, options=None, **kw_options)`*:
Initialise the command line.
Raises `GetoptError` for unrecognised options.

Parameters:
* `argv`:
  optional command line arguments
  including the main command name if `cmd` is not specified.
  The default is `sys.argv`.
  The contents of `argv` are copied,
  permitting desctructive parsing of `argv`.
* `cmd`:
  optional keyword specifying the command name for context;
  if this is not specified it is taken from `argv.pop(0)`.
* `options`:
  an optional keyword providing object for command state and context.
  If not specified a new `self.OPTIONS_CLASS` instance
  is allocated for use as `options`.
  The default `OPTIONS_CLASS` is `BaseCommandOptions`,
  a `SimpleNamespace` with some prefilled attributes and properties
  to aid use later.
  These can be further updated by the `.apply_default()` method.
Other keyword arguments are applied to `self.options`
as attributes.

The `cmd` and `argv` parameters have some fiddly semantics for convenience.
There are 3 basic ways to initialise:
* `BaseCommand()`: `argv` comes from `sys.argv`
  and the value for `cmd` is derived from `argv[0]`
* `BaseCommand(argv)`: `argv` is the complete command line
  including the command name and the value for `cmd` is
  derived from `argv[0]`
* `BaseCommand(argv, cmd=foo)`: `argv` is the command
  arguments _after_ the command name and `cmd` is set to
  `foo`

The command line arguments are parsed according to
the optional `GETOPT_SPEC` class attribute (default `''`).
If `getopt_spec` is not empty
then `apply_opts(opts)` is called
to apply the supplied options to the state
where `opts` is the return from `getopt.getopt(argv,getopt_spec)`.

After the option parse,
if the first command line argument *foo*
has a corresponding method `cmd_`*foo*
then that argument is removed from the start of `argv`
and `self.cmd_`*foo*`(argv,options,cmd=`*foo*`)` is called
and its value returned.
Otherwise `self.main(argv,options)` is called
and its value returned.

If the command implementation requires some setup or teardown
then this may be provided by the `run_context`
context manager method,
called with `cmd=`*subcmd* for subcommands
and with `cmd=None` for `main`.

*`BaseCommand.OPTIONS_CLASS`*

*Method `BaseCommand.__init_subclass__()`*:
Update subclasses of `BaseCommand`.

Appends the usage message to the class docstring.

*Method `BaseCommand.apply_defaults(self)`*:
Stub `apply_defaults` method.

Subclasses can override this to set up the initial state of `self.options`.

*Method `BaseCommand.apply_opt(self, *a, **kw)`*:
Handle an individual global command line option.

This default implementation raises a `RuntimeError`.
It only fires if `getopt` actually gathered arguments
and would imply that a `GETOPT_SPEC` was supplied
without an `apply_opt` or `apply_opts` method to implement the options.

*Method `BaseCommand.apply_opts(self, opts)`*:
Apply command line options.

Subclasses can override this
but it is usually easier to override `apply_opt(opt,val)`.

*Method `BaseCommand.apply_preargv(self, argv)`*:
Do any preparsing of `argv` before the subcommand/main-args.
Return the remaining arguments.

This default implementation returns `argv` unchanged.

*Method `BaseCommand.cmd_help(argv)`*:
Usage: {cmd} [-l] [subcommand-names...]
Print the full help for the named subcommands,
or for all subcommands if no names are specified.
-l  Long help even if no subcommand-names provided.

*Method `BaseCommand.getopt_error_handler(cmd, options, e, usage, subcmd=None)`*:
The `getopt_error_handler` method
is used to control the handling of `GetoptError`s raised
during the command line parse
or during the `main` or `cmd_`*subcmd*` calls.

This default handler issues a warning containing the exception text,
prints the usage message to standard error,
and returns `True` to indicate that the error has been handled.

The handler is called with these parameters:
* `cmd`: the command name
* `options`: the `options` object
* `e`: the `GetoptError` exception
* `usage`: the command usage or `None` if this was not provided
* `subcmd`: optional subcommand name;
  if not `None`, is the name of the subcommand which caused the error

It returns a true value if the exception is considered handled,
in which case the main `run` method returns 2.
It returns a false value if the exception is considered unhandled,
in which case the main `run` method reraises the `GetoptError`.

To let the exceptions out unhandled
this can be overridden with a method which just returns `False`.

Otherwise,
the handler may perform any suitable action
and return `True` to contain the exception
or `False` to cause the exception to be reraised.

*Method `BaseCommand.poparg(argv: List[str], *a)`*:
Pop the leading argument off `argv` and parse it.
Return the parsed argument.
Raises `getopt.GetoptError` on a missing or invalid argument.

This is expected to be used inside a `main` or `cmd_*`
command handler method or inside `apply_preargv`.

You can just use:

    value = argv.pop(0)

but this method provides conversion and valuation
and a richer failure mode.

Parameters:
* `argv`: the argument list, which is modified in place with `argv.pop(0)`
* the argument list `argv` may be followed by some help text
  and/or an argument parser function.
* `validate`: an optional function to validate the parsed value;
  this should return a true value if valid,
  or return a false value or raise a `ValueError` if invalid
* `unvalidated_message`: an optional message after `validate`
  for values failing the validation

Typical use inside a `main` or `cmd_*` method might look like:

    self.options.word = self.poparg(argv, int, "a count value")
    self.options.word = self.poparg(
        argv, int, "a count value",
       lambda count: count > 0, "count should be positive")

Because it raises `GetoptError` on a bad argument
the normal usage message failure mode follows automatically.

Demonstration:

    >>> argv = ['word', '3', 'nine', '4']
    >>> BaseCommand.poparg(argv, "word to process")
    'word'
    >>> BaseCommand.poparg(argv, int, "count value")
    3
    >>> BaseCommand.poparg(argv, float, "length")
    Traceback (most recent call last):
      ...
    getopt.GetoptError: length 'nine': float('nine'): could not convert string to float: 'nine'
    >>> BaseCommand.poparg(argv, float, "width", lambda width: width > 5)
    Traceback (most recent call last):
      ...
    getopt.GetoptError: width '4': invalid value
    >>> BaseCommand.poparg(argv, float, "length")
    Traceback (most recent call last):
      ...
    getopt.GetoptError: length: missing argument

*Method `BaseCommand.popopts(argv, attrfor=None, **opt_specs)`*:
Parse option switches from `argv`, a list of command line strings
with leading option switches.
Modify `argv` in place and return a dict mapping switch names to values.

The optional positional argument `attrfor`
may supply an object whose attributes may be set by the options,
for example:

    def cmd_foo(self, argv):
        self.popopts(argv, self.options, a='all', j_=('jobs', int))
        ... use self.options.jobs etc ...

The expected options are specified by the keyword parameters
in `opt_specs`:
* options not starting with a letter may be preceeded by an underscore
  to allow use in the parameter list, for example `_1='once'`
  for a `-1` option setting the `once` option name
* a single letter name specifies a short option
  and a multiletter name specifies a long option
* options requiring an argument have a trailing underscore
* options not requiring an argument normally imply a value
  of `True`; if their synonym commences with a dash they will
  imply a value of `False`, for example `n='dry_run',y='-dry_run'`

Example:

    >>> import os.path
    >>> options = SimpleNamespace(
    ...   all=False,
    ...   jobs=1,
    ...   number=0,
    ...   once=False,
    ...   path=None,
    ...   trace_exec=True,
    ...   verbose=False,
    ...   dry_run=False)
    >>> argv = ['-1', '-v', '-y', '-j4', '--path=/foo', 'bah', '-x']
    >>> opt_dict = BaseCommand.popopts(
    ...   argv,
    ...   options,
    ...   _1='once',
    ...   a='all',
    ...   j_=('jobs',int),
    ...   n='dry_run',
    ...   v='verbose',
    ...   x='-trace_exec',
    ...   y='-dry_run',
    ...   dry_run=None,
    ...   path_=(str, os.path.isabs, 'not an absolute path'),
    ...   verbose=None,
    ... )
    >>> opt_dict
    {'once': True, 'verbose': True, 'dry_run': False, 'jobs': 4, 'path': '/foo'}
    >>> options
    namespace(all=False, jobs=4, number=0, once=True, path='/foo', trace_exec=True, verbose=True, dry_run=False)

*Method `BaseCommand.run(self, **kw_options)`*:
Run a command.
Returns the exit status of the command.
May raise `GetoptError` from subcommands.

Any keyword arguments are used to override `self.options` attributes
for the duration of the run,
for example to presupply a shared `RunState` from an outer context.

If the first command line argument *foo*
has a corresponding method `cmd_`*foo*
then that argument is removed from the start of `argv`
and `self.cmd_`*foo*`(cmd=`*foo*`)` is called
and its value returned.
Otherwise `self.main(argv)` is called
and its value returned.

If the command implementation requires some setup or teardown
then this may be provided by the `run_context()`
context manager method.

*Method `BaseCommand.run_context(self)`*:
Stub context manager which surrounds `main` or `cmd_`*subcmd*.

*Method `BaseCommand.subcommand_usage_text(subcmd, usage_format_mapping=None, short=False)`*:
Return the usage text for a subcommand.

Parameters:
* `subcmd`: the subcommand name
* `short`: just include the first line of the usage message,
  intented for when there are many subcommands

*Method `BaseCommand.subcommands()`*:
Return a mapping of subcommand names to subcommand specifications
for class attributes which commence with `cls.SUBCOMMAND_METHOD_PREFIX`
by default `'cmd_'`.

*Method `BaseCommand.usage_text(*, cmd=None, format_mapping=None, subcmd=None, short=False)`*:
Compute the "Usage:" message for this class
from the top level `USAGE_FORMAT`
and the `'Usage:'`-containing docstrings
from its `cmd_*` methods.

Parameters:
* `cmd`: optional command name, default derived from the class name
* `format_mapping`: an optional format mapping for filling
  in format strings in the usage text
* `subcmd`: constrain the usage to a particular subcommand named `subcmd`;
  this is used to produce a shorter usage for subcommand usage failures

## Class `BaseCommandOptions(types.SimpleNamespace)`

A base class for the `BaseCommand` `options` object.

This is the default class for the `self.options` object
available during `BaseCommand.run()`.

It comes prefilled with:
* `.dry_run=False`
* `.force=False`
* `.quiet=False`
* `.verbose=False`
and a `.doit` property which is the inverse of `.dry_run`.

*Property `BaseCommandOptions.doit`*:
I usually use a `doit` flag,
the inverse of `dry_run`.

*Method `BaseCommandOptions.popopts(self, argv, **opt_specs)`*:
Convenience method to appply `BaseCommand.popopts` to the options.

## Function `docmd(dofunc)`

Decorator for `cmd.Cmd` subclass methods
to supply some basic quality of service.

This decorator:
- wraps the function call in a `cs.pfx.Pfx` for context
- intercepts `getopt.GetoptError`s, issues a `warning`
  and runs `self.do_help` with the method name,
  then returns `None`
- intercepts other `Exception`s,
  issues an `exception` log message
  and returns `None`

The intended use is to decorate `cmd.Cmd` `do_`* methods:

    from cmd import Cmd
    from cs.cmdutils import docmd
    ...
    class MyCmd(Cmd):
        @docmd
        def do_something(...):
            ... do something ...

# Release Log



*Release 20220605*:
* BaseCommand: new popopts(argv,...) compact getopt wrapper.
* BaseCommand: new poparg(argv,...) compact validating argument consumer.
* BaseCommand: drop run_argv, provided no utility.
* BaseCommand.run: get the RunState signal list from self.options.runstate_signals.
* BaseCommand.apply_opts: support multiple individual options raising GetoptError, as I hate commands which abort at the first bad option.
* Assorted other small things.

*Release 20220429*:
* BaseCommand: fold dots in argv[0] into underscores, supports subcommands like "setup.py".
* BaseCommand: new popargv(argv[,help_text[,parse[,validate[,unvalidated_message]]]]) helper class method.
* BaseCommand: accept dashed-form of the underscored_form subcommand name.
* BaseCommand: new self.options.runstate_signals=SIGINT,SIGTERM specifying singals to catch-and-cancel, shuffle run() context managers.

*Release 20220318*:
BaseCommand.__init__: handle main() method in the New Scheme.

*Release 20220315*:
_BaseSubCommand.__init__: hook in the class USAGE_KEYWORDS for methods.

*Release 20220311*:
BaseCommand: big refactor of subcommand internals and make the "cmd_foo=FooCommand" implementation work properly.

*Release 20211208*:
BaseCommand: better handle an unknown subcommand.

*Release 20210927*:
* Usage: show only the per subcommand usage for in-subcommand GetoptError.
* Usage: show terse usage when the subcommand cannot be recognised.
* Usage: support bare -h, -help, --help.

*Release 20210913*:
New BaseCommand.apply_preargv method to gather special arguments before subcommands.

*Release 20210906*:
* BaseCommand.cmd_help: bugfix obsolete parameter list.
* BaseCommand.SUBCOMMAND_ARGV_DEFAULT: support a single str value, turn into list.

*Release 20210809*:
Bugfix BaseCommand.cmd_help for modern API.

*Release 20210731*:
* BaseCommand.run: apply optional keyword arguments to self.options during the run.
* Look for self.SUBCOMMAND_ARGV_DEFAULT if no subcommand is supplied.
* Bugfix case for "main" method and no "cmd_*" methods.
* Bugfix BaseCommand.cmd_help.

*Release 20210420*:
* BaseCommand.getopt_error_handler: replace error print() with warning().
* Docstring improvements.

*Release 20210407.1*:
BaseCommand: bugfix for __init_subclass__ docstring update.

*Release 20210407*:
* BaseCommand.__init_subclass__: behave sanely if the subclass has no initial __doc__.
* BaseCommand: new .run_argv convenience method, obviates the "def main" boilerplate.

*Release 20210404*:
BaseCommand subclasses: automatically add the main usage message to the subclass docstring.

*Release 20210306*:
* BREAKING CHANGE: rework BaseCommand as a more normal class instantiated with argv and with most methods being instance methods, getting the former `options` parameter from self.options.
* BaseCommand: provide default `apply_opt` and `apply_opts` methods; subclasses will generally just override the former.

*Release 20210123*:
BaseCommand: propagate the format mapping (cmd, USAGE_KEYWORDS) to the subusage generation.

*Release 20201102*:
* BaseCommand.cmd_help: supply usage only for "all commands", full docstring for specified commands.
* BaseCommand: honour presupplied options.log_level.
* BaseCommand.usage_text: handle missing USAGE_FORMAT better.
* BaseCommand.run: provide options.upd.
* BaseCommand subclasses may now override BaseCommand.OPTIONS_CLASS (default SimpleNamespace) in order to provide convenience methods on the options.
* BaseCommand.run: separate variable for subcmd with dash translated to underscore to match method names.
* Minor fixes.

*Release 20200615*:
BaseCommand.usage_text: do not mention the "help" command if it is the only subcommand (it won't be available if there are no other subcommands).

*Release 20200521.1*:
Fix DISTINFO.install_requires.

*Release 20200521*:
* BaseCommand.run: support using BaseCommand subclasses as cmd_* names to make it easy to nest BaseCommands.
* BaseCommand: new hack_postopts_argv method called after parsing the main command line options, for inferring subcommands or the like.
* BaseCommand: extract "Usage:" paragraphs from subcommand method docstrings to build the main usage message.
* BaseCommand: new cmd_help default command.
* Assorted bugfixes and small improvements.

*Release 20200318*:
* BaseCommand.run: make argv optional, get additional usage keywords from self.USAGE_KEYWORDS.
* @BaseCommand.add_usage_to_docstring: honour cls.USAGE_KEYWORDS.
* BaseCommand: do not require GETOPT_SPEC for commands with no defined options.
* BaseCommand.run: call cs.logutils.setup_logging.

*Release 20200229*:
Improve subcommand selection logic, replace StackableValues with stackattrs, drop `cmd` from arguments passed to main/cmd_* methods (present in `options`).

*Release 20200210*:
* New BaseCommand.add_usage_to_docstring class method to be called after class setup, to append the usage message to the class docstring.
* BaseCommand.run: remove spurious Pfx(cmd), as logutils does this for us already.

*Release 20190729*:
BaseCommand: support for a USAGE_FORMAT usage message format string and a getopt_error_handler method.

*Release 20190619.1*:
Another niggling docstring formatting fix.

*Release 20190619*:
Minor documentation updates.

*Release 20190617.2*:
Lint.

*Release 20190617.1*:
Initial release with @docmd decorator and alpha quality BaseCommand command line assistance class.
