============================
PyAMS security views package
============================

.. contents::


What is PyAMS?
==============

PyAMS (Pyramid Application Management Suite) is a small suite of packages written for applications
and content management with the Pyramid framework.

**PyAMS** is actually mainly used to manage web sites through content management applications (CMS,
see PyAMS_content package), but many features are generic and can be used inside any kind of web
application.

All PyAMS documentation is available on `ReadTheDocs <https://pyams.readthedocs.io>`_; source code
is available on `Gitlab <https://gitlab.com/pyams>`_ and pushed to `Github
<https://github.com/py-ams>`_. Doctests are available in the *doctests* source folder.


What is PyAMS security views?
=============================

PyAMS security is a pluggable Pyramid package used to handle application security management;
this package provides all browser-related views and content providers, including management
interface (based on PyAMS_zmi package), custom widgets and a small Cornice REST API to look for
principals.
