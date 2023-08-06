# admobilizeapis python package generator
Repo contains python package generator for [admobilizeapis](https://bitbucket.org/admobilize/admobilizeapis) proto interface.

### Install

`$ pip install admobilizeapis`

### Requirements
* Python 3
* Pip 3
* Tip: Use [Virtualenv](https://virtualenv.pypa.io/en/latest/) to not mess your python machine

### Dependencies
* MacOS only: `$ brew install gnu-sed`
* External libraries: `$ pip install google-api-core protobuf`

### Before build
* Clone submodules: `$ git submodule update --init --recursive`
* The submodules will relies on `./third_party/` folder. `./admobilizeapis/` also is a submodule, but for some way (certainly project decision) is present outside of `./third_party/` folder.
* If you need to build a specific branch of `./admobilizeapis/` please go to that folder and do `$ git checkout <TARGET_BRANCH>` execute the build process.

### Building the python package
* Run (The second param is a version number of your choice): `$ ./build.sh 0.0.30`
* The `./tmp/dist/` folder will now contain the built package that can be installed in upstream projects. To do the installation run: `$ pip install ./tmp/dist/admobilizeapis-0.0.30.tar.gz`.
