# Pandas

Today's lesson will focus on the Pandas package.  We'll be following [Brandon Rhodes' 2015 PyCon Tutorial](https://www.youtube.com/watch?v=5JnMutdy6Fw) with some slight modifications.



The [source repository](https://github.com/hassanshamim/pycon-pandas-tutorial) for this lesson is forked from Brandon's original repo.  I've manually added a trimmed version of the original data (each csv is limited to 200k rows.  The orignal cast.csv for reference is 3.6 million rows) and included a `requirements.txt` to build our environment from.  Some minor changes to the lessons have been made to avoid deprecation warnings.



Original prepared csvs (as used in the repo) can be downloaded [here](https://drive.google.com/open?id=1o8uXNPZkblilgT-yrc1UTGjIEWghW2fh) if you would like the full dataset without going through the build process as described in the original repo.



## Set-up

Usual instructions as always - clone the repo, create a virtual environment, activate it, install from `requirements.txt`.  You can use your previous environment from our numpy lesson if you'd like to avoid the boilerplate steps.  You'll still need to `pip install -r requirements.txt` to get pandas and matplotlib.



### Links

- [BinderHub](https://mybinder.org/v2/gh/hassanshamim/pycon-pandas-tutorial/master) ( live notebook of this repo in your browser)

### References

- [Pandas API reference](https://pandas.pydata.org/pandas-docs/stable/api.html)
- [Python DataScience Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/03.00-introduction-to-pandas.html)
- [Cheat Sheet](https://github.com/pandas-dev/pandas/blob/master/doc/cheatsheet/Pandas_Cheat_Sheet.pdf)