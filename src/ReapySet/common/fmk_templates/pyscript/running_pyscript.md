# Running PyScript 101

## Project structure

```text
project/
├── index.html
├── main.py
├── utils.py (optional)
└── pyscript.json
```

## HTML

```html
<link
    rel="stylesheet"
    href="https://pyscript.net/releases/2026.7.2/core.css"
>

<script
    type="module"
    src="https://pyscript.net/releases/2026.7.2/core.js">
</script>

<script
    type="py"
    src="./main.py"
    config="./pyscript.json">
</script>
```

## Installing packages

Declare external packages in `pyscript.json`:

```json
{
    "packages": [
        "numpy",
        "pandas"
    ]
}
```

Import them as usual:

```python
import numpy as np
import pandas as pd
```

PyScript downloads the packages automatically. Most pure Python packages work, but not every package on PyPI is compatible with WebAssembly.

## Importing local modules

Expose local files in `pyscript.json`:

```json
{
    "files": {
        "./utils.py": "./utils.py"
    }
}
```

Import them normally:
 for example
```python
from utils import create_message
```

The left-hand path is the source file, while the right-hand path is its destination in PyScript's virtual file system.

## Running the project

Start a local web server:

```bash/zsh
python -m http.server 8000
```

Open your browser and navigate to:

```text
http://localhost:8000
```

Do not open `index.html` directly using a `file://` URL.