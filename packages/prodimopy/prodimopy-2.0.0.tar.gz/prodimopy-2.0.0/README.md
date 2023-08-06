# prodimopy

Python package for reading and plotting ProDiMo results.

Any bug reports or feature requests are very welcome.
If you want to contribute some code please contact me (Christian Rab).

[[_TOC_]]


## Notebook examples
If you want to take a look before installing you can try prodimopy
on the web in a binder environment:

[![prodimopy binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgitlab.astro.rug.nl%2Fprodimo%2Fprodimopy/HEAD?labpath=notebooks)

On your left hand side you will see the notebooks, just open one and try it!

## Requirements
prodimopy uses several additional python packages which are commonly used in the astronomical community. 
If you use [anaconda](https://www.anaconda.com/distribution/) all this packages should be available in your python distribution. 
The following packages are required

* *matplotib* required for the plotting part only, version>=2 is recommended  
* *astropy*     version >=2.0 is recommended
* *numpy*       no known special requirements
* *scipy*       no known special requirements

If you use the setup script (see Installation) those packages will be installed automatically if 
they are not included in your python distribution. We recommend to use python3 but python2 should
also still work.

## Installation

### from source (for Developers)
I you always want to have the most recent version of if you plan to change the code (you are very welcome) clone this repository and install the package directly from the source: 

* change into a directory of your choice and 
* clone the repository (git will create a new directory called prodimopy)

  ```
  git clone https://gitlab.astro.rug.nl/prodimo/prodimopy.git
  ```    
 
* change into the newly created prodimopy directory and type:

  ```
  python setup.py develop
  ```

This will install the package in your current python environment (should be the one you want to use for ProDiMo). 
The develop options allows to update the python code (e.g. via git) without the need to reinstall the package.

If you do not have root access to install python packages, this should work

  ```
  python setup.py develop --user
  ```

##### Code Update

Simply type 

```
git pull 
```

in the prodimopy directory. You can directly use the updated code (no reinstall required).

### via pip (for Users)
If you just want a stable version you can also use pip to install the project. Just type in the command line 

```
pip install prodimopy
```

to upgrade to a new version you can also use pip. We recommend to do it this way. 

```
pip install --upgrade --upgrade-strategy only-if-needed prodimopy
```
    
### Windows

We do not really recommend it and also do not test it, but it is also possible to use prodimopy with Windows (at least we know about one succesfull case). It worked with the Anaconda distribution for Windows. With the Anaconda prompt (comes with the installation) the installation procedure is the same as above. However, you most likely need to install git first.  


## Documentation
Please check out the documentation! Click on the badge!

[![Documentation Status](https://readthedocs.org/projects/prodimopy/badge/?version=latest)](https://prodimopy.readthedocs.io/en/latest/?badge=latest)

