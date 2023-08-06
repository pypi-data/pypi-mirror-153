Assorted process and subprocess management functions.

*Latest release 20220606*:
* run: fold in the superior run() from cs.ebooks.
* pipefrom,pipeto: replace trace= with quiet= like run().
* print_argv: add an `end` parameter (used by pipefrom).

## Function `groupargv(pre_argv, argv, post_argv=(), max_argv=None, encode=False)`

Distribute the array `argv` over multiple arrays
to fit within `MAX_ARGV`.
Return a list of argv lists.

Parameters:
* `pre_argv`: the sequence of leading arguments
* `argv`: the sequence of arguments to distribute; this may not be empty
* `post_argv`: optional, the sequence of trailing arguments
* `max_argv`: optional, the maximum length of each distributed
  argument list, default: MAX_ARGV
* `encode`: default False.
  If true, encode the argv sequences into bytes for accurate tallying.
  If `encode` is a Boolean,
  encode the elements with their .encode() method.
  If `encode` is a `str`, encode the elements with their `.encode()`
  method with `encode` as the encoding name;
  otherwise presume that `encode` is a callable
  for encoding each element.

The returned argv arrays will contain the encoded element values.

## Function `PidFileManager(path, pid=None)`

Context manager for a pid file.

Parameters:
* `path`: the path to the process id file.
* `pid`: the process id to store in the pid file,
  default from `os.etpid`.

Writes the process id file at the start
and removes the process id file at the end.

## Function `pipefrom(argv, quiet=False, binary=False, keep_stdin=False, **kw)`

Pipe text from a command.
Optionally trace invocation.
Return the `Popen` object with `.stdout` decoded as text.

Parameters:
* `argv`: the command argument list
* `binary`: if true (default false)
  return the raw stdout instead of a text wrapper
* `quiet`: optional flag, default `False`;

  if `trace` is `True`, recite invocation to stderr
  otherwise presume that `trace` is a stream
  to which to recite the invocation.
* `keep_stdin`: if true (default `False`)
  do not attach the command's standard input to the null device.
  The default behaviour is to do so,
  preventing commands from accidentally
  consuming the main process' input stream.

Other keyword arguments are passed to the `io.TextIOWrapper`
which wraps the command's output.

## Function `pipeto(argv, quiet=False, **kw)`

Pipe text to a command.
Optionally trace invocation.
Return the Popen object with .stdin encoded as text.

Parameters:
* `argv`: the command argument list
* `trace`: if true (default `False`),
  if `trace` is `True`, recite invocation to stderr
  otherwise presume that `trace` is a stream
  to which to recite the invocation.

Other keyword arguments are passed to the `io.TextIOWrapper`
which wraps the command's input.

## Function `print_argv(*argv, indent='', subindent='  ', end='\n', file=None, fold=False)`

Print an indented possibly folded command line.

## Function `remove_pidfile(path)`

Truncate and remove a pidfile, permissions permitting.

## Function `run(argv, doit=True, logger=None, quiet=False, **subp_options)`

Run a command via `subprocess.run`.
Return the `CompletedProcess` result or `None` if `doit` is false.

Parameters:
* `argv`: the command line to run
* `doit`: optional flag, default `True`;
  if false do not run the command and return `None`
* `logger`: optional logger, default `None`;
  if `True`, use `logging.getLogger()`;
  if not `None` or `False` trace using `print_argv`
* `quiet`: default `False`; if true, do not print the command or its output
* `subp_options`: optional mapping of keyword arguments
  to pass to `subprocess.run`

## Function `signal_handler(sig, handler, call_previous=False)`

Context manager to push a new signal handler,
yielding the old handler,
restoring the old handler on exit.
If `call_previous` is true (default `False`)
also call the old handler after the new handler on receipt of the signal.

Parameters:
* `sig`: the `int` signal number to catch
* `handler`: the handler function to call with `(sig,frame)`
* `call_previous`: optional flag (default `False`);
  if true, also call the old handler (if any) after `handler`

## Function `signal_handlers(sig_hnds, call_previous=False, _stacked=None)`

Context manager to stack multiple signal handlers,
yielding a mapping of `sig`=>`old_handler`.

Parameters:
* `sig_hnds`: a mapping of `sig`=>`new_handler`
  or an iterable of `(sig,new_handler)` pairs
* `call_previous`: optional flag (default `False`), passed
  to `signal_handler()`

## Function `stop(pid, signum=<Signals.SIGTERM: 15>, wait=None, do_SIGKILL=False)`

Stop the process specified by `pid`, optionally await its demise.

Parameters:
* `pid`: process id.
  If `pid` is a string, treat as a process id file and read the
  process id from it.
* `signum`: the signal to send, default `signal.SIGTERM`.
* `wait`: whether to wait for the process, default `None`.
  If `None`, return `True` (signal delivered).
  If `0`, wait indefinitely until the process exits as tested by
  `os.kill(pid, 0)`.
  If greater than 0, wait up to `wait` seconds for the process to die;
  if it exits, return `True`, otherwise `False`;
* `do_SIGKILL`: if true (default `False`),
  send the process `signal.SIGKILL` as a final measure before return.

## Function `write_pidfile(path, pid=None)`

Write a process id to a pid file.

Parameters:
* `path`: the path to the pid file.
* `pid`: the process id to write, defautl from `os.getpid`.

# Release Log



*Release 20220606*:
* run: fold in the superior run() from cs.ebooks.
* pipefrom,pipeto: replace trace= with quiet= like run().
* print_argv: add an `end` parameter (used by pipefrom).

*Release 20220531*:
* New print_argv function for writing shell command lines out nicely.
* Bump requirements for cs.gimmicks.

*Release 20220504*:
signal_handlers: reshape try/except to avoid confusing traceback.

*Release 20220429*:
* New signal_handler(sig,handler,call_previous=False) context manager to push a signal handler.
* New signal_handlers() context manager to stack handlers for multiple signals.

*Release 20190101*:
Bugfix context manager cleanup. groupargv improvements.

*Release 20171112*:
Bugfix array length counting.

*Release 20171110*:
New function groupargv for breaking up argv lists to fit within the maximum argument limit; constant MAX_ARGV for the default limit.

*Release 20171031*:
run: accept optional pids parameter, a setlike collection of process ids.

*Release 20171018*:
run: replace `trace` parameter with `logger`, default None

*Release 20170908.1*:
remove dependency on cs.pfx

*Release 20170908*:
run: pass extra keyword arguments to subprocess.call

*Release 20170906.1*:
Add run, pipefrom and pipeto - were incorrectly in another module.

*Release 20170906*:
First PyPI release.
