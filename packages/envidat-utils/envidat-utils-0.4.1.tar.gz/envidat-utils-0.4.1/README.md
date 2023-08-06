# EnviDat Python Utils

<div align="center">
  <img src="https://www.envidat.ch/uploads/group/2020-11-04-134216.5237452000px-LogoWSL.svg.png" width="200" style="width: 200px;" alt="WSL"></a>
</div>
<div align="center">
  <em>Utilities for EnviDat projects in Python.</em>
</div>
<div align="center">
  <a href="https://pypi.org/project/envidat-utils" target="_blank">
      <img src="https://img.shields.io/pypi/v/envidat-utils?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypistats.org/packages/envidat-utils" target="_blank">
      <img src="https://img.shields.io/pypi/dm/envidat-utils.svg" alt="Downloads">
  </a>
  <a href="https://gitlabext.wsl.ch/EnviDat/envidat-python-utils/-/raw/main/LICENCE" target="_blank">
      <img src="https://img.shields.io/github/license/EnviDat/envidat-python-utils.svg" alt="Licence">
  </a>
</div>

---

**Documentation**: <a href="https://envidat.gitlab-pages.wsl.ch/envidat-python-utils/" target="_blank">https://envidat.gitlab-pages.wsl.ch/envidat-python-utils/</a>

**Source Code**: <a href="https://gitlabext.wsl.ch/EnviDat/envidat-python-utils" target="_blank">https://gitlabext.wsl.ch/EnviDat/envidat-python-utils</a>

---

## PyPi Package

- This package aims to speed up EnviDat python workflows
- Contains:
  - Backend API function wrappers.
  - S3 bucket class, with configurable endpoint.
  - Utils to use in multiple projects (e.g. consistent logger setup).

## Install

```bash
$ pip install -U pip
$ pip install envidat-utils
```

## Usage

```python
from envidat.utils import get_logger
from envidat.s3 import Bucket
from envidat.api.v1 import get_package_list
```
