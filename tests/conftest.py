"""Make the `scripts/` directory importable by tests.

Scripts aren't organized as a Python package, so without this hook each
test module would need its own sys.path manipulation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
