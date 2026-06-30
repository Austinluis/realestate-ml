# Django Project Package

This directory contains the root Django project configuration.

## Files

- `settings.py`: installed apps, middleware, database settings, static/media settings, authentication redirects, and Django REST Framework defaults.
- `urls.py`: root URL routing for admin, accounts, dashboard, properties, predictions, and local media serving in debug mode.
- `wsgi.py`: WSGI application entry point used by Gunicorn in deployment.
- `__init__.py`: marks this directory as a Python package.
