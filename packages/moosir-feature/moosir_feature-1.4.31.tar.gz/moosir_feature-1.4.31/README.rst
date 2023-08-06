==============
moosir_feature 
==============
(Trader.Forex.Moosir.Feature)

It s to create packages required for feature extraction
Follow [this](https://pyscaffold.org/en/stable/usage.html)

.. contains feature extraction, news data, ...

How to run tests
################
`pytest /tests`


How to run
##########
* create conda env with environment.yml
* run ``pip install -e .``
* run ``tox -e build``
* create package locally ``tox -e publish``
* push package in pypi ``tox -e publish -- --repository pypi``
    * to publish, you need to tag git commits (otherwise pypi returns errors)
    * **After commit** ``git tag -a v1.4 -m "my version 1.4"``
        * make sure version matches the intended pypi version
        * to see list of git tags 
            * ``git describe``
            * ``python setup.py --version``
        * if not work
            * delete tags, ammend commends, add tag again, tox build
        * if still does not work delete .tox and dist directory
        * if version is big version change, just mention two first part
            * v1.0 and not v1.0.0!!!
    * in case does nt work, remove all in ``.tox`` file

Note
#################
* tox cant be used for running tests
    * ```tox``` returns errors!!
    * todo: why?
* additional package
    * in setup.cfg
        * ``install_requires``













