import argparse


class ImportlibMetadataVersionAction(argparse._VersionAction):
    """Delayed version action for argparse.

    An action kwarg for argparse.add_argument() which computes
    the version number only when the version option is passed.

    This allows to import importlib.metadata only when the
    ``--version`` option is passed to the CLI.
    """

    def __init__(self, *args, **kwargs):
        try:
            self.importlib_metadata_version_from = kwargs.pop(
                "importlib_metadata_version_from"
            )
        except KeyError:
            raise ValueError(
                "Missing kwarg 'importlib_metadata_version_from' for ImportlibMetadataVersionAction"
            )
        super().__init__(*args, **kwargs)

    def __call__(self, parser, *args, **kwargs):
        version = self.version
        if version is None:
            # prevents default argparse behaviour because version is optional:
            # https://github.com/python/cpython/blob/86a5e22dfe77558d2e2609c70d1d9e27274a63c0/Lib/argparse.py
            #
            # if version not passed raises here:
            # AttributeError: 'ArgumentParser' object has no attribute 'version'
            try:
                version = parser.version
            except AttributeError:
                # use '%(version)s' as default placeholder
                version = "%(version)s"
        if "%(version)s" not in version:
            raise ValueError(
                "Missing '$(version)s' placeholder in ImportlibMetadataVersionAction's"
                " 'version' kwarg"
            )

        try:
            import importlib.metadata as importlib_metadata
        except ImportError:  # Python < 3.8
            import importlib_metadata

        # replacing here avoids `KeyError: 'prog'` when using printf placeholders
        #
        # seems safe because argparse uses printf placeholders
        self.version = version.replace("%(version)s", "{version}").format(
            version=importlib_metadata.version(
                self.importlib_metadata_version_from,
            ),
        )
        super().__call__(parser, *args, **kwargs)
