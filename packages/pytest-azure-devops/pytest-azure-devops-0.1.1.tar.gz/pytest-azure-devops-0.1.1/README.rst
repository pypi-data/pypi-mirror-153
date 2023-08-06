===================
pytest-azure-devops
===================

.. image:: https://img.shields.io/pypi/v/pytest-azure-devops.svg
    :target: https://pypi.org/project/pytest-azure-devops
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-azure-devops.svg
    :target: https://pypi.org/project/pytest-azure-devops
    :alt: Python versions

.. image:: https://dev.azure.com/elies/elies/_apis/build/status/FrancescElies.pytest-azure-devops?branchName=master
    :target: https://dev.azure.com/elies/elies/_build?definitionId=5&_a=summary&branchFilter=19
    :alt: See Build Status on Azure DevOps

Simplifies using azure devops `azure devops parallel strategy`_ with pytest.

Instead of using a powershell as in `ParallelTestingSample-Python`_ to
do the test selection we we can tell pytest to directly take care of
selecting the right subset.

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.



Installation
------------

You can install "pytest-azure-devops" via `pip`_ from `PyPI`_::

    $ pip install pytest-azure-devops


Usage
-----

* TODO

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/FrancescElies/pytest-azure-devops/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project/pytest-azure-devops
.. _`azure devops parallel strategy`: https://docs.microsoft.com/en-us/azure/devops/pipelines/test/parallel-testing-any-test-runner
.. _`ParallelTestingSample-Python`: https://github.com/PBoraMSFT/ParallelTestingSample-Python
