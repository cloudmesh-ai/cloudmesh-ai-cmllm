from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("cloudmesh-ai-cmm")
except PackageNotFoundError:
    # Fallback for local development if not installed
    try:
        with open("VERSION") as f:
            __version__ = f.read().strip()
    except FileNotFoundError:
        __version__ = "0.0.0"
