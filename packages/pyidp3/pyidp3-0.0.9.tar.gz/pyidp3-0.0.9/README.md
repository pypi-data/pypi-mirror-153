# Pyidp3

This project is a Python3 port [Joost Vennekens' pyidp](https://bitbucket.org/joostv/pyidp/src).

The Pyidp3 module is an API between [Python3](<https://www.python.org/>) and [the IDP system](https://dtai.cs.kuleuven.be/software/idp).
In short, IDP is a Knowledge Base System (KBS) using the FO(.) language.
FO(.) is standard First-Order logic, but expanded. See the IDP website for more.
A KBS is a system that stores all it's knowledge in a knowledge base, and then supports different inference method    s to apply on the knowledge. It's programmed in a declarative manner. More on programming the IDP system and FO(.)     can be found [here](https://dtai.cs.kuleuven.be/krr/files/TutorialIDP.pdf).

Pyidp3 will try to bridge the gap between IDP (which is programmed *declaratively*) and Python (which is programme    d *imperatively*).
It works in both directions: the user can supply data in Pythonic form to Pyidp3, which will then be converted to     IDP form and given to the IDP system.
When the IDP system is done infering, Pyidp3 will process it's output and translate this back into Pythonic form.

![](./Docs/images/pyidp3.png)



## Documentation
The documentation of this project can be found at the [readthedocs](https://pyidp3.readthedocs.io/en/latest/)
[![Documentation Status](https://readthedocs.org/projects/pyidp3/badge/?version=latest)](https://pyidp3.readthedocs.io/en/latest/?badge=latest)


## Installation
Pyidp3 is in the PyPi repository.
As such, simply using Pip to install will work.

For Arch-Linux:
```
pip install pyidp3
```

For most other Linux distributions:
```
python3 pip install pyidp3
```

## Features 
Because Pyidp3 is a port of Pyidp, not all features were added by me.

### Existing features from Pyidp
Here is the list of features that were already in Joost Vennekens' Pyidp (and were merely ported by me):

* Parsing Python to IDP, and from IDP to Python.
* Converting Pythonic to IDP-form. *(This is no longer supported. The code is there, I just don't work on it.)*
* Support for *Type*, *Predicate*, *Function*, *Constant* and *Definitions*.
* Support for *vocabulary*, *theory* and *structures*.
* Basic model expansion.


### Added features in Pyidp3
Here is the list of features I added myself:

* Sphinx [documentation](https://pyidp3.readthedocs.io/en/latest/)
* Documentation throughout the code, to make it more readable.
* Support for adding the *Term* block, as a subclass of *Block*.
* Support for **constructed_from** keyword in a *Type*.
* Support for **isa** keyword in a *Type*.
* Model expansion is now done by calling *.model_expand()*.
* Implemented a way to minimize, by adding the *.minimize(term)* method.
* Implemented a way to SATcheck, by adding the *.sat_check()* method.
* Users can now also set IDP options (All options! Most of them haven't been tested though).
* The *model_expand* and *minimize* methods are now able to return multiple solutions, instead of only one.
* The IDP object now has a *compare* method to compare two enumerables and list the differences.
