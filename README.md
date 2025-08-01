# Dollop
A python package for splitting up iterables into smaller portions 🥣.

## Installation 
`pip install dollop`

## Overview & examples

Dollop is a flexible, simple tool for splitting up iterables into smaller parts. It preserves type, so 
dolloping a string yields substrings, dolloping a tuple yields subtuples, etc.

Here are some quick examples on how to use Dollop!

```
from dollop import serve

for serving in serve('Dolloping all day long', serving_size=6):
    print(serving)

for serving in serve((1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89), n_servings=4):
    print(serving)
```

Output:
```
Dollop
ing al
l day 
long
(1, 1, 2)
(3, 5, 8)
(13, 21, 34)
(55, 89)
```

## Supported types & modes

Dollop supports the following iterable types:
- **Sequences:** `list`, `tuple`, `str`, `range`, `bytes`, `bytearray` or any other sequence-like object.
- **Pandas objects:** `pd.DataFrame`, `pd.Series`.
- **Array-like objects:** `np.ndarray`, `torch.Tensor`.
- **Files:** either as a file path or handle.

You can dollop either according to:
- **`serving_size`**: Splits the iterable into equal-sized dollops of size `serving_size`, except possibly the last dollop which may be smaller.
- **`n_servings`**: Splits the iterable into `n_servings` dollops of equal size ±1. Note this option cannot be used to dollop files or file handles.

The main method is `dollop.serve`, which checks the input type and acts accordingly. Under the hood, this calls one of the following type-specific methods
- **Sequences:** `from dollop.sequence.serve import serve`.
- **Pandas:** `from dollop.pandas.serve import serve`
- **NumPy:** `from dollop.numpy.serve import serve`
- **PyTorch:** `from dollop.torch.serve import serve`
- **Files:** `from dollop.file.serve import serve`.

## Dolloping files

Files can either be dolloped by line or by character. The file can be passed either as a `Path` type, a file handle, or a string filename (if using the type-specific `dollop.file.serve`). For example:
```
from dollop import serve

# Processes the file 5 lines at a time
with open('yogurt.txt') as f:
    for lines in serve(f, serving_size=5, mode='lines'):
        do_something(lines)

# Processes the file 10 characters at a time
with open('yogurt.txt') as f:
    for chars in serve(f, serving_size=10, mode='chars'):
        do_something(lines)
```


Or you can use the type-specific method to open the file directly from its name (otherwise `dollop` will treat it as a string):

```
from dollop.file import serve

# Processes the file 5 lines at a time

for lines in serve('yogurt.txt', serving_size=5, mode='lines'):
    do_something(lines)
```


## Dolloping arrays and tensors 
For arrays (NumPy) and tensors (PyTorch), you can additionally add the `dim` argument to specify which dimension on which to split. For example:

```
import numpy as np

from dollop import serve

array = np.random.rand(10, 10, 10, 10)
for serving in serve(array, serving_size=3):
    print(serving.shape)

for serving in serve(array, serving_size=3, dim=2):
    print(serving.shape)    
```

Output:

```
(3, 10, 10, 10)
(3, 10, 10, 10)
(3, 10, 10, 10)
(1, 10, 10, 10)
(10, 10, 3, 10)
(10, 10, 3, 10)
(10, 10, 3, 10)
(10, 10, 1, 10)
```

## Comparison with other tools

The `more_itertools` and later (Python 3.12+) `itertools` packages have something similar:

```
from more_itertools import chunked

chunks = chunked(iterable, n))
```

and

```
from itertools import batched

batches = batched(iterable, n))
```

However these both have the major disadvantage that typing is not preserved, for example chunking/batching a string does not return an iterable of strings, but an iterable of tuples.
