[![Coverage Status](https://coveralls.io/repos/github/i386x/vutils-cli/badge.svg?branch=main)](https://coveralls.io/github/i386x/vutils-cli?branch=main)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/i386x/vutils-cli.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/i386x/vutils-cli/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/i386x/vutils-cli.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/i386x/vutils-cli/context:python)

# vutils-cli: Auxiliary Library for Writing CLI Applications

This package provides a set of tools for writing applications with command line
interface.

## Installation

To install `vutils-cli`, type
```sh
$ pip install vutils-cli
```

## How to Use

vutils-cli provides three mixins:
* `vutils.cli.application.ApplicationMixin` providing methods for launching the
  application code and error management;
* `vutils.cli.io.StreamsProxyMixin` providing methods for I/O streams
  manipulation;
* `vutils.cli.logging.LoggerMixin` providing methods for logging support.

Combined together, these three mixins form a base for creating command line
interface applications. User can make a subclass from each of mixins to reach
desired behavior. A simple application can be made in a way like this:
```python
from vutils.cli.application import ApplicationMixin
from vutils.cli.io import StreamsProxyMixin
from vutils.cli.logging import LoggerMixin


class CommandBase(ApplicationMixin, StreamsProxyMixin, LoggerMixin):

    def __init__(self):
        ApplicationMixin.__init__(self)
        StreamsProxyMixin.__init__(self)
        LoggerMixin.__init__(self)


class Application(CommandBase):

    def __init__(self):
        CommandBase.__init__(self)

    def main(self, argv):
        s = " ".join(argv)
        self.wout(f"{s}\n")
        return type(self).EXIT_SUCCESS


Application.start(__name__)
```

When the application starts, it prints its command line arguments to the
standard output. Methods provided by `ApplicationMixin` related to running the
application are:
* `main(self, argv)` provides the application entry point. The application
  logic should be placed into this method. This method is called from `run` and
  the value it returns is used as an application exit code. `argv` is an array
  containing command line arguments.
* `run(self, argv)` runs `main` and handles errors occurred inside `main`.
  Returns the exit code returned by `main` or by `ApplicationMixin.exit` or by
  `on_error` handler.
* `start(cls, modname="__main__")` runs the application. In greater detail, it
  calls the `run` method with `sys.argv` only if `modname` is equal to
  `"__main__"`.

In the example above, `CommandBase` has been introduced to indicate that it is
possible to use these three mixins also for implementing subcommands. This is
due no one of these three mixins has a global dependencies.

### Error Management

`ApplicationMixin` provides a set of methods for doing error management:
* `catch(self, exc)` register an exception `exc` that should be caught when it
  is raised inside `main`. If an exception raised inside `main` is not
  registered, the exception is not caught and it is propagated outside of
  `main`. `ApplicationError` from `vutils.cli.errors` is registered by default.
* `error(self, msg, ecode=1)` logs `msg` and calls `ApplicationMixin.exit` with
  `ecode`. To make logging work, `ApplicationMixin` must be used together with
  `LoggerMixin` (from `vutils.cli.logging`) and `StreamsProxyMixin` (from
  `vutils.cli.io`) mixins.
* `exit(self, ecode)` exits the application with the exit code `ecode`. Unlike
  `sys.exit`, it causes `on_exit` hook to be called, if `exit` has been invoked
  within `main`. If `exit` is called outside the `main`'s stack frame, the
  behavior is undefined.
* `on_exit(self, ecode)` is a hook which is called when `exit` has been invoked
  within `main`. `ecode` is the exit code given to `exit`. This method is
  dedicated to be overridden by a user. The default implementation logs the
  exit event, so to make it work properly `ApplicationMixin` must be used
  together with `LoggerMixin` and `StreamsProxyMixin` mixins.
* `on_error(self, exc)` is an exception handler to where a user can put his/her
  code to handle the caught exception `exc`. Everything registered by `catch`
  that comes from `main` is caught and passed as `exc` to this handler. The
  value returned by this handler is used as the application's exit code. The
  default implementation logs the `exc` and returns `EXIT_FAILURE`, thus the
  application must implement logging, at least by inheriting from `LoggerMixin`
  and `StreamsProxyMixin` mixins.

`ApplicationMixin` also provides two constants `EXIT_SUCCESS` and
`EXIT_FAILURE` which equals to 0 and 1, respectively.

User can make his/her custom errors by deriving from `ApplicationError` from
`vutils.cli.errors`. By implementing `detail` method, user can provide more
detail about his/her error.

### Input and Output Streams

Adding `StreamsProxyMixin` from `vutils.cli.io` to the list of base classes of
an application allow to use a set of methods for manipulating streams:
* `set_streams(self, ostream=None, estream=None)` set the output and error
  output streams. `None` means the original setting is left untouched. The
  default output and error output stream is `sys.stdout` and `sys.stderr`,
  respectively.
* `wout(self, text)` writes `text` to the output stream.
* `werr(self, text)` writes `text` to the error output stream.

`vutils.cli.io` provides also functions for colorizing the text, namely
`nocolor`, `red`, `green`, `blue`, `yellow`, and `brown`.

### Logging

As noted many times above, to support logging, use both `LoggerMixin` and
`StreamsProxyMixin` mixins together with `ApplicationMixin`:
```python
import pathlib

from vutils.cli.application import ApplicationMixin
from vutils.cli.io import StreamsProxyMixin
from vutils.cli.logging import LoggerMixin


class MyApp(ApplicationMixin, StreamsProxyMixin, LoggerMixin):

    def __init__(self):
        ApplicationMixin.__init__(self)
        StreamsProxyMixin.__init__(self)
        LoggerMixin.__init__(self)

    def main(self, argv):
        self.set_logger_props(logpath=pathlib.Path("/var/tmp/MyApp.log"))
        self.linfo("Hello from MyApp!\n")

        return ApplicationMixin.EXIT_SUCCESS
```

`LoggerMixin` extends `MyApp` about these methods:
* `set_logger_props(self, logpath=None, formatter=None, vlevel=None, dlevel=None)`
  allows to modify the logging facility properties. `logpath` sets the path of
  the log file, `formatter` sets the new formatter object (see `LogFormatter`),
  `vlevel` sets the verbosity level, and `dlevel` sets the debug level. The
  initial values of these properties given during the time of `LoggerMixin`
  initialization are `None` for `logpath`, `LogFormatter` instance for
  `formatter`, 1 for `vlevel`, and 0 for `dlevel`. A property is set only if a
  new value of the property is not `None`.
* `set_log_style(self, name, color)` sets the style of log messages (currently
  only color). `name` is the name of the type of log messages. The value should
  be one of the following constants provided by `LogFormatter`: `INFO`,
  `WARNING`, `ERROR`, and `DEBUG`. `color` is the color function, see
  `vutils.cli.io`. This method modifies directly the formatter object set by
  `set_logger_props`.
* `wlog(self, msg)` writes `msg` to the log file if it is set.
* Following methods write a message to the both error output stream and log
  file:
  * `linfo(self, msg, vlevel=1)`: if `vlevel` is less or equal to the verbosity
    level, issue `msg` as an info message.
  * `lwarn(self, msg)` issues `msg` as a warning message.
  * `lerror(self, msg)` issues `msg` as an error message.
  * `ldebug(self, msg, dlevel=1)`: if `dlevel` is less or equal to the debug
    level, issue `msg` as a debug message.

`vutils.cli.logging` provides also facility for formatting log messages,
`LogFormatter`. `LogFormatter` provides four constants to identify four
different types of log messages:
* `INFO` for info messages;
* `WARNING` for warning messages;
* `ERROR` for error messages;
* `DEBUG` for debug messages.

`LogFormatter.FORMAT` contains a format string used to format every message.
The format string is interpolated using `str.format` method and it recognizes
`label` for the message label and `message` for the message itself. Methods
provided by `LogFormatter` are:
* `set_style(self, name, color)` sets the style (currently only color) of log
  messages. `name` is the name of the message type and `color` is the message
  color. By default, `LogFormatter` prints `INFO` messages in blue, `WARNING`
  messages in yellow, `ERROR` messages in red, and `DEBUG` messages in brown.
* `colorize(self, name, msg, nocolor=False)` colorizes `msg` using the color
  associated with `name` by previous call of `set_style`. If `nocolor` is
  `True` or `name` has no color associated with it, `msg` is not colorized.
* `format(self, name, msg)` formats `msg` by interpolating `FORMAT` with
  uppercased `name` as `label` and `msg` as `message`. By overriding this
  method user can customize how log messages are formatted.
