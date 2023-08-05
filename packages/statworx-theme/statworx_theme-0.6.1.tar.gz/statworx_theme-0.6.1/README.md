# Statworx Theme

[![PyPI version](https://badge.fury.io/py/statworx-theme.svg)](https://badge.fury.io/py/statworx-theme)
[![Documentation Status](https://readthedocs.org/projects/statworx-theme/badge/?version=latest)](https://statworx-theme.readthedocs.io/en/latest/?badge=latest)
[![Release](https://github.com/AnHo4ng/statworx-theme/actions/workflows/release.yml/badge.svg)](https://github.com/AnHo4ng/statworx-theme/actions/workflows/release.yml)
[![Code Quality](https://github.com/AnHo4ng/statworx-theme/actions/workflows/conde_quality.yml/badge.svg)](https://github.com/AnHo4ng/statworx-theme/actions/workflows/conde_quality.yml)
[![Python version](https://img.shields.io/badge/python-3.8-blue.svg)](https://pypi.org/project/kedro/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/AnHo4ng/statworx-theme/blob/master/LICENSE)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

A color theme plugin for the [matplotlib](https://matplotlib.org/) library and all its derivatives, which automatically applies the official statworx color theme.
This package also registers commonly used [color maps](https://matplotlib.org/stable/tutorials/colors/colormaps.html) for use in presentations.

![Sample](./docs/assets/sample.svg)

## Quick Start

Simply install a module with `pip` by using the following command.

```console
pip install statworx-theme
```

To apply the style, you must call the `apply_style` function by typing:

```python
from statworx_theme import apply_style
apply_style()
```

## Gallery

We have an extensive gallery of figures using the statworx theme. You can see them [here](https://statworx-theme.readthedocs.io/en/latest/gallery.html).

![Sample](./docs/assets/gallery.png)
