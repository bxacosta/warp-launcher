import sys
from pathlib import Path

# Add src to path so we can import our modules
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# ruff: noqa: E402
from warp_launcher.cli import main

if __name__ == "__main__":
    sys.exit(main())
