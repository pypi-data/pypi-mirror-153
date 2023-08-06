# django-society-elections
A Django app to run first-past-the-post elections for a university society


## Build and Installation

First, make sure you have the required version of Python (>=3.6) and you have created a virtual environment with `python -m venv venv`. To create migrations during development, run `make migrations`. This will also be done as part of the build and install stages.

To build: `make build` or alternatively `python setup.py build`

To install: `make install` or alternatively `python setup.py install`


## Using it in your Django project

You will need some settings for your Django project to make this work. If you want to use the emailing features you will need the following settings in your `settings.py`:

```python
# The root URL of your site without the trailing slash
SOCIETY_ELECTIONS_ROOT_URL = "http(s)://[hostname]"

# Prefix to your templates if you have written your own
SOCIETY_ELECTIONS_TEMPLATE_PREFIX = "elections/"

# Email address to send emails from
DEFAULT_FROM_EMAIL = "noreply@hostname"
```

You will also need any additional email configuration to get the emailing functionality working in your Django application. See https://docs.djangoproject.com/en/dev/topics/email/

Currently I have not written documentation for the various models, views, and urls. To understand the functionality whilst this is in progress I recommend you take a look at the source code for these classes and functions yourself.