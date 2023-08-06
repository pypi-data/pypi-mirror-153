Queue functions for execution later in priority and time order.

*Latest release 20220605*:
* Later: replace the default = _ThreadLocal with a default = ThreadState(current=None).
* Later: fold startup/shutdown/__enter__/__exit__ into the startup_shutdown context manager, fixes MultiOpenMixin misbehaviour.

I use `Later` objects for convenient queuing of functions whose
execution occurs later in a priority order with capacity constraints.

Why not futures?
I already had this before futures came out,
I prefer its naming scheme and interface,
and futures did not then support prioritised execution.

Use is simple enough: create a `Later` instance and typically queue
functions with the `.defer()` method::

    L = Later(4)      # a Later with a parallelism of 4
    ...
    LF = L.defer(func, *args, **kwargs)
    ...
    x = LF()          # collect result

The `.defer` method and its siblings return a `LateFunction`,
which is a subclass of `cs.result.Result`.
As such it is a callable,
so to collect the result you just call the `LateFunction`.

## Function `defer(func, *a, **kw)`

Queue a function using the current default Later.
Return the `LateFunction`.

## Class `LateFunction(cs.result.Result)`

State information about a pending function,
a subclass of `cs.result.Result`.

A `LateFunction` is callable,
so a synchronous call can be done like this:

    def func():
      return 3
    L = Later(4)
    LF = L.defer(func)
    x = LF()
    print(x)        # prints 3

Used this way, if the called function raises an exception it is visible:

    LF = L.defer()
    try:
      x = LF()
    except SomeException as e:
      # handle the exception ...

To avoid handling exceptions with try/except the .wait()
method should be used:

    LF = L.defer()
    x, exc_info = LF.wait()
    if exc_info:
      # handle exception
      exc_type, exc_value, exc_traceback = exc_info
      ...
    else:
      # use `x`, the function result

TODO: .cancel(), timeout for wait().

*Method `LateFunction.__init__(self, func, name=None, retry_delay=None)`*:
Initialise a `LateFunction`.

Parameters:
* `func` is the callable for later execution.
* `name`, if supplied, specifies an identifying name for the `LateFunction`.
* `retry_local`: time delay before retry of this function on RetryError.
  Default from `later.retry_delay`.

*Method `LateFunction.wait(*args, **kwargs)`*:
OBSOLETE FUNCTION wait

Obsolete name for `.join`.

## Class `LatePool`

A context manager after the style of subprocess.Pool
but with deferred completion.

Example usage:

    L = Later(4)    # a 4 thread Later
    with LatePool(L) as LP:
      # several calls to LatePool.defer, perhaps looped
      LP.defer(func, *args, **kwargs)
      LP.defer(func, *args, **kwargs)
    # now we can LP.join() to block for all `LateFunctions`
    #
    # or iterate over LP to collect `LateFunction`s as they complete
    for LF in LP:
      result = LF()
      print(result)

*Method `LatePool.__init__(self, L=None, priority=None, delay=None, when=None, pfx=None, block=False)`*:
Initialise the `LatePool`.

Parameters:
* `L`: `Later` instance, default from default.current.
* `priority`, `delay`, `when`, `name`, `pfx`:
  default values passed to Later.submit.
* `block`: if true, wait for `LateFunction` completion
  before leaving __exit__.

*Method `LatePool.__enter__(self)`*:
Entry handler: submit a placeholder function to the queue,
acquire the "commence" lock, which will be made available
when the placeholder gets to run.

*Method `LatePool.__exit__(self, exc_type, exc_val, exc_tb)`*:
Exit handler.
If .block is true, wait for `LateFunction` completion before return.

*Method `LatePool.__iter__(self)`*:
Report completion of the `LateFunction`s.

*Method `LatePool.add(self, LF)`*:
Add a `LateFunction` to those to be tracked by this LatePool.

*Method `LatePool.defer(self, func, *a, **kw)`*:
Defer a function using the LatePool's default parameters.

*Method `LatePool.join(self)`*:
Wait for completion of all the `LateFunction`s.

*Method `LatePool.submit(self, func, **params)`*:
Submit a function using the LatePool's default parameters, overridden by `params`.

## Class `Later(cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin)`

A management class to queue function calls for later execution.

Methods are provided for submitting functions to run ASAP or
after a delay or after other pending functions. These methods
return `LateFunction`s, a subclass of `cs.result.Result`.

A Later instance' close method closes the Later for further
submission.
Shutdown does not imply that all submitted functions have
completed or even been dispatched.
Callers may wait for completion and optionally cancel functions.

TODO: __enter__ returns a SubLater, __exit__ closes the SubLater.

TODO: drop global default Later.

*Method `Later.__init__(self, capacity, name=None, inboundCapacity=0, retry_delay=None)`*:
Initialise the Later instance.

Parameters:
* `capacity`: resource contraint on this Later; if an int, it is used
  to size a Semaphore to constrain the number of dispatched functions
  which may be in play at a time; if not an int it is presumed to be a
  suitable Semaphore-like object, perhaps shared with other subsystems.
