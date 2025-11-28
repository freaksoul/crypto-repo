import os

# Base directory for data files. Can be overridden with environment variable
# VIBORON_DATA_DIR. Default stays compatible with existing setups on Windows.
BASE_DATA_DIR = os.environ.get('VIBORON_DATA_DIR', r'C:\Viboron\CryptoProyecto')

def data_path(filename: str) -> str:
    """Return an absolute path under the configured data directory.

    Ensures the directory exists.
    """
    base = os.path.abspath(BASE_DATA_DIR)
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, filename)
