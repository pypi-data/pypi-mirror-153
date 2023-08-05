# Brent algorithm

## To install

Brent's algorithm requires `Python 3.8` and the [rich](https://github.com/Textualize/rich) library.

To install the library, run:

```bash
pip install pydagogy-brent
```

Then run the following in a Python shell:

```python
from pydagogy_brent import Settings, brent
import math
settings = Settings(x_rel_tol=1e-12, x_abs_tol=1e-12, y_tol=1e-12, verbose=True)
f = math.cos
brent(f, 0.0, 3.0, settings)
```


## To develop

We use the [Poetry](https://python-poetry.org/) dependency management system.

We use [VS Code](https://code.visualstudio.com/), the Black/isort/pylint tools. To install them, run:

```bash
poetry install 
```
