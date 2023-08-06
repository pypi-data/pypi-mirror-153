import inspect
from multiprocessing import cpu_count
import pathos.multiprocessing as mp


class Pool:
    """
    Encapsulates a pool of processes. A thin convenience wrapper over the process pool from the package
    `pathos.multiprocessing`.
    """

    class MockResult:
        """
        Thin wrapper over the result from a `local`, single-processing operation. Implements the interface for
        obtaining the result - see `pathos.multiprocessing.ProcessPool.get()`
        """

        def __init__(self, result):
            self._result = result

        def get(self):
            return self._result

    # noinspection PyBroadException
    @staticmethod
    def _is_iterable(value) -> bool:
        try:
            _ = iter(value)
            return True
        except:  # noqa: E722
            return False

    # noinspection PyBroadException

    def __init__(self, nprocs=0, local=False):
        """
        Parameters
        ----------
        nprocs : int
            the number of processes in the pool. Default: the number of CPU=s on the machine.
        local : bool
            If `True` doesn't create a pool and uses the current process to map the action(s) to. Default: `False`.
            See also `Pool.run()`.
        """
        self._pool = None
        self._lambdas = None
        self._local = local
        self._nprocs = nprocs
        if self._nprocs < 1:
            self._nprocs = cpu_count()

        if not self._local:
            self._pool = mp.ProcessPool(nodes=self._nprocs)

    @property
    def size(self):
        """Gets the size of the pool, i.e. the number of processes in it."""
        return self._nprocs

    @property
    def local(self):
        """If the pool is local returns `True`, otherwise `False`."""
        return self._local

    def _run(self, action):
        if self.local:
            return Pool.MockResult(action())

        return self._pool.apipe(action)

    def _map(self, action, *args):
        if self.local:
            transposed_args = self.transpose(*args)
            return [action(*targs) for targs in transposed_args]

        return self._pool.map(action, *args)

    def run(self, actions):
        """
        Sends one or more different actions to the processes in the pool.

        Parameters
        ----------
        actions : `callable`, or `iterable` of `callable`-s. The action(s) to send to the processes in the pool. Note
            that there is no way to provide parameters to the `actions`. If you need to pass parameters you could use
            simple lambda functions that wrap the call with the parameters, e.g.
            ```
                actions = [
                    lambda: foo(a, b, c),
                    lambda: bar(x, y, z)
                ]
                pool.run(actions)
            ```

        Returns
        -------
        Object or a `list` of objects - result(s) of the completed action(s).
        """
        single = False
        if not Pool._is_iterable(actions):
            single = True
            actions = [actions]

        results = [r.get() for r in [self._run(a) for a in actions]]
        if single:
            return results[0]

        return results

    def add(self, action, *args, **kwargs):
        """
        Internally stores a new pointer to function to be executed on the process pool upon `Pool.execute`.
        ```
            pool = Pool()
            ...
            results = pool
                .add(action1, arg1, arg2, named=arg3)
                .add(function2, arg0)
                .add(method3, foo=bar)
                .execute()
        ```

        Parameters:
        -----------
        action : `callable` pointer to a function to be executed later by the function `Pool.execute()`
        *args : a list of positional arguments to be passed to the `action` parameter upon `Pool.execute()`
        **kwargs : named parameters to be passed to the `action` parameter upon  `Pool.execute()`

        Return:
        -------
        The function returns the current `Pool` instance, so that the `add`-s and the `execute` can be chained in one
        statement.
        """
        if self._lambdas is None:
            self._lambdas = []
        self._lambdas.append(lambda: action(*args, **kwargs))
        return self

    def execute(self):
        """
        Synchronously executes the functions stored by the calls to the function `Pool.add()` on the process pool. After
        execution the added functions are removed and new ones can be `add`-ed.

        Return:
        -------
        A list of results from the execution of the previously `add`-ed functions.
        """
        if not self._lambdas:
            raise RuntimeError("Nothing to execute. Use Pool.add() first.")
        result = self.run(self._lambdas)
        self._lambdas = None
        return result

    def map(self, action, *args):
        """
        Synchronously executes a single method `action` with different sets of arguments on the process pool in
        parallel.

        The caller is supposed to pass a list for each argument of `action`. All lists should be equal size and the
        items in the arrays should be the same type, e.g.
        ```
            def foo(a: int, b: str, c: bool) -> str:
                ...
                return result

            res_list = pool.map(foo, [1, 2, 3], ["a", "b", "c"], [True, False, True])
        ```
        In the above example the method `foo` will be executed in three different processes in parallel:
        * `foo(1, "a", True)`
        * `foo(2, "b", False)`
        * `foo(3, "c", True)`
        The result `res_list` will be an array of 3 strings.

        If your logic arranges the arguments in array of calling argument sets, e.g. `[[1, "a", True], ...]` you can
        use the static function transpose:
        ```
            res_list = pool.map(foo, *pool.transpose([1, "a", True], [2, "b", False], [3, "c", True]))
        ```
        See also `pool.transpose()`.

        Parameters:
        -----------
        action : `callable`. The function to be executed.
        *args : `iterable` of arrays of parameters

        Returns:
        --------
        An array of results from the executed functions.
        """
        Pool._check_arg_matrix(*args)
        return self._map(action, *args)

    @staticmethod
    def _check_arg_matrix(*args) -> int:
        def _args_matrix_error_msg() -> str:
            return (
                "The `{}` function must be passed a non-empty list or tuple of arguments "
                "which are non-empty lists or tuples of equal lengths."
            ).format(inspect.stack()[2][3])

        if len(args) == 0:
            raise ValueError(_args_matrix_error_msg())

        t0 = type(args[0])
        if t0 is not list and t0 is not tuple:
            raise ValueError(_args_matrix_error_msg())

        len0 = len(args[0])
        if len0 == 0:
            raise ValueError(_args_matrix_error_msg())

        for arg in args[1:]:
            if type(arg) is not list and type(arg) is not tuple or len(arg) != len0:
                raise ValueError(_args_matrix_error_msg())

    def transpose(self, *args):
        """
        Transposes a list of equal size lists (matrix) of values. E.g.
        ```
            # original shape
            pool.transpose([1, "a", True], [2, "b", False], [3, "c", True], [4, "d", False])
            # will produce the new matrix:
            [[1, 2, 3, 4], ["a", "b", "c", "d"], [True, False, True, False]]
        ```
        Can be used in conjuction with `Pool.map()`:
        ```
            res_list = pool.map(foo, *pool.transpose([1, "a", True], [2, "b", False], [3, "c", True]))
        ```

        Parameters:
        -----------
        *args : array of arrays (matrix) of values

        Return:
        -------
        The transposed input matrix.
        """
        Pool._check_arg_matrix(*args)
        return [[row[i] for row in args] for i in range(len(args[0]))]

    def clear(self):
        """
        Closes the underlying process pool.

        Note:
            After closing the pool you cannot call `run()` or `map()` unless you first set a new `size` of the pool.
        """
        self._lambdas = None
        if self._pool:
            # this may look silly but I see the Pathos author doing it in many of his examples... ¯\_(ツ)_/¯
            self._pool.close()
            self._pool.join()
            self._pool.clear()
            self._pool = None

    # region Scope defining helpers used by the `with` statement
    def __enter__(self):
        """
        Along with `__exit__` makes the current object also a context manager of itself and can be used in a python
        `with` statement.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Along with `__enter__` makes the current object also a context manager of itself and can be used in a python
        `with` statement.
        """
        self.clear()

    # endregion


