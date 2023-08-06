# GeezLit

![GitHub issues](https://img.shields.io/github/issues/fgaim/geezswitch.svg)
[![PyPI](https://img.shields.io/pypi/v/geezswitch.svg)](https://pypi.org/project/geezswitch/)

**Ge'ez** Trans**lit**eration

A Python library for transliterating Ge'ez script into various ASCII based encodings.

Supported scheme:

- [x] ethiop: for Latex documents that use the `ethiop` package with `babel` to render Ge'ez text.
- [ ] sera: a system for representing Ge'ez script in ASCII.
- [ ] msera: a system based on SERA but modified by [HornMorph](https://github.com/hltdi/HornMorpho).
- [ ] geezime: a scheme used by the [GeezIME](https://geezlab.com) input method by GeezLab
- [ ] ipa: the International Phonetic Alphabet [IPA](https://en.wikipedia.org/wiki).

## Install

Use pip install the package:

```
pip install geezlit
```

## Usage

Once installed, you can import the library and make a simple function calls.

```python
from geezlit import geezlit

geezlit("<Ge'ez text>", style="<style>")
```

Currently, the default `style` is `ethiop`.
