# Python bindings to crate [FST](https://github.com/BurntSushi/fst)

For more mature implementation see https://github.com/jbaiter/python-rust-fst

## Motivation

This package is quick workaround for 
https://github.com/BurntSushi/fst/issues/38

In its state as is, it should not be really used, but I would not mind adding missing API, if you fill an issue.

Issue is fixed by throwing faulty levenstein DFA out the window, so performance will suffer. I will try to find time fix actual issue downstream later.

## Installation

TODO

## Usage

```py
from fst_python_bindings import FstMap

items = [
    ('soy', 0),
    ('joy', 2),
    ('godefroy', 3),
    ('godfrey', 3)
]
# Items must be in lexicographical order
items.sort(key=lambda item: item[0])

# Create map instance.
fst_map = FstMap.from_iter()

print(fst_map.search_levenstein('roy', 1))
print(fst_map.search_levenstein('godefrey', 1))
```