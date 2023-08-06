# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lb_health_check']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2']

setup_kwargs = {
    'name': 'django-lb-health-check',
    'version': '1.0.1',
    'description': 'Middleware based health check for Django',
    'long_description': '# Django Load Balancer Health Check\n\nAliveness check for Django that bypasses ALLOWED_HOSTS for the purposes of load balancers\n\n## Purpose\n\nWhen running on some app platforms and behind some load balancers, it is often the case that the host header is not set appropriately for health checks. When these platforms perform an HTTP health check without the proper host header an *error 400 bad request* will be returned by Django. This package provides a method to allow for for a simple "aliveness" health check that bypasses the `ALLOWED_HOSTS` protections. `ALLOWED_HOSTS` protection is bypassed only for the status aliveness check URL and not for any other requests.\n\nThis package is not an alternative to something like [django-health-check](https://github.com/KristianOellegaard/django-health-check), but is instead a better alternative than the TCP health check that is the default on many load balancers. The TCP health checks can only see if your uWSGI/Gunicorn/Uvicorn/etc server is alive, while this package ensures that requests are being properly routed to Django.\n\n## How it works\n\nThis package works by returning an HTTP response from a middleware class before Django\'s common middleware performs the host check and before the security middleware does HTTPS checks. The Django URL routing system is also bypassed since that happens "below" all middleware. During request processing, *django-lb-health-check* checks if the request is a *GET* request and matches `settings.ALIVENESS_URL`. If it is, a static plain text "200 OK" response is returned bypassing any other processing.\n\n\n## Usage\n\nInstall *django-lb-health-check*\n\n```shell\npip install django-lb-health-check\n```\n\nAdd *lb_health_check* to your middleware at the top position. It **must** be above *django.middleware.common.CommonMiddleware* and in most cases should be above *django.middleware.security.SecurityMiddleware*. Security middleware does things like check for HTTPS, which is often missing in health checks from load balancers. Common middleware does the checks against ALLOWED_HOSTS.\n\n```python\nMIDDLEWARE = [\n    \'lb_health_check.middleware.AliveCheck\', #  <- New middleware here\n    \'django.middleware.security.SecurityMiddleware\',\n    \'django.contrib.sessions.middleware.SessionMiddleware\',\n    \'django.middleware.common.CommonMiddleware\',\n    \'django.middleware.csrf.CsrfViewMiddleware\',\n    \'django.contrib.auth.middleware.AuthenticationMiddleware\',\n    \'django.contrib.messages.middleware.MessageMiddleware\',\n    \'django.middleware.clickjacking.XFrameOptionsMiddleware\',\n]\n```\n\nSet the URL you want to use for your aliveness check. Note that a GET request to this URL **will** shadow any other route you have defined through the Django URL mapper. Aliveness URL can be a string for a single health check URL or a list of strings if you want the aliveness check to run from multiple URLs. The multiple URL strategy is helpful if you are changing the URL of the endpoint by allowing both the old and new URLs to be checked.\n\n```python\nALIVENESS_URL = "/health-check/"\n```\n\nTest your health check after starting your server:\n\n```bash\ncurl localhost:8000/health-check/\nOK\n```\n\nNote that the example app has *lb_health_check* in INSTALLED_APPS. This is only necessary for testing purposes - the app does not use any Django models, admin, views, URL routing, or the like that would require it to be listed in INSTALLED_APPS.',
    'author': 'Adam Peacock',
    'author_email': 'adam@thepeacock.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Hovercross/django-lb-health-check',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
