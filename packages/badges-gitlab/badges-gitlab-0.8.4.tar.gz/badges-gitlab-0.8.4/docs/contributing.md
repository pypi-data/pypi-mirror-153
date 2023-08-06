# Contributing

Merge requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Below are instructions to set up the environment and testing.

## Installing Environment

This package uses the Pipenv Virtual Environment for managing 
the dependencies. They are all listed in the Pipfile.

Current supported version is Python >= 3.8, and this virtual environment
is configured for Python 3.8.

Install pipenv if you don't have it yet.

```bash
$ pip install -U pipenv
```

Clone the Repository and download the dependencies.

```bash
$ git clone https://gitlab.com/felipe_public/badges-gitlab.git
$ cd badges-gitlab
$ pipenv install --dev
```

## Testing

This project uses some tools for static code analysis and the python
embedded unittest for Unit Testing.

To run locally the static tests, a script was developed.
```bash
$ pipenv run statictest
```

To run unittests locally you can use a scripted short version.
```bash
$ pipenv run unit
```


### Dependencies Requirements

This package depends on the following dependencies:
- Python Gitlab API
- Anybadge
- Iso8601
- xmltodict
- toml