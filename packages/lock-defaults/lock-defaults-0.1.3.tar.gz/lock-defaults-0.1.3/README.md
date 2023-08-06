# lock-defaults
[![PyPI](https://img.shields.io/pypi/v/lock-defaults.svg)](https://pypi.org/project/lock-defaults/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/inkleby/lock-defaults/blob/main/LICENSE.md)
[![Copy and Paste](https://img.shields.io/badge/Copy%20%2B%20Paste%3F-yes!-blue)](#install)

This decorator is small and only relies on the standard library, so can just be copied into a project.

Python has a weird behaviour around default values for functions. If you use an empty list as a default argument, things added to the list during the function can hang around for next time the function is called. A common pattern of dealing with this is the following:

```python
def func(foo = None):
    if foo is None:
        foo = []
```

But this looks rubbish! And gets worse when you add typing:

```python
def func(foo: list | None = None):
    if foo is None:
        foo = []
```

You don't need that workaround for any other of default value. Why does the list parameter have to pretend it can be None, when that's not the intention at all?

The `lockmutabledefaults` decorator fixes this by introducing what *should* be the default approach, and default values that are lists, dictionaries or sets are isolated in each re-run.

```python
@lockmutabledefaults
def func(foo: list = []):
    pass
```

## Install

You can install from pip: `python -m pip install lock-defaults`

Or you can copy the function directly into your projects.

* For python 3.10+: [with_paramspec/lock_defaults.py](/src/lock_defaults/with_paramspec/lock_defaults.py)
* For python 3.8, 3.9: [without_paramspec/lock_defaults.py](/src/lock_defaults/without_paramspec/lock_defaults.py)