class ResizablePool(Pool):
    """
    The same as `Pool` but allows for dynamic resizing of the underlying pool of processes using the property setter
    `size`.
    """

    def __init__(self, nprocs=0, local=False):
        """
        Parameters
        ----------
        nprocs : int
            the initial number of processes in the pool. Default: the number of CPU=s on the machine. See also the
            `Pool.size` property.
        local : bool
            If `True` doesn't create a pool and uses the current process to map the action(s) to. Default: `False`.
            See also `Pool.run()`.
        """
        super().__init__(nprocs, local)

    @property
    def local(self):
        """If the pool is local returns `True`, otherwise `False`."""
        return self._local

    # region Property `size` getter and setter
    @property
    def size(self):
        """Gets the size of the pool, i.e. the number of processes in it."""
        return self._nprocs

    @size.setter
    def size(self, value):
        """
        Gets or sets the size of the pool, i.e. the number of processes in it.

        Caution:
            Setting of the property causes the object to first close the current underlying pool (if any) and then
            creates a new one with the specified size `value`. Hence, this is expensive and time consuming operation.

        Parameters
        ----------
        value : int
            The new size of the pool
        """
        current_nprocs = self._nprocs

        self._nprocs = value
        if self._nprocs < 1:
            self._nprocs = cpu_count()

        # if didn't resize - do nothing
        if current_nprocs == self._nprocs:
            return

        # recreate the pool
        self.clear()
        if not self.local:
            self._pool = mp.ProcessPool(nodes=self._nprocs)

        # endregion