* `name`: optional identifying name for this instance.
* `inboundCapacity`: if >0, used as a limit on the number of
  undispatched functions that may be queued up; the default is 0 (no
  limit).  Calls to submit functions when the inbound limit is reached
  block until some functions are dispatched.
* `retry_delay`: time delay for requeued functions.
  Default: `DEFAULT_RETRY_DELAY`.

*Method `Later.__call__(self, func, *a, **kw)`*:
A Later object can be called with a function and arguments
with the effect of deferring the function and waiting for
it to complete, returning its return value.

Example:

  def f(a):
    return a*2
  x = L(f, 3)   # x == 6

*Method `Later.after(self, LFs, R, func, *a, **kw)`*:
Queue the function `func` for later dispatch after completion of `LFs`.
Return a `Result` for collection of the result of `func`.

This function will not be submitted until completion of
the supplied `LateFunction`s `LFs`.
If `R` is `None` a new `Result` is allocated to
accept the function return value.
After `func` completes, its return value is passed to `R.put()`.

Typical use case is as follows: suppose you're submitting
work via this `Later` object, and a submitted function itself
might submit more `LateFunction`s for which it must wait.
Code like this:

      def f():
        LF = L.defer(something)
        return LF()

may deadlock if the Later is at capacity. The `after()` method
addresses this:

      def f():
        LF1 = L.defer(something)
        LF2 = L.defer(somethingelse)
        R = L.after( [LF1, LF2], None, when_done )
        return R

This submits the `when_done()` function after the LFs have
completed without spawning a thread or using the `Later`'s
capacity.

See the retry method for a convenience method that uses the
above pattern in a repeating style.

*Method `Later.bg(self, func, *a, **kw)`*:
Queue a function to run right now,
ignoring the `Later`'s capacity and priority system.

This is really just an easy way to utilise the `Later`'s thread pool
and get back a handy `LateFunction` for result collection.
Frankly, you're probably better off using `cs.result.bg` instead.

It can be useful for transient control functions that themselves
queue things through the `Later` queuing system but do not want to
consume capacity themselves, thus avoiding deadlock at the cost of
transient overthreading.

The premise here is that the capacity limit
is more about managing compute contention than pure `Thread` count,
and that control functions should arrange other subfunctions
and then block or exit,
thus consuming neglible compute.
It is common to want to dispatch a higher order operation
via such a control function,
but that higher order would itself normally consume some
of the capacity
thus requiring an an hoc increase to the required capacity
to avoid deadlock.

*Method `Later.complete(self, outstanding=None, until_idle=False)`*:
Generator which waits for outstanding functions to complete and yields them.

Parameters:
* `outstanding`: if not None, an iterable of `LateFunction`s;
  default `self.outstanding`.
* `until_idle`: if true,
  continue until `self.outstanding` is empty.
  This requires the `outstanding` parameter to be `None`.

*Method `Later.debug(self, *a, **kw)`*:
Issue a debug message with `later_name` in `'extra'`.

*Method `Later.defer(self, func, *a, **kw)`*:
Queue the function `func` for later dispatch using the
default priority with the specified arguments `*a` and `**kw`.
Return the corresponding `LateFunction` for result collection.

`func` may optionally be preceeded by one or both of:
* a string specifying the function's descriptive name,
* a mapping containing parameters for `priority`,
  `delay`, and `when`.

Equivalent to:

    submit(functools.partial(func, *a, **kw), **params)

*Method `Later.defer_iterable(self, it, outQ, test_ready=None)`*:
Submit an iterable `it` for asynchronous stepwise iteration
to return results via the queue `outQ`.
Return a `Result` for final synchronisation.

Parameters:
* `it`: the iterable for for asynchronous stepwise iteration
* `outQ`: an `IterableQueue`like object
  with a `.put` method to accept items
  and a `.close` method to indicate the end of items.
  When the iteration is complete,
  call `outQ.close()` and complete the `Result`.
  If iteration ran to completion then the `Result`'s `.result`
  will be the number of iterations, otherwise if an iteration
  raised an exception the the `Result`'s .exc_info will contain
  the exception information.
* `test_ready`: if not `None`, a callable to test if iteration
  is presently permitted; iteration will be deferred until
  the callable returns a true value.

*Method `Later.error(self, *a, **kw)`*:
Issue an error message with `later_name` in `'extra'`.

*Property `Later.finished`*:
Probe the finishedness.

*Method `Later.info(self, *a, **kw)`*:
Issue an info message with `later_name` in `'extra'`.

*Method `Later.logTo(self, filename, logger=None, log_level=None)`*:
Log to the file specified by `filename` using the specified
logger named `logger` (default the module name, cs.later) at the
specified log level `log_level` (default logging.INFO).

*Method `Later.log_status(self)`*:
Log the current delayed, pending and running state.

*Method `Later.pool(self, *a, **kw)`*:
Return a `LatePool` to manage some tasks run with this `Later`.

*Method `Later.priority(self, pri)`*:
A context manager to temporarily set the default priority.

