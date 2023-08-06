# Using the Process Pool

As of version 3.1 of the platform, the Assembly SDK includes the classes `Pool` and `ResizablePool`, as well as the corresponding `pytest` fixtures `pool` and `rpool`. A good area to use these objects is testing and especially performance and throughput testing by issuing multiple requests to the tested component from multiple processes in parallel.

## Multiprocessing vs. Multithreading in Python

[This document](https://timber.io/blog/multiprocessing-vs-multithreading-in-python-what-you-need-to-know/) is one of many good descriptions of the differences between the two approaches. We decided to do multiprocessing because:

* we didn't want to be constrained by the Global Interpreter Lock (GIL)
* we didn't need the complexity of multithreading synchronization
* we needed to utilize the full potential of the system where the tests are running and have a true in-parallel calling from multiple processes to the tested API-s

However, multiprocessing introduces its own challenges. And the user of `Pool` or `ResizablePool` must have those in mind when constructing their tests.

1. Multiprocessing requires [_pickling_ and _un-pickling_](https://docs.python.org/2/library/pickle.html) (a.k.a. _marshaling_ and _un-marshaling_) of the **input arguments** (including `self`!), as well as the **return values**, because they must be serialized and transported via IPC (process also known as _marshaling_ or _pickling_) to another process. This implies that some process specific types of objects cannot be simply passed over, e.g. `requests.Session`, database connection, etc.

   > For instance the contract tests almost always make heavy use of the `network` fixture which returns a ready to use `NetworkClient` object. This object encapsulates a `NodeClient` instance and this in turn has a member of type `requests.Session` which is not pickle-able. So, we had to add the standard pickle/un-pickle helpers  `__getstate__`/`__setstate__` methods to `assembly_client.api.node_client.NodeSession`.

2. All arguments are ***passed by value*** to the functions executed on the process pool. In other words, the caller cannot expect any side effects: if the function changes something in one or more of the input arguments, the caller cannot expect to see these changes after the call - they are not marshaled back. The common solution to this would be to include the changed parameters in the return value:

    ```python
    def foo(obj: dict) -> dict:
        ...
        obj['bar'] = 42
        return obj

    result = None
    with Pool() as pool:
        arg = {'bar': 7, 'tar': 34}
        result = pool.add(foo, arg).execute()

    assert arg['bar'] == 7
    assert result['bar'] == 42
    ```

## Implementation

In Python `multiprocessing` is the "standard" multi-threading and multi-processing library. The popular `multiprocessing.pathos` package makes `multi-processing` simpler to use. We leveraged `multiprocessing.pathos` in the implementation of the `Pool` and `ResizablePool` classes.

## `Pool`

The class `Pool` encapsulates a pool of processes (as provided by [Pathos](https://pathos.readthedocs.io/en/latest/pathos.html) and `multi-processing`).

---

### `Pool()` constructor (`__init__`)

The objects of this class are instantiated by invoking the constructor with two optional parameters.

* Parameters

  * `nprocs: int` - specifies the number of processes in the pool.

    The default is the number of CPU cores on the current system.

  * `local: bool` - specifies that the pool will be used with the _local mock network_.

    The local mock network is **NOT** a multi-process/multi-thread safe entity and therefore cannot be called from within the process pool. Instead, the `Pool` object simply runs all _actions_ in a serial fashion - one by one on the main thread. One can say that the flag `local` forces **emulation** of a real process pool.

    Because of this pool emulation inside the main Python thread, this parameter can be also used to debug functions executed on the pool (a.k.a. _the actions_). Debugging a function running in another process can be hard, but if you set the `local` flag to `True`, you force execution in the same process and then debugging is trivial. However, remember that debugging actions in the same process, that are otherwise meant to be run on a process pool, may lead to obscuring problems with pickling and un-pickling of arguments and return values.

    The default is `False`.

  See also the custom `pytest` parameters `--pool-nprocs` and `--pool-debug` used by the fixtures `pool` and `rpool` described below.

* Example

  ```python
  pool = Pool()               # creates a process pool with
                              # `multiprocessing.cpu_count()` number of processes
  assert pool.size == multiprocessing.cpu_count()

  pool4 = Pool(4)             # creates a pool with 4 processes

  assert pool4.size == 4

  local = sdk_args.network_config is None or
          sdk_args.pool_debug

  local_pool8 = Pool(8, local)  # if local is True
                                # will "SIMULATE" a process pool with 8 processes

  assert local_pool8.size == 8
  assert local_pool8.local == sdk_args.network_config is None or
                              sdk_args.pool_debug
  ```

---

### `size` property

Gets the number of processes in the pool.

```python
pool = Pool(4)

assert pool.size == 4
```

---

### `run()` method

The `run` method accepts one parameter-less function; or a list-like object (i.e. `list`, `tuple`, `set`) of parameter-less functions. It will execute each of them in a separate process from the pool and will wait for all of them to finish, i.e. the call to `run()` is _synchronous_.

* Parameters

  * `actions` - the parameter must be a single callable or list-like object of callable objects (e.g. functions).

* Return value

    The value or a `list` of the values that were returned by executing the parameter(s) `actions`.

* Example

  ```python
  actions = [
      lambda: foo(a, b, c),
      lambda: bar(x, y, z)]
  results = pool.run(actions)
  for result in results: ...
  ```

---

### `add()` method

The `add` and `execute` (see below) methods were introduced as an arguably easier to use alternative of `run()`. A series of subsequent `add()` calls creates an array of parameter-less functions and the invoking `execute()` executes them on the process pool. One may say that a series of `add()`-s and an `execute()` are _syntactic sugar_ for `run()`

* Parameters
  * `action` - a callable.
  * `*args` - list of positional arguments to `action`.
  * `**kwargs` - a dictionary of named arguments to `action`.

* Return value

  Returns the pool object itself, so that the subsequent calls to `add` and the final call to `execute` can be _chained_.

* Example

  ```python
  pool = Pool()
  ...
  results = pool.add(action1, arg1, arg2, named=arg3)
                .add(function2, arg0)
                .add(method3, foo=bar)
                .execute()

  for result in results: ...
  ```

---

### `execute()` method

Synchronously executes the call-ables stored by the previous calls to the `add` function.

* Parameters

  None.

* Return value

  If there was a single call to `add`, `execute` will return a single value - the result of the execution of the added single action. If there were two or more calls to `add`, `execute` will return a list of the return values.

* __Note:__ once `execute`-d, the added functions are removed from the object and cannot be `execute`-d a second time.

* Example

  ```python
  pool = Pool()

  ...
  results = pool.add(action1, arg1, arg2, named=arg3)
                .add(function2, arg0)
                .add(method3, foo=bar)
                .execute()

  for result in results: ...
  ```

---

### `map()` method

The `map` method is useful when you want to test calling multiple instances of the same function with different sets of parameters from different processes.

* Parameters
  * `action` - the function to be executed on the pool
  * `*args` - a list-like of list-like objects (matrix) of arguments. All inner list-like items **must be of the same length**, equal to the number of calls that you want to put on the pool. Also the elements of the inner list-like items **must be of the same type** - the type of the corresponding parameter in `action`.
  * ___Note___:
    1. the `action` must have at least 1 parameter
    1. `map` does NOT accept `**kwargs`

* Return value

  Executes synchronously and returns a list of the return values from each invocation.

* Example

  ```python
  def foo(a: int, b: str, c: bool) -> str:
      ...
      return result

  results = pool.map(foo, [1, 2, 3], ["a", "b", "c"], [True, False, True])

  # the above is equivalent to:
  # results = pool.run(lambda: foo(1, "a", True),
  #                    lambda: foo(2, "b", False),
  #                    lambda: foo(3, "c", True))

  # or equivalent to:
  # results = pool.add(foo, 1, "a", True)
  #               .add(foo, 2, "b", False)
  #               .add(foo, 3, "c", True)
  #               .execute()

  for result in results: ...
  ```

  In the above example the method `foo` will be executed in three different processes in parallel:

  * `foo(1, "a", True)`
  * `foo(2, "b", False)`
  * `foo(3, "c", True)`

  The result `res_list` will be an array of 3 strings.

  If your logic arranges the arguments in array of calling argument sets, e.g. `[1, "a", True], ...` you can use the static function `transpose` to transpose the input matrix of arguments to the required form:

  ```python
  results = pool.map(foo, *pool.transpose([1, "a", True], [2, "b", False], [3, "c", True]))
  ```

  ___Notes:___

  1. If your function takes only one parameter, the set still must be enclosed in a list-like object, e.g.

      ```python
      def bar(a: int) -> str:
        ...
        return result

      results = pool.map(bar, [1, 2, 42])
      # equivalent to:
      # results = pool.run(lambda: bar(1),
      #                    lambda: bar(2),
      #                    lambda: bar(42))
      # or:
      # results = pool.add(bar, 1)
      #               .add(bar, 2)
      #               .add(bar, 42)
      #               .execute()

      for result in results: ...
      ```

  2. If you'd like to call a single instance of a function that takes one or more parameters on the process pool, you still need to enclose each parameter in one-item arrays:

      ```python
      def baz(q: int, b: int, c: bool) -> str:
        ...
        return result

      results = pool.map(baz, [42], ["don't panic"], [False])
      # equivalent to:
      # results = pool.run(lambda: baz(42, "don't panic", False))
      # or:
      # results = pool.add(baz, 42, "don't panic", False).execute()

      for result in results: ...
      ```

---

### `transpose()` method

Transposes a list-like of equal size list-likes (a matrix) of values. E.g.

```python
# from the original shape [1, "a", True],
#                         [2, "b", False],
#                         [3, "c", True],
#                         [4, "d", False]

transposed = pool.transpose([1, "a", True], [2, "b", False], [3, "c", True], [4, "d", False])

# will produce the new transposed matrix [[1,    2,     3,    4],
#                                         ["a",  "b",   "c",  "d"],
#                                         [True, False, True, False]]
```

This function is intended for use in conjunction with `Pool.map()`:

```python
    res_list = pool.map(foo, *pool.transpose([1, "a", True], [2, "b", False], [3, "c", True]))
```

* Parameters

  `*args` : list-like of list-likes (a matrix) of values. All internal list-likes must be equal size

---

### `clear()` method

Destroys the process pool.

___Note:___ the pool class implements the methods `__enter__` and `__exit__`, so it can be used from within the python scope definition statement `with`. In this case, since `__exit__` calls `clear()` you do not need to call it explicitly, e.g.

```python
def bar(a: str) -> str:
    ...
    return result

results = None
with Pool() as pool:
    results = pool.map(bar, ["aaa", "bbb", "ccc"])

for result in results: ...
```

---

## `ResizablePool`

The class `ResizablePool` inherits from `Pool` and extends it by providing the `size` property ___setter___ for resizing the pool, i.e. changing the number of processes in the process pool.

---

### `ResizablePool()` constructor (`__init__`)

The objects of this class are instantiated by invoking the constructor with two optional parameters.

* Parameters

  * `nprocs: int` - specifies the number of processes in the pool.

    The default is the number of CPU cores on the current system.

  * `local: bool` - specifies that the pool will be used with the _local mock network_.

    Default `False`.

---

* `size` property

  Gets or **sets** the number of processes in the pool. Useful for scalability and multi-process tests to observe the effects of parallel calls to the tested object.

  ```python
  pool = ResizablePool(4)

  assert pool.size == 4

  pool.size = 8

  assert pool.size == 8
  ```

---

## `pytest` fixtures

### `pool`

Returns a ready to use `Pool` object. The fixture has a **`session`** scope so that after the test session finishes, the fixture destroys the pool automatically. The size of the pool can be parameterized with the custom `pytest` parameter `--pool-nprocs`.

To debug the functions which normally run on the process pool (a.k.a. _actions_) use the custom `pytest` paramater `--pool-debug`.

### `rpool`

The same as `pool` but returns a ready to use `ResizablePool` object that can be resized dynamically instead. The object returned by `rpool` also can be parameterized with the custom `pytest` parameters `--pool-nprocs` and `--pool-debug`.

**NOTE: Use the parameter `--pool-debug` only for debugging actions!**
