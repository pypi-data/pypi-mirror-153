import logging
import os
from pathlib import Path


logger = logging.getLogger("fdfs_init")


base_dir = str(Path(__file__).parent.absolute())

env_file = os.environ.get("FASTFDS_CONFIG_FILE")
FASTFDS_CONFIG_FILE = env_file if env_file else os.path.join(base_dir, "fdfs.env")



