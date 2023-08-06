from pathlib import Path
import ssg_sea

# Project Directories
PACKAGE_ROOT = Path(ssg_sea.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "params.yaml"
DATASET_DIR = PACKAGE_ROOT / "data"
PICKLE_FILE_PATH = PACKAGE_ROOT / "data/pickle.pkl"


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")
