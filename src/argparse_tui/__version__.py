try:
    from ._version import version
except ModuleNotFoundError:
    import importlib.metadata

    __version__ = importlib.metadata.version(__name__)
else:
    __version__ = version
