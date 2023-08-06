# Serviceinstaller Changelog


## Version 0.2.0 (2022-06-03)

Stable release supporting Python 3.6-3.10.

### Core features

* Allow execution on non-native platforms with the skip_enable parameter
* Add output_path parameter to main function to set a custom output dir
* Return actual output path for consumption by callers
* Defer logging configuration to callers rather than handling it internally

### Bug fixes

* Fix bug creating parent directories one level too shallow
* Fix bug setting permissions/owner on parent directory, not service file
* Handle permission error with chown and being unsupported on current platform

### Infrastructure

* Officially document support for Python 3.6-3.10 (up from only 3.6-3.8)
* Modernize packaging infrastructure for PEP 517 w/pyproject.toml & setup.cfg
* Revise Readme to reflect version support and other improvements

### Under the hood

* Update pylint config with suite of plugins and remove unneeded disable
* Update Release Guide to use more modern and robust procedure
* Further minor related refactoring



## Version 0.1.4 (2022-05-31)

Bugfix release to fix a critical packaging issue:

* Ensure the actual Python module is included in distribution packages



## Version 0.1.3 (2020-04-23)

Bugfix release to address one minor issue:

* Fix issue with timeout being set too short for low-end systems (e.g. Pi Zero)



## Version 0.1.2 (2020-03-10)

Bugfix release to fix various issues:

* Fix serious bug when filename, services_enable or services_disable is None
* Minor refinements to setup.py
* Ensure full project is pylint-clean and add .pylintrc



## Version 0.1.1 (2019-10-28)

Minor bugfix release to fix a one significant bug on Debian:

* Don't add group name to avoid issues where group doesn't exist, e.g. Debian



## Version 0.1.0 (2019-10-06)

Initial deployed release for Brokkr and Sindri, with the following features:

* Automatically generate service unit file for Systemd
* Reload daemon and enable service
* Enable and disable other services as needed
* Detailed, controllable logging and error handling
* Extensible to other service systems
