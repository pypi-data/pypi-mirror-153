# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['importlib_metadata_argparse_version']
extras_require = \
{':python_version < "3.8"': ['importlib_metadata']}

setup_kwargs = {
    'name': 'importlib-metadata-argparse-version',
    'version': '0.1.0',
    'description': 'Argparse action to define CLI version with a delayed call to importlib.metadata',
    'long_description': '# `importlib-metadata-argparse-version`\n\nPython\'s [`argparse`] module action to define CLI version with a delayed\ncall to [`importlib.metadata.version`] only when `--version` argument\nis passed.\n\n## Rationale\n\nWhen you use `importlib.metadata` for adding the version to a CLI utility,\nyou need to import `importlib.metadata` and call\n`importlib.metadata.version("<your-package>")` at initialization time.\nIf you only want to see the documentation for your CLI with `--help`,\n`importlib.metadata` will be imported too even when is not needed.\n\nThe problem is easily fixed by this module.\n\n## Usage\n\n```python\nimport argparse\n\nfrom importlib_metadata_argparse_version import ImportlibMetadataVersionAction\n\n\nparser = argparse.ArgumentParser()\nparser.add_argument(\n    "-v", "--version",\n    action=ImportlibMetadataVersionAction,\n    importlib_metadata_version_from="your-module-name",\n)\n```\n\nThis is a rough equivalent to something like:\n\n\n```python\nimport argparse\n\ntry:\n    import importlib.metadata as importlib_metadata\nexcept ImportError:\n    import importlib_metadata\n\n\nparser = argparse.ArgumentParser()\nparser.add_argument(\n    "-v", "--version",\n    action="version",\n    version=importlib_metadata.version("your-module-name"),\n)\n```\n\n...but with the difference that `importlib.metadata` will only be\nimported when you call `--version`, so it is more efficient.\n\nWhen using `ImportlibMetadataVersionAction` the `version` kwarg\naccepts `%(version)s` as a placeholder like `%(prog)s`. So you\ncan write something like this to display the program name before the\nversion:\n\n```python\nparser.add_argument(\n    "-v", "--version",\n    action=ImportlibMetadataVersionAction,\n    importlib_metadata_version_from="your-module-name",\n    version="%(prog)s %(version)s",\n)\n\n# or\n\nparser.version = "%(prog)s %(version)s"\nparser.add_argument(\n    "-v", "--version",\n    action=ImportlibMetadataVersionAction,\n    importlib_metadata_version_from="your-module-name",\n)\n```\n\nAnd the `version` kwarg becomes optional, being `"%(version)s"`\nthe default value.\n\nAnother convenient improvement is that, if you forget to define the\nkwarg `importlib_metadata_version_from` in the argument, a `ValueError`\nwill be raised at initialization time.\nPython\'s [`argparse`] `"version"` action raises an `AttributeError`\nonly when you call your program with `--version`, which is less safer\nbecause could lead you to forget the `version=` kwarg and the error\nwill pass unexpected until you test it.\n\n[`argparse`]: https://docs.python.org/3/library/argparse.html\n[`importlib.metadata.version`]: https://docs.python.org/3/library/importlib.metadata.html?highlight=importlib%20metadata#distribution-versions\n',
    'author': 'Álvaro Mondéjar Rubio',
    'author_email': 'mondejar1994@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mondeja/importlib-metadata-argparse-version',
    'py_modules': modules,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
