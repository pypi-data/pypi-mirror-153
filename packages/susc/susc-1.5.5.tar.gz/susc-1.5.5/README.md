![License](https://img.shields.io/github/license/speedapi/susc)
![Version](https://img.shields.io/pypi/v/susc)
![Downloads](https://img.shields.io/pypi/dm/susc)
![PRs and issues](https://img.shields.io/badge/PRs%20and%20issues-welcome-brightgreen)

# SUS compiler
This repository contains the compiler and language server for the SUS description language. Install it with:
```
pip3 install susc
```

# What is SpeedAPI?
It's a platform-agnostic API and serialization tool specifically geared towards high-throughput realtime applications. You can read more about its features [here](https://github.com/speedapi/info)

# Usage

### Help
```
$ susc --help
# OR
$ python3 -m susc --help
```

### Compiler
  - Compile file(s): `susc source1.sus source2.sus`
  - Compile file, override output dir: `susc -o output source.sus`
  - Compile file, override output language: `susc -l ts source.sus`

### Language server
  - Start language server: `susc -s`
  - Start language server in stdio mode: `susc -si`

### Misc
  - Print file with syntax highlighting: `susc -p source.sus`
  - Explain a diagnostic code: `susc -x 0010`

# Programmatic usage
```python
from susc import File

file = File()
# load file:
file.load_from_file("/path/to/file.sus")
# or
file.load_from_file(open("/path/to/file.sus"))
# or load text:
file.load_from_text("compound Test { a: Str; b: Str; }")

things, diagnostics = file.parse()
print(things)
print(diagnostics)

language = "ts"
file.write_output(language, "/path/to/output/dir")
```
