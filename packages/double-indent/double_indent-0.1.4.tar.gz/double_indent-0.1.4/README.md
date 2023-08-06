[![ci](https://github.com/theendlessriver13/double-indent/workflows/ci/badge.svg)](https://github.com/theendlessriver13/double-indent/actions?query=workflow%3Aci)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/theendlessriver13/double-indent/master.svg)](https://results.pre-commit.ci/latest/github/theendlessriver13/double-indent/master)
[![codecov](https://codecov.io/gh/theendlessriver13/double-indent/branch/master/graph/badge.svg)](https://codecov.io/gh/theendlessriver13/double-indent)

# double-indent

A code formatter to add double indentation to function and method definitions.

## Installation

`pip install double-indent`

## usage

```console
usage: double-indent [-h] [-i INDENT] [filenames ...]

positional arguments:
  filenames

optional arguments:
  -h, --help            show this help message and exit
  -i INDENT, --indent INDENT
                        number of spaces for indentation
```

## pre-commit hook

See [pre-commit](https://pre-commit.com) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/theendlessriver13/double-indent
  rev: 0.1.4
  hooks:
    - id: double-indent
```

## indent function and method definitions twice

```diff
 def func(
-    arg,
-    arg2,
+        arg,
+        arg2,
 ):
     ...
```

```diff
 class C:
     def __init__(
-        self,
-        arg,
+            self,
+            arg,
     ):
         ...
```