Example:

    L = Later(4)
    with L.priority(1):
      L.defer(f)  # queue f() with priority 1
    with L.priority(2):
      L.defer(f, 3)  # queue f(3) with priority 2

WARNING: this is NOT thread safe!

TODO: is a thread safe version even a sane idea without a
      per-thread priority stack?

*Method `Later.ready(self, **kwargs)`*:
Awful name.
Return a context manager to block until the Later provides a timeslot.

*Method `Later.state(self, new_state, *a)`*:
Update the state of this Later.

*Method `Later.submit(self, func, priority=None, delay=None, when=None, name=None, pfx=None)`*:
Submit the callable `func` for later dispatch.
Return the corresponding `LateFunction` for result collection.

If the parameter `priority` is not None then use it as the priority
otherwise use the default priority.

If the parameter `delay` is not None, delay consideration of
this function until `delay` seconds from now.

If the parameter `when` is not None, delay consideration of
this function until the time `when`.
It is an error to specify both `when` and `delay`.

If the parameter `name` is not None, use it to name the `LateFunction`.

If the parameter `pfx` is not None, submit pfx.partial(func);
  see the cs.logutils.Pfx.partial method for details.

If the parameter `LF` is not None, construct a new `LateFunction` to
  track function completion.

*Property `Later.submittable`*:
May new tasks be submitted?
This normally tracks "not self.closed", but running tasks
are wrapped in a thread local override to permit them to
submit further related tasks.

*Method `Later.wait(self)`*:
Wait for the Later to be finished.

*Method `Later.wait_outstanding(self, until_idle=False)`*:
Wrapper for complete(), to collect and discard completed `LateFunction`s.

*Method `Later.warning(self, *a, **kw)`*:
Issue a warning message with `later_name` in `'extra'`.

*Method `Later.with_result_of(self, callable1, func, *a, **kw)`*:
Defer `callable1`, then append its result to the arguments for
`func` and defer `func`.
Return the `LateFunction` for `func`.

## Function `retry(retry_interval, func, *a, **kw)`

Call the callable `func` with the supplied arguments.

If it raises `RetryError`,
run `time.sleep(retry_interval)`
and then call again until it does not raise `RetryError`.

## Class `RetryError(builtins.Exception, builtins.BaseException)`

Exception raised by functions which should be resubmitted to the queue.

## Class `SubLater`

A class for managing a group of deferred tasks using an existing `Later`.

*Method `SubLater.__init__(self, L)`*:
Initialise the `SubLater` with its parent `Later`.

TODO: accept `discard=False` param to suppress the queue and
associated checks.

*Method `SubLater.__iter__(self)`*:
Iteration over the `SubLater`
iterates over the queue of completed `LateFUnction`s.

*Method `SubLater.close(self)`*:
Close the SubLater.

This prevents further deferrals.

*Method `SubLater.defer(self, func, *a, **kw)`*:
Defer a function, return its `LateFunction`.

The resulting `LateFunction` will queue itself for collection
on completion.

*Method `SubLater.reaper(self, handler=None)`*:
Dispatch a `Thread` to collect completed `LateFunction`s.
Return the `Thread`.

`handler`: an optional callable to be passed each `LateFunction`
as it completes.

# Release Log



*Release 20220605*:
* Later: replace the default = _ThreadLocal with a default = ThreadState(current=None).
* Later: fold startup/shutdown/__enter__/__exit__ into the startup_shutdown context manager, fixes MultiOpenMixin misbehaviour.

*Release 20201021*:
* Later: subclass MultiOpenMixin.
* Later._defer: make a shallow copy of the keyword parameters as we do for the positional parameters.

*Release 20191007*:
Drop pipeline functionality, moved to new cs.pipeline module.

*Release 20181231*:
* New SubLater class to provide a grouping for deferred functions and an iteration to collect them as they complete.
* Drop WorkerThreadPool (leaks idle Threads, brings little benefit).
* Later: drop worker queue thread and semaphore, just try a dispatch on submit or complete.
* Later: drop tracking code. Drop capacity context manager, never used.

*Release 20181109*:
* Updates for cs.asynchron renamed to cs.result.
* Later: no longer subclass MultiOpenMixin, users now call close to end submission, shutdown to terminate activity and wait to await finalisation.
* Clean lint, add docstrings, minor bugfixes.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* Add LatePool, a context manager after the flavour of subprocess.Pool.
* Python 2 fix.
* Rename NestingOpenCloseMixin to MultiOpenMixin - easier to type, say and remember, not to mention being more accurate.
* Add RetryError exception for use by Later.retriable.
* LateFunction: support RetryError exception from function, causing requeue.
* LateFunction: accept retry_delay parameter, used to delay function retry.
* Later.defer_iterable: accept `test_ready` callable to support deferring iteration until the callable returns truthiness.
* New function retry(retry_interval, func, *a, **kw) to call func until it does not raise RetryError.
* Later: wrap several methods in @MultiOpenMixin.is_opened.
* Assorted bugfixes and improvements.

*Release 20150115*:
First PyPI release.
