# Python Modules



### [Official Docs](https://docs.python.org/3/tutorial/modules.html)



### Review

**[PATH](https://en.wikipedia.org/wiki/PATH_(variable))** Is a environment variable on your computer that lists directories to look in for the commands you type.  Sometimes when installing new software on your computer, you must edit the PATH variable to include the new directory with the code/tool you just installed.  Other times, the software will be installed to a folder already on your path.

You can see your path in python: `python -c 'from sys import path; print(path)'`.  NOTE: that first empty string refers to your current working directory.

When you activate a virtual environment, the new folder is added to the beginning of your path, taking precedence over other python installation.s

Python uses your PATH to find the modules you import as well.

**NOTE:** [PYTHONPATH](https://docs.python.org/3.6/using/cmdline.html#envvar-PYTHONPATH) is a special environment variable you can use to tell python where to find modules.  This only comes into play when you are importing a module, not executing a python file.

### What is a Python Module?

- A python file, package, or .zip file from which you can 'import' code.
- Normally just individual files that can be imported or called directly



You can locate python on your filesystem by accessing their `__file__` attribute.  (This doesn't work for some builtins)

### What is a Python Package?

- A collection of modules in a folder
- The folder name is the name of the package (unless overridden)
- May contain other packages
- i.e. `import packageA.moduleB` or `import packageA.packageB` etc
- **Must** have an `__init__.py` file, to indicate it's a package
- `__init__.py` can be blank
- optional `__main__.py`- acts like the `if __name__ == '__main__`' block above



### Importing

When you import a python module, the whole file is executed.  Generally, it only contains function or variable definitions.  But if you want to treat it like a script, we wrap the code in a special conditional:

```python
if __name__ == '__main__':
      # Code to be run goes here
```

This conditional is triggered ONLY when we run the file with `python some_file.py` and not when we `import some_file`.

### Types of imports

`import requests` 

- Imports whole module at top level namespace

- Access submodules or packages with dot notation `requests.api`

  ​

`from requests import api`

- imports submodule directly

- Avoids top level, only gets the `api` submodule

- Access imported module directly.  `api` not `requests.api`

  ​

`import numpy as np`

`from requests import api as requests_api`

- Rename a module as it's imported

  ​

`from requests import *`

- wildcard import.  It gets everything defined inside of requests.

- no more `requests.` prefix

- Please don't do this.  Makes dependencies implicit (I can't scroll to the top of your file and figure out what module `some_function` comes from)

  ​

`from . import sibling_package`

- **Relative** import
- in this example, assumes `sibling_package` is in the same folder as the file with the above import
- Can also import from parent directories: `from .. import something_else`
- Absolute imports are generally favored