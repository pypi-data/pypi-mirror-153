.. meta::
    :description: Burin logging utility documentation

.. currentmodule:: burin

=====================
Burin Logging Utility
=====================

Burin (/ˈbyʊər ɪn, ˈbɜr-/byoor-in, bur-/) is a logging library that is meant to
add features and simplify usage compared to the Python standard library
:mod:`logging` package.  It can be used as a direct replacement in most cases.

The name Burin is based on the (originally French) name of a handheld chisel
like tool used for engraving.

Currently Python 3.6, 3.7, 3.8, 3.9, and 3.10 are all supported.  There are no
dependencies or additional requirements for Burin and it should work on any
platform that Python does.

An important aspect of Burin is an easy migration that allows changing from the
:mod:`logging` package to Burin without anything breaking in most use cases.
While class names may need to be changed this generally should work well.
Although some situations may require other small changes due to the added
features of Burin.

Using Burin to replace :mod:`logging` use in a program can be done gradually or
all at once.  Burin should not interfere with :mod:`logging` usage as its
internal references are all managed independently.  However; it's best to
ensure that they are not trying to log to the same file as this may cause
issues.

.. note::

    While some classes in Burin inherit from classes in the Python standard
    :mod:`logging` package they cannot be used interchangeably.

    Using classes from :mod:`logging` in Burin or vice-versa may cause
    exceptions or other issues.

.. note::

    Burin is still in early development and may change in backwards
    incompatible ways between minor release versions.  This should be rare as
    general compatibility with :mod:`logging` is desired to ease switching, but
    it is a good idea check the release notes when upgrading between minor
    (0.X.0) releases.


.. toctree::
    :maxdepth: 1
    :caption: Burin Documentation
    :hidden:

    self

.. toctree::
    :maxdepth: 1
    :caption: Introduction

    intro

.. toctree::
    :maxdepth: 1
    :caption: Library Documentation

    burin
    loggers
    handlers
    formatters
    log_records
    exceptions

.. toctree::
    :maxdepth: 1
    :caption: About

    project
    changelog
    license
    genindex
