import sys
from pathlib import Path

# Adds the 'src' folder to the Python module path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from app.main import main

if __name__ == "__main__":
    raise SystemExit(main())
