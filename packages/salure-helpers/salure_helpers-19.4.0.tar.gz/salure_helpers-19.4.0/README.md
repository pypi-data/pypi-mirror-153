# HOW TO USE THE PACKAGES
The packages repository contains all the helper files which are build for projects of Salure. 
Sometimes, code in a project could be useful for other projects and will be added to the packages repository.
This readme describes the folder structure, the several packages and how to add new packages.
The docs section contains a detailed description per package.

## Directory structure
The directory structure in the packages is as follows:
- The datasets directory contains some usefull datasets like countries with iso code, currencies, etc.;
- The docs contain detailed documentation about server management, the packages itself, etc.;
- The salure_helpers folder contains the packages itself. The subdirectory connectors can be used for connectors between Profit and another system. The packages in the root of `/src` are usefull for a variety of tasks;

## How to create an updated pip package
https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi

## How to ship changes locally for testing purposes
When you want to test changes you have made locally before releasing a new version, run install_locally.sh (make sure you have changed the setup number already).
Input the customer name in the command prompt that will open and the package will be placed in the customer directory.
Then rebuild your dockerfile, which should include the following lines below the `pip install requirements` part but above the `copy . /app` part:.
```
COPY ["salure_helpers*", "."]
RUN pip3 install salure_helpers --find-links . salure_helpers --upgrade
```
This will install the version locally in your customer docker container so you can test it first before releasing.

## How to ship changes
When you commit a change, take the following in mind. The versioning we use is called semantic versioning. More information can be found on https://semver.org/ 

Given a version number MAJOR.MINOR.PATCH, increment the:
```
    1. MAJOR version when you make incompatible API changes,
    2. MINOR version when you add functionality in a backwards-compatible manner, and
    3. PATCH version when you make backwards-compatible bug fixes.
```
1. A normal version number MUST take the form X.Y.Z where X, Y, and Z are non-negative integers, and MUST NOT contain leading zeroes. X is the major version, Y is the minor version, and Z is the patch version. Each element MUST increase numerically. For instance: 1.9.0 -> 1.10.0 -> 1.11.0.
1. Patch version Z (x.y.Z | x > 0) MUST be incremented if only backwards compatible bug fixes are introduced. A bug fix is defined as an internal change that fixes incorrect behavior.
1. Minor version Y (x.Y.z | x > 0) MUST be incremented if new, backwards compatible functionality is introduced to the public API. It MUST be incremented if any public API functionality is marked as deprecated. It MAY be incremented if substantial new functionality or improvements are introduced within the private code. It MAY include patch level changes. *Patch version MUST be reset to 0 when minor version is incremented*.
1. Major version X (X.y.z | X > 0) MUST be incremented if any backwards incompatible changes are introduced to the public API. It MAY include minor and patch level changes. *Patch and minor version MUST be reset to 0 when major version is incremented.*

## Create a new release (for legacy versions)
When we create a new release, we need to create a seperate branch for the current release. Then it's easy to update old releases with bugs etc. Do the following
* Create a new branche with as type 'release' and the number of the major version. For example, if you create version 9, before you do that, create a branch named release/8
* Rename in the the file `bitbucket-pipelines.yml` on line 10 `master` into the release name, for example `release/8`

## Changelog
See commit history