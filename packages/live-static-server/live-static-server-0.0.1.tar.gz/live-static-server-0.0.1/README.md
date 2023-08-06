# live-static-server

live static server


## Installation


## Usage


## Development Tips

* init env:     python3 -m pip install --upgrade pipenv
* init shell:   pipenv shell
* init project: pipenv install
* build:        python -m build
* upload test:  python -m twine upload --repository testpypi dist/*
* upload prod:  python -m twine upload dist/*

* use test:     pip install --index-url https://test.pypi.org/simple/ --no-deps package-name-USER_NAME
* use prod:     pip install package-name


<!--
## Roadmap

If you have ideas for releases in the future, it is a good idea to list them in the README.
-->

## Changelog

[Changelog](./CHANGELOG.md)


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
