import sys
from pathlib import Path

# Add src directory to path so imports work correctly in pytest
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from lib.logger import setup_logging

setup_logging()
