# NWON-Django-Toolbox

This package provides some Django additions that can be used across several projects.

## Settings

The Django Toolbox can be configured using the Django settings. We expect the key `NWON_DJANGO` that holds a dictionary. The dictionary must be of type `NWONDjangoSettings` that comes with this package (`nwon_django_toolbox.nwon_django_settings`). The keys mus be snake case or camel case.

For example like this

```python
NWON_DJANGO: NWONDjangoSettings = {
    "authorization_prefix": "Bearer",
    "logger_name": "your-log-name",
    "application_name": "application"
}
```

## Dependencies

The project has a bunch of dependencies that we use in most of our projects. In the end we have quite a lot and need to slim this down in the future.

Django related libraries are:

- Django (Obviously 🧠)
- django-polymorphic
- django-json-widget
- django-rest-polymorphic

For API documentation our models and serializer support two library which come as a dependency as well:

- drf-spectacular
- drf-yasg

On top we use a bunch of helper libraries

- Pydantic
- Pillow-PIL
- jsonref
- jsonschema-to-openapi
- pyhumps
- nwon-baseline

Package is meant for internal use at [NWON](https://nwon.de) as breaking changes may occur on version changes. This may change at some point but not for now 😇.

## Development Setup

We recommend developing using poetry.

This are the steps to setup the project with a local virtual environment:

1. Tell poetry to create dependencies in a `.venv` folder withing the project: `poetry config virtualenvs.in-project true`
1. Create a virtual environment using the local python version: `poetry env use $(cat .python-version)`
1. Install dependencies: `poetry install`

## Prepare Package

Before publishing the package we need to:

1. Clean dist folder
1. Bump up the version of the package
1. Build the package

Luckily we provide a script for doing all of this `python scripts/prepare.py patch`. Alternatively you can run the script in a poetry context `poetry run prepare patch`. The argument at the end defines whether you want a `patch`, `minor` or `major` version bump.

The final zipped data ends up in the `dist` folder.

## Publish Package 

Test package publication

1. Add test PyPi repository: `poetry config repositories.testpypi https://test.pypi.org/legacy/`
2. Publish the package to the test repository: `poetry publish -r testpypi`
3. Test package: `pip install --index-url https://test.pypi.org/simple/ nwon_baseline`

If everything works fine publish the package via `poetry publish`.
