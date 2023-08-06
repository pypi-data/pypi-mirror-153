# dict_and_union_with

A manual solution to the union operation on dictionaries, in Python

Inspired by `union_with` from Haskell.

Keep in mind that Python now has a union operator:

`dict_one |= dict_two  # union dict_two into dict_one`

`dict_union = dict_one | dict_two  # dict_union is the union of dict_one and dict_two`

In `dict_and_union_with`, these instructions become:

`union_with(dict_one, dict_two)  # union dict_two into dict_one`

`dict_union = union_all_with(dict_union, [dict_one, dict_two])  # dict_union is the union of dict_one and dict_two`

Open source available on [GitHub](https://github.com/Whoeza/dict_and_union_with) and 
[PyPI](https://pypi.org/project/dict_and_union_with/).

## Installation

Install from pip:

`py -m pip install dict_and_union_with`

Update to the latest version from pip:

`py -m pip install --upgrade dict_and_union_with`

Uninstall from pip:

`py -m pip uninstall dict_and_union_with`

### Building from sources

Run this command from the package directory on your filesystem:

`py -m build`

## Community

[Open a new issue](https://github.com/Whoeza/dict_and_union_with/issues) for
support.
