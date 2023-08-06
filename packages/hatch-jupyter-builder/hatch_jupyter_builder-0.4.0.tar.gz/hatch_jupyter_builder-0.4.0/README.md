# hatch-jupyter-builder

[![PyPI - Version](https://img.shields.io/pypi/v/hatch-jupyter-builder.svg)](https://pypi.org/project/hatch-jupyter-builder)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-jupyter-builder.svg)](https://pypi.org/project/hatch-jupyter-builder)

---

This provides a [build hook](https://hatch.pypa.io/latest/config/build/#build-hooks) plugin for [Hatch](https://github.com/pypa/hatch) that adds a build step for use with Jupyter packages.

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Usage and Configuration](#usage_and_configuration)
- [Local Development](#local_development)

## Installation

```console
pip install hatch-jupyter-builder
```

## License

`hatch-jupyter-builder` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Usage and Configuration

The [build hook plugin](https://hatch.pypa.io/latest/plugins/build-hook/) name is `jupyter-builder`.

- **_pyproject.toml_**

  ```toml
  [tool.hatch.build.hooks.jupyter-builder]
  dependencies = ["hatch-jupyter-builder"]
  build-function = "hatch_jupyter_builder.npm_builder"
  ensured-targets = ["foo/generated.txt"]
  install-pre-commit-hook = true

  [tool.hatch.build.hooks.jupyter-builder.build-kwargs]
  build_cmd = "build:src"
  ```

### Options

The only required fields are `dependencies` and `build-function`.
The build function is defined as an importable string with a module and a function name, separated by a period. The function must accept a
`target_name` (either "wheel" or "sdist"), and a `version` (either "standard" or "editable") as its only positional arguments. E.g.

- **_builder.py_**

  ```python
  def build_func(target_name, version):
      ...
  ```

Would be defined as `build-function = "builder.build_func"`

The optional `ensured-targets` is a list of expected file paths after building a
"standard" version sdist or wheel.

The optional `skip-if-exists` is a list of paths whose presence would cause
the build step to be skipped.

The optional `build-kwargs` is a set of keyword arguments to pass to the build
function.

You can also use `editable-build-kwargs` if the parameters should differ
in editable mode. If only the build command is different, you can use
`editable_build_cmd` in `build-kwargs` instead.

The optional `install-pre-commit-hook` boolean causes a `pre-commit` hook to be installed during an editable install.

### Npm Builder Function

This library provides a convenenice `npm_builder` function which can be
used to build `npm` assets as part of the build.

## Local Development

To test this package locally with another package, use the following:

```toml
[tool.hatch.build.hooks.jupyter-builder]
dependencies = ["hatch-jupyter-builder@file://<path_to_this_repo>"]
```
