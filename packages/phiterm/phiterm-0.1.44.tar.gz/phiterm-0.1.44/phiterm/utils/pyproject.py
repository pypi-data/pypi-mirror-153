from pathlib import Path
from typing import Optional, Dict

from phiterm.utils.log import logger


def read_pyproject_phidata(pyproject_file: Path) -> Optional[Dict]:
    logger.debug(f"reading {pyproject_file}")
    try:
        import tomli

        pyproject_dict = tomli.loads(pyproject_file.read_text())
        logger.debug(f"pyproject_dict: {pyproject_dict}")
        phidata_conf = pyproject_dict.get("tool", {}).get("phidata", None)
        if phidata_conf is not None and isinstance(phidata_conf, dict):
            return phidata_conf
    except Exception as e:
        logger.error(f"Could not read {pyproject_file}")
        logger.error(e)
    return None
