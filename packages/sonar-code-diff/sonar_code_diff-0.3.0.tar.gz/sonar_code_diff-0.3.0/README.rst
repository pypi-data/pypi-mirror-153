======================
Sonar Code Diff Plugin
======================


.. image:: https://img.shields.io/pypi/v/sonar_code_diff.svg
        :target: https://pypi.python.org/pypi/sonar_code_diff

.. image:: https://readthedocs.org/projects/sonar-code-diff/badge/?version=latest
        :target: https://sonar-code-diff.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Sonar Code Diff is used to run a diff between a test code base and known code base


* Free software: MIT license
* Documentation: https://sonar-code-diff.readthedocs.io.


Features
--------

* This is used to scan code that has been copied from a third party and you can't guarantee
  that there haven't been any changes.  Run this scanner and point it to both the directory
  you are scanning and a copy of the original verified source.  This will generate a
  report that can be imported directly into SonarQube.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
