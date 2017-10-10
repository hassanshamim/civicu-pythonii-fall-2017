# Installing Packages

[OFFICIAL DOCUMENTATION](https://packaging.python.org/tutorials/installing-packages/) - Basically just reference that when you need.

We usually use `pip` which comes with python.



`pip install something` by default searches the Python Package Index (PyPi) for the package.

You can also install from various version control systems or locally.

A common pattern is to store all the necessary external packages (aka dependencies) in a `requirements.txt` file.



`pip freeze` will list out your installed packages.  You can copy and paste that into `requirements.txt`

To install all packages from a text file like above:

`pip install -r requirements.txt`  

This is generally the first step you take when working on a project or following a tutorial. (after you've cloned the repository and created a virtual environment)



## Creating a Package

- [simple reference package](https://github.com/kennethreitz/samplemod)
- [Guide to Structuring your package](http://docs.python-guide.org/en/latest/writing/structure/)
- [Official Reference](https://packaging.python.org/tutorials/distributing-packages/)

When you have code and you want to share it, or use it in other projects, you should create a python package which you can `pip install` when you want to use it.

There are different philosophies on how to structure a package, I reccommend keeping it as simple as possible to start, and enhance when you need.

The simplest way to create a new python package you intend to distribute, use a project scaffold.  I like [cookiecutter](https://github.com/audreyr/cookiecutter), specifically: [this one](https://github.com/audreyr/cookiecutter-pypackage)



To use cookiecutter to generate a project:

- create a virtualenv
- install cookiecutter
- tell it the template you want to use
  - `cookiecutter gh:audreyr/cookiecutter-pypackage`
  - answer a few questions
- Get your code ready to be installed by others:
  - The command you use to package your code varies, depending on supported python versions and various dependencies
  - view the official reference for more details
  - Today, we'll use `python setup.py bdist_wheel`
  - You're Ready!
- Share your package
  - Either upload to PyPi with [twine](https://pypi.python.org/pypi/twine) (You must register for a PyPI account)
  - Or just push to a github repo, and point there when you install it
  - `pip install git+https://git.repo/some_pkg.git#egg=SomeProject `

To install a package you created:

- if on github:` pip install git+https://git.repo/some_pkg.git#egg=SomeProject `
- if local: `pip install path/to/package/folder`