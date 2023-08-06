============================
Logging Utility for InfluxDB
============================


Utility to write logging to influxdb2 in order to gather some application stats. After using this utility, user can create dashboard in Grafana with InfluxDB.


* Free software: MIT license
* Documentation: https://log2influx.readthedocs.io.


Features
--------

* A helper to log information to InfluxDB2 for further report purpose.
* The funcitons here has handle errors, if anything goes wrong it still return and won't break main program logic. But the information won't be recorded in InfluxDB.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

============================
Developer's Causion
============================

This package is hosted by pypi public. Do not include any sensitive information in this project.
