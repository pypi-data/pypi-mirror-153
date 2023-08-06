# `importlib-metadata-argparse-version`

Python's [`argparse`] module action to define CLI version with a delayed
call to [`importlib.metadata.version`] only when `--version` argument
is passed.

## Rationale

When you use `importlib.metadata` for adding the version to a CLI utility,
you need to import `importlib.metadata` and call
`importlib.metadata.version("<your-package>")` at initialization time.
If you only want to see the documentation for your CLI with `--help`,
`importlib.metadata` will be imported too even when is not needed.

The problem is easily fixed by this module.

## Usage

```python
import argparse

from importlib_metadata_argparse_version import ImportlibMetadataVersionAction


parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--version",
    action=ImportlibMetadataVersionAction,
    importlib_metadata_version_from="your-module-name",
)
```

This is a rough equivalent to something like:


```python
import argparse

try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata


parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--version",
    action="version",
    version=importlib_metadata.version("your-module-name"),
)
```

...but with the difference that `importlib.metadata` will only be
imported when you call `--version`, so it is more efficient.

When using `ImportlibMetadataVersionAction` the `version` kwarg
accepts `%(version)s` as a placeholder like `%(prog)s`. So you
can write something like this to display the program name before the
version:

```python
parser.add_argument(
    "-v", "--version",
    action=ImportlibMetadataVersionAction,
    importlib_metadata_version_from="your-module-name",
    version="%(prog)s %(version)s",
)

# or

parser.version = "%(prog)s %(version)s"
parser.add_argument(
    "-v", "--version",
    action=ImportlibMetadataVersionAction,
    importlib_metadata_version_from="your-module-name",
)
```

And the `version` kwarg becomes optional, being `"%(version)s"`
the default value.

Another convenient improvement is that, if you forget to define the
kwarg `importlib_metadata_version_from` in the argument, a `ValueError`
will be raised at initialization time.
Python's [`argparse`] `"version"` action raises an `AttributeError`
only when you call your program with `--version`, which is less safer
because could lead you to forget the `version=` kwarg and the error
will pass unexpected until you test it.

[`argparse`]: https://docs.python.org/3/library/argparse.html
[`importlib.metadata.version`]: https://docs.python.org/3/library/importlib.metadata.html?highlight=importlib%20metadata#distribution-versions
