# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-29

### Added

- Initial release.
- `pathcase` CLI supporting `snake`, `kebab`, `camel` and `pascal` naming styles.
- Extension preservation, `-r/--recursive`, `-n/--dry-run`.
- Python API: `words()`, `snake_case()`, `kebab_case()`, `camel_case()`, `pascal_case()`,
  `plan_renames()`, `apply_renames()`.
- CI matrix across Python 3.9–3.13 on Linux and Windows.
