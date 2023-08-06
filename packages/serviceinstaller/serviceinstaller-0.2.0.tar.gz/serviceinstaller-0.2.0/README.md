# Serviceinstaller

A simple Python module to automate the installation of system services, currently compatible with Systemd services on Linux.
Used by the [Brokkr](https://github.com/project-mjolnir/brokkr/) and [Sindri](https://github.com/project-mjolnir/sindri/) packages as part of [Project Mjolnir](https://github.com/project-mjolnir/).

See the ``install_service()`` docstring in [``serviceinstaller.py``](./serviceinstaller.py) for more details on usage.


## License

Copyright (c) 2019-2022 C.A.M. Gerlach and contributors

This project is distributed under the terms of the MIT (Expat) License; see the [``LICENSE.txt``](./LICENSE.txt) for more details.


## Installation and Setup

Compatible and tested with Python 3.6-3.10, and should work with 3.11.
Currently, the actual service installation itself only supports Linux, but it can generate and write the service file (e.g. for testing, bundling or cross-compilation) on any platform.
No dependencies required.
