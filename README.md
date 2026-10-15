# pathcase

[![CI](https://github.com/LuluGebi/pathcase/actions/workflows/ci.yml/badge.svg)](https://github.com/LuluGebi/pathcase/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)

A small, dependency-free CLI that batch-renames files and directories between
naming conventions: `snake_case`, `kebab-case`, `camelCase` and `PascalCase`.

## Why

Downloaded assets, screenshots and generated reports arrive in every naming
convention except the one your pipeline expects. `pathcase` normalises them in
one pass, without shell gymnastics or third-party dependencies.

## Features

- Convert to **snake_case**, **kebab-case**, **camelCase** or **PascalCase**
- Extensions are preserved (`My Photo.jpg` → `my_photo.jpg`)
- `-n/--dry-run` prints the plan before anything is touched
- `-r/--recursive` walks subdirectories (children renamed before parents)
- Existing names that already match the target style are left alone
- Cross-platform: Windows, macOS, Linux — pure standard library

## Install

```bash
pip install git+https://github.com/LuluGebi/pathcase.git
```

## Usage

Preview a rename (nothing is written):

```console
$ pathcase kebab -n "Summer Report 2026.pdf"
Summer Report 2026.pdf  ->  summer-report-2026.pdf
```

Do the rename:

```bash
pathcase snake .
pathcase kebab -r ~/Downloads
pathcase camel src/assets/icons
```

Exit code is `0` when every rename succeeded, `1` otherwise.

## Library use

```python
from pathlib import Path
from pathcase.core import plan_renames, apply_renames

plan = plan_renames(Path("downloads").iterdir(), "kebab")
apply_renames(plan)
```

## Development

```bash
pip install -e . pytest
pytest
```

## License

[MIT](LICENSE)
