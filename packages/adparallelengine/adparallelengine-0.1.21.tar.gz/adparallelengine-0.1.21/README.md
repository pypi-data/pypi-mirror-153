[![doc](https://img.shields.io/badge/-Documentation-blue)](https://advestis.github.io/adparallelengine)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### Status
[![pytests](https://github.com/Advestis/adparallelengine/actions/workflows/pull-request.yml/badge.svg)](https://github.com/Advestis/adparallelengine/actions/workflows/pull-request.yml)
[![push-pypi](https://github.com/Advestis/adparallelengine/actions/workflows/push-pypi.yml/badge.svg)](https://github.com/Advestis/adparallelengine/actions/workflows/push-pypi.yml)
[![push-doc](https://github.com/Advestis/adparallelengine/actions/workflows/push-doc.yml/badge.svg)](https://github.com/Advestis/adparallelengine/actions/workflows/push-doc.yml)

![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
[![issues](https://img.shields.io/github/issues/Advestis/adparallelengine.svg)](https://github.com/Advestis/adparallelengine/issues)
[![pr](https://img.shields.io/github/issues-pr/Advestis/adparallelengine.svg)](https://github.com/Advestis/adparallelengine/pulls)


#### Compatibilities
![ubuntu](https://img.shields.io/badge/Ubuntu-supported--tested-success)
![unix](https://img.shields.io/badge/Other%20Unix-supported--untested-yellow)

![python](https://img.shields.io/pypi/pyversions/adparallelengine)


##### Contact
[![linkedin](https://img.shields.io/badge/LinkedIn-Advestis-blue)](https://www.linkedin.com/company/advestis/)
[![website](https://img.shields.io/badge/website-Advestis.com-blue)](https://www.advestis.com/)
[![mail](https://img.shields.io/badge/mail-maintainers-blue)](mailto:pythondev@advestis.com)

# adparallelengine

A wrapper around several ways of doing map multiprocessing in Python. One can use :
* Dask
* concurrent.futures
* mpi4py.futures
The underlying engine is also available in a serial mode, for debugging purposes 

## Installation

```
pip install adparallelengine[all,mpi,dask,support_shared,k8s]
```

## Usage

### Basic use

Creating the engine is done this way:

```python
from adparallelengine import Engine
from transparentpath import Path

if __name__ == "__main__":
    which = "multiproc"  # Can also be "serial", "dask", "mpi" or "k8s"
    engine = Engine(kind=which, path_shared=Path("tests") / "data" / "shared")
```

Then using the engine is done this way:
```python
from adparallelengine import Engine
import pandas as pd
from transparentpath import Path

def method(df):
    return 2 * df, 3 * df

if __name__ == "__main__":
    which = "multiproc"  # Can also be "serial", "dask", "mpi" or "k8s"
    engine = Engine(
        kind=which,
        # max_workers=10  One can limit the number of workers. By default, os.cpu_count() or MPI.COMM_WORLD.size is used
    )
    results = engine(
        method,  # The method to use...
        [pd.DataFrame([[1, 2]]), pd.DataFrame([[3, 4]]), pd.DataFrame([[5, 6]])]  # ...on each element of this iterable 
    )
```

### Gathering

Results will be a list of tuples, each containing two dataframes, because `method` returns a tuple of two dataframes.
One could have used the keyword "gather" to flatten this list inside the engine :

```python
    results = engine(method, [pd.DataFrame([[1, 2]]), pd.DataFrame([[3, 4]]), pd.DataFrame([[5, 6]])], gather=True)
```

### Batching

By default, one process will execute `method` on a single element of the iterable. This can result in significant
overhead if your iterable is much bigger than the number of workers, in which case the keyword "batched" can be used :

```python
    results = engine(method, [pd.DataFrame([[1, 2]]), pd.DataFrame([[3, 4]]), pd.DataFrame([[5, 6]])], batched=True)
```

In that case, sublists of elements are given to each process so that there are exactly the same number of processes than
numbers (unless the iterable is too small of course).

Doing this can also have its own problem, namely a load unbalance of some process finish much quicker than others. One
can optionally use more batches than the number of workers by giving an integer instead of a boolean to the "batched"
keyword :

```python
    # Using 16 batches
    results = engine(method, [pd.DataFrame([[1, 2]]), pd.DataFrame([[3, 4]]), pd.DataFrame([[5, 6]])], batched=16)
```

### other keyword arguments

The `method` can accept other keyword arguments, for example

```python
def method(df, s):
    return 2 * df * s, 3 * df * s
```

Those can be given when calling the engine and will be passed to each process. For example :
```python
from adparallelengine import Engine
import pandas as pd
from transparentpath import Path

def method(df, s):
    return 2 * df * s, 3 * df * s

if __name__ == "__main__":
    which = "multiproc"  # Can also be "serial", "dask", "mpi" or "k8s"
    engine = Engine(kind=which, path_shared=Path("tests") / "data" / "shared")
    some_series = pd.Series([10, 20])
    results = engine(method, [pd.DataFrame([[1, 2]]), pd.DataFrame([[3, 4]]), pd.DataFrame([[5, 6]])], s=some_series)
```

#### Large objects given to keyword arguments

If `method` is given large objects as keyword arguments, passing the object to workers could imply a significant loss
of time. I observed that doing out-of-core learning can sometime be quicker, despite the I/O that it implies. It 
can even save a bit of memory. You can use it by using the "share" keyword argument :

```python
    results = engine(method, [pd.DataFrame([[1, 2]]), pd.DataFrame([[3, 4]]), pd.DataFrame([[5, 6]])], share={"s": some_series})
```

Here, "some_series" will be written to disk by the engine, and only a path will be given to each process, which will then
read it when starting. For now, only pandas dataframes and series, and numpy arrays, are supported for sharing. The directory
where the shared objects are written is by default the local temp dir, by one can specify some other location by giving
the "path_shared" keyword argument when creating the engine (NOT when calling it!).

### Method to run in each processes

When using multiprocessing with numpy, one has to use the "spawn" multiprocessing context to avoid the GIL. By doing so
however, any environment variable or class attributes defined in the main process is forgotten in the child processes,
since the code is imported from scratch. So, one might need to re-load some variables and re-set some class attributes
inside each process. This can be done in an additional method that can be given to engine. The complete example below
shows how it is done.

### Complete example

The code below shows an example of how to use the engine. Here `method` accepts two other arguments, one that can be a
pandas' dataframe or series, and one that is expected to be a float. It returns a tuple of two dataframes.

If the parallelization is done using Python's native multiprocessing, do not forget to use `if __name__ == "__main__"`
like in the example !

```python
import sys
from typing import Union
import pandas as pd
import numpy as np
from transparentpath import Path

from adparallelengine import Engine


class Dummy:
    some_attr = 0


def method_in_processes(a):
    Dummy.some_attr = a


def method(
    element: pd.DataFrame,
    some_other_stuff: Union[float, pd.DataFrame, pd.Series, np.ndarray],
    some_float: float,
):
    return (
       element * some_other_stuff + some_float + Dummy.some_attr,
       3 * (element * some_other_stuff + some_float + Dummy.some_attr)
    )


if __name__ == "__main__":

    Dummy.some_attr = 1

    dfs = [
        pd.DataFrame([[0, 1], [2, 3]]),
        pd.DataFrame([[4, 5], [6, 7]]),
        pd.DataFrame([[8, 9], [10, 11]]),
        pd.DataFrame([[12, 13], [14, 15]]),
        pd.DataFrame([[16, 17], [18, 19]]),
        pd.DataFrame([[21, 22], [23, 24]]),
    ]
    s = pd.Series([2, 3])
    f = 5.0

    which = sys.argv[1]
    gather = True if sys.argv[2] == "True" else False
    batched = True if sys.argv[3] == "True" else False if sys.argv[3] == "False" else int(sys.argv[3])
    share = True if sys.argv[4] == "True" else False

    if share is True:
        share_kwargs = {"share": {"some_other_stuff": s}}
    else:
        share_kwargs = {"some_other_stuff": s}
    engine = Engine(kind=which, path_shared=Path("tests") / "data" / "shared")
    res = engine(
        method,
        dfs,
        init_method={"method": method_in_processes, "kwargs": {"a": 1}},
        some_float=f,
        gather=gather,
        batched=batched,
        **share_kwargs
    )
```
