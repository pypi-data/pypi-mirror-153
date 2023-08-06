=========
Changelog
=========

0.8.0 (2022-06-06)
==================

Generate a new `biskotaki` Python Package Project, using the
`v1.4.0 Cookiecutter Python Package`_ project generator.

For more, on the generator used, check the `documentation`, `repository`_ and `Template`_ links.

Generated Additions
-------------------

Complete Documentation Website, build with Sphinx on readthedocs.org server!


0.7.0 (2022-05-11)
==================

Generate a new `biskotaki` Python Package Project, using the
`v0.10.0 Cookiecutter Python Package`_ project generator.

The project generation process used the `v.0.10.0 Template`_ and all required input
information was read from the `v0.10.0 biskotaki.yaml`_ configuration file.

From a developer's point of view, this release's code was produced as follows:

1. Run generator and replace all files in the local `biskotaki` repository checkout
2. Commit all the changes

For more, on the generator used, check the `documentation`, `repository`_ and `Template`_ links.

Generated Additions
-------------------

Enhance the CI config, by adding extra `checks` in the `Test Jobs` and
automating the `integration` with the `codecov.io` hosting service.

**Added checks**:

- Doing a 'Lint check' on the code
- Doing a 'Compliance check' of the resulting packaged distro against python best practices
- Gathering and sending the Test Suite results to the codecov.io service

**Code Coverage**:

Include `step` in all Test Jobs to gather and send Code Coverage data resulting from running
the Test Suite.

    `Codecov` is to Code Coverage, as `GA` is to Continuous Integration.

    Upon granting permission, `codecov` will start accepting the accumulated results (such as
    Code Coverage data) from all `Test Jobs` during a `build` and provide a web UI featuring
    interactive visualization of the python code and its `coverage` on user-defined granularity
    level, interactive charts of the `coverage` evolution and more.

Changes
^^^^^^^

ci
""
- enable lint, distro packaging QA & test results transimission to codecov.io CI service
- enable test workflow for tags matching pattern "v*", pull requests to dev & pushes to ci branch


0.0.1 (2022-05-09)
==================

| This is the first ever release of the **biskotaki** Python Package.
| The package is open source and is part of the **Biskotaki** Project.
| The project is hosted in a public repository on github at https://github.com/boromir674/biskotaki
| The project was scaffolded using the `Cookiecutter Python Package`_ (cookiecutter) Template at https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python

| Scaffolding included:

- **CI Pipeline** running on Github Actions at https://github.com/boromir674/biskotaki/actions
  - `Test Workflow` running a multi-factor **Build Matrix** spanning different `platform`'s and `python version`'s
    1. Platforms: `ubuntu-latest`, `macos-latest`
    2. Python Interpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`

- Automated **Test Suite** with parallel Test execution across multiple cpus.
  - Code Coverage
- **Automation** in a 'make' like fashion, using **tox**
  - Seamless `Lint`, `Type Check`, `Build` and `Deploy` *operations*


.. LINKS

.. _Cookiecutter Python Package: https://python-package-generator.readthedocs.io/en/master/

.. _Template: https://github.com/boromir674/cookiecutter-python-package/tree/master/src/cookiecutter_python

.. _v0.10.0 Template: https://github.com/boromir674/cookiecutter-python-package/tree/v0.10.0/src/cookiecutter_python

.. _v0.10.0 Cookiecutter Python Package: https://python-package-generator.readthedocs.io/en/v0.10.0/
.. _v1.4.0 Cookiecutter Python Package: https://python-package-generator.readthedocs.io/en/v1.4.0/

.. _v0.10.0 biskotaki.yaml: https://github.com/boromir674/cookiecutter-python-package/tree/v0.10.0/.github/biskotaki.yaml

.. _documentation: https://python-package-generator.readthedocs.io/

.. _repository: https://github.com/boromir674/cookiecutter-python-package
