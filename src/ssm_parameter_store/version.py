import importlib.metadata

try:
    __version__ = importlib.metadata.version('ssm-parameter-store')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.0'  # package not installed
