# pdfcropper

`pdfcropper` is a tool to crop pdf files and converting them into png files.

## Installation

You can install `pdfcropper` by cloning this repository or by using [Pip](http://pypi.python.org/pypi/pip):

```sh
$ pip install pdfcropper
```

If you want to use the development version, you can install directly from github:

```sh
$ pip install -e git+git://gitlab.com/ali7line/awesome-scripts/-/tree/master/pdfcropper
```

If using, the development version, you might want to install dependencies as well:

```
$ pip install -r requirements.txt
```

**NOTE**: Only tested in Python **3.7.9**

## Usage

Just run `pdfcropper --help` to see the commands available options.

The list of options available are:

* `--config=<FILE>` to specify your yaml config file to use
* `--sample-config=<FILE>` writres sample yaml config file with default options
