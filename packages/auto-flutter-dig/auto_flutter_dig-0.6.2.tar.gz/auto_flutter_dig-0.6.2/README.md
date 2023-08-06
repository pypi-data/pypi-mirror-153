# Auto Flutter
[![Build Status](https://img.shields.io/appveyor/build/DIG-/auto-flutter/main?logo=appveyor&logoColor=dddddd)](https://ci.appveyor.com/project/DIG-/auto-flutter/branch/main)
[![PyPI - License](https://img.shields.io/pypi/l/auto-flutter-dig?color=blue)](https://creativecommons.org/licenses/by-nd/4.0/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/auto-flutter-dig)](https://pypi.org/project/auto-flutter-dig/)
[![PyPI - Version](https://img.shields.io/pypi/v/auto-flutter-dig)](https://pypi.org/project/auto-flutter-dig/)

[![Windows - Supported](https://img.shields.io/badge/windows-supported-success?logo=windows&logoColor=dddddd)](#)
[![Linux - Supported](https://img.shields.io/badge/linux-supported-success?logo=linux&logoColor=dddddd)](#)
[![MacOS - Partial](https://img.shields.io/badge/macos-partial-orange?logo=apple&logoColor=dddddd)](#)

Automatic build tools for flutter build tools

### Reason
Flutter build tools does not allow to create or bind tasks, making some process tedious.
Auto Flutter came with that in mind. Tasks that can be bind with other, and some integrations, like Firebase AppDist out of box.

## License
[CC BY-ND 4.0](https://creativecommons.org/licenses/by-nd/4.0/)

- You can use and redist freely.
- You can also modify, but only for yourself.
- You can use it as a part of your project, but without modifications in this project.

## Installation
### From PyPI (preferred):
``` sh
python -m pip install auto_flutter_dig
```
### From github release:
``` sh
python -m pip install "https://github.com/DIG-/auto-flutter/releases/download/0.6.2/auto_flutter_dig-0.6.2-py3-none-any.whl"
```
or
``` sh
python -m pip install "https://github.com/DIG-/auto-flutter/releases/download/0.6.2/auto_flutter_dig.tar.gz"
```

### From github main branch:
``` sh
python -m pip install "git+https://github.com/DIG-/auto-flutter.git@main#egg=auto_flutter_dig"
```

## Usage
``` sh
python -m auto_flutter_dig
```
or
``` sh
aflutter
```

### First steps
``` sh
# To show help
aflutter help
# To show how to configure environment
aflutter setup -h
# Check if everything is ok
aflutter setup --check
```

Go to your flutter project root. Aka. Where is `pubspec.yaml` and:
``` sh
aflutter init --name "Name to your project"
# And let the magic happen
```
