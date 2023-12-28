# Dollop
A python package for splitting up iterables into smaller portions 🥣.

## Usage

Supports:
- **Sequences:** `list`, `tuple`, `str`, `range`, `bytes`, `bytearray` or any other sequence-like object.
- **Pandas objects:** `DataFrame`, `Series`.
- **Files:** either as a file path or handle.

Example usage (automatically checks object type):
```
from dollop import serve

dollops = serve(items, serving_size=10)

for dollop in dollops:
    do_something(dollop)
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

These both have the disadvantage that typing is not preserved.