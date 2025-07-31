# Dollop
A python package for splitting up iterables into smaller portions 🥣.

## Installation
`pip install dollop`

## Usage

Supports:
- **Sequences:** `list`, `tuple`, `str`, `range`, `bytes`, `bytearray` or any other sequence-like object.
- **Pandas objects:** `pd.DataFrame`, `pd.Series`.
- **Array-like objects:** `np.ndarray`, `torch.Tensor`.
- **Files:** either as a file path or handle.

Example usage (automatically checks object type):
```
from dollop import serve

for serving in serve('Dolloping all day long', serving_size=6):
    print(serving)

for serving in serve((1, 1, 2, 3, 5, 8, 13, 21, 34, 55), serving_size=4):
    print(serving)
```

Output:
```
Dollop
ing al
l day 
long
(1, 1, 2, 3)
(5, 8, 13, 21)
(34, 55)
```

The `serving_size` parameter defines how many items/lines/characters/etc. you want in each dollop!

To use type-specific `dollop`:
- **Sequences:** `from dollop.sequence import serve`.
- **Pandas:** `from dollop.pandas import serve`
- **Files:** `from dollop.file import serve`.

For `dollop.file` you can specify `mode=lines` or `mode=chars` to read the file line-by-line or character-by-character.


## See also

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
