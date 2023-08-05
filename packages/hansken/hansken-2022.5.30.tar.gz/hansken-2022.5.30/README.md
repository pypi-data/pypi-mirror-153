hansken.py
==========

`hansken.py` is a Python client to [Hansken](https://hansken.org)'s REST API, developed and maintained by the Netherlands Forensic Institute.

Installation
------------

`hansken.py` is hosted on PyPI, install it using `pip`:

``` plain
pip install hansken
```

The installation package defines extras to enable some additional features:

- **report**: utilities to help create reports in HTML and PDF formats;
- **mount**: enables the `mount` subcommand, creating FUSE mounts for data sources in a Hansken project;
- **kerberos**: enables the use of Kerberos single-sign-on authentication for environments that support it;
- **all**: installs all of the above.

These extras can be installed using `pip`:

``` plain
pip install hansken[all]
```
