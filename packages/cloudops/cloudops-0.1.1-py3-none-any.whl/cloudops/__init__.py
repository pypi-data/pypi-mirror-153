"""The cloudops package."""
from datetime import datetime
import pkgutil

__version__ = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
__path__ = pkgutil.extend_path(__path__, __name__)
