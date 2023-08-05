# tkdialog-wrapper

A wrapper library to use tkinter dialogs easily.

[![PyPI version](https://badge.fury.io/py/tkdialog-wrapper.svg)](https://badge.fury.io/py/tkdialog-wrapper) [![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

## Usage

`pip install tkdialog-wrapper`

```python
import tkdialog

# make open dialog
filename = tkdialog.open_dialog()

# make saveas dialog
filename = tkdialog.open_dialog()

# open a pickled file with file selector
obj = tkdialog.load_pickle_with_dialog()

# pickle an object with save dialog
dat = {'x': 100, 'y': '01234'}
tkdialog.dump_pickle_with_dialog(dat)

# with numpy
dat = np.load(tkdialog.open_dialog())

# with pandas
df = pd.read_csv(tkdialog.open_dialog())
```
