# EmptyFile

![emptyfile](https://github.com/alexpdev/emptyfile/blob/master/assets/emptyfile.png?raw=true)

-----------

![GitHub repo size](https://img.shields.io/github/repo-size/alexpdev/emptyfile?color=orange)
![GitHub contributors](https://img.shields.io/github/contributors/alexpdev/emptyfile)

## 🌐 Overview

`emptyfile` is a tiny console tool that removes empty files or directories from your filesystem. The program recursively traverses a given directory and analyizes each file.

## 🔌 Requirements

- python 3

## 💻 Install

To install EmptyFile, follow these steps:

from __git__

```bash
git clone https://github.com/alexpdev/emptyfiles.git
cd emptyfiles
pip install .
```

from __PyPi__

```bash
pip install emptyfile
```

## 🚀 Usage

- Remove empty files recursively from one or more base directories

```bash
emptyfiles /path/1 /path/2 /path/3 ...
```

- Remove empty directories recursively from one or more base directories

```bash
emptyfiles -d /path/1 /path/2 /path/3 ...
```

- Include a list of file extensions to ignore while checking for empty's

```bash
emptyfiles --exclude-ext .py .json ... -- /path/1 /path/2 ...
```

- Include a list of file or directory names to ignore while searching for empty files

```bash
emptyfiles --exclude-names README.md __init__.py .gitignore -d /path/1 ...
```

> Both the `exclude-ext` and `exclude-names` options can be used with or without the `-d` directory option

## Contributing

Issues, Feature Requests and Pull Requests are all welcome.

## 📝 License

__Apache 2.0 License__
See `LICENSE` file for more information.
