# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plausible_proxy', 'plausible_proxy.templatetags', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2', 'requests>=2,<3']

setup_kwargs = {
    'name': 'django-plausible-proxy',
    'version': '0.3.0',
    'description': 'Django module to proxy requests to Plausible Analytics.',
    'long_description': '# Django Plausible Proxy\n\nDjango application to proxy requests and send server-side events to Plausible Analytics. Plays well with self-hosted and the managed cloud service.\n\n## Proxying\n\nProxying allows a project owner concerned about missing data seeing a more complete picture. See [Adblockers and using a proxy for analytics](https://plausible.io/docs/proxy/introduction) for the detailed outline of the problem and solution.\n\nWhen installed and configured in `settings.py` and `urls.py`, the app proxies the HTTP requests as such:\n\n```\nhttps://<yourdomain.com>/js/script.js -> https://plausible.io/js/script.js\nhttps://<yourdomain.com>/api/event    -> https://plausible.io/api/event\n```\n\n## Server-side events\n\nTrack on the server side events that can\'t be tracked otherwise, such as API requests.\n\n```python\nfrom plausible_proxy import send_custom_event\n...\nsend_custom_event(request, name="Register", props={"plan": "Premium"})\n```\n\n## Installation\n\nInstall the package from PyPI.\n\n```shell\npip install django-plausible-proxy\n```\n\nConfigure Django setting in the `settings.py`.\n\n```python\n\n# Register the app to enable {% plausble %} templatetag.\nINSTALLED_APPS = [\n    # ...\n    "plausible_proxy"\n    # ...\n]\n\n# Optionally, define a default value for Plausible domain to provide a default value\n# for the Plausible domain and the `send_custom_event()` function.\nPLAUSIBLE_DOMAIN = "yourdomain.com"\n\n# Optionally, define the plausible endpoint that you would like to post to.\n# This is useful if you are self-hosting plausible.\nPLAUSIBLE_BASE_URL = "https://plausible.io"\n\n# Optionally, define the value for the script prefix. The default value is "js". When\n# you include the script to the page with the {% plausible %} templatetag, it becomes\n# available as "<script src=\'${PLAUSIBLE_SCRIPT_PREFIX}/script.js\'></script>". E.g.,\n# "<script src=\'js/script.js\'></script>"\n#\n# Overriding PLAUSIBLE_SCRIPT_PREFIX is helpful to avoid clashes with another script\n# of your site that may become available under the same name.\n\nPLAUSIBLE_SCRIPT_PREFIX = "plsbl/js"\n```\n\nUpdate `urls.py`.\n\n\n```python\nfrom django.urls import include, path\n\nurlpatterns = [\n    # ...\n    path("", include("plausible_proxy.urls")),\n    # ...\n]\n```\n\nUpdate your base HTML template to include the plausible templatetag.\n\n```html\n{% load plausible %}\n<html>\n  <head>\n      ...\n      {% plausible script=\'script.js\' %}\n  </head>\n```\n\n## API reference\n\n\n### **`{% plausible %}`**\n\nA templatetag to include the Plausible analytics script to the page.\n\nArguments:\n\n- `domain` (default to `settings.PLAUSIBLE_DOMAIN`): defines the `data-domain` parameter, the is the domain for the Plausible analytics.\n- `script` (default to `script.js`): defines the Plausible script to use. See [Script extensions for enhanced measurement](https://plausible.io/docs/script-extensions) for the list of alternative script names and what they can track for you.\n\nUsage example:\n\n```html\n{% load plausible %}\n<html>\n  <head>\n      ...\n      {% plausible domain=\'example.com\' script=\'script.outbound-links.js\' %}\n  </head>\n```\n\n### `plausible_proxy.services.`**`send_custom_event()`**\n\nend a custom event to Plausible and return successful status.\n\nSee [Plausible events API](https://plausible.io/docs/events-api) for more information\n\nArguments:\n\n- `request` (HttpRequest): Original Django HTTP request. Will be used to create X-Forwarded-For and User-Agent headers.\n- `name` (string): Name of the event. Can specify `pageview` which is a special type of event in Plausible. All other names will be treated as custom events.\n- `domain` (optional string): Domain name of the site in Plausible. The value from settings.PLAUSIBLE_DOMAIN is used by default.\n- `url` (optional string): URL of the page where the event was triggered. If not provided, the function extracts the URL from the request. If the URL contains UTM parameters, they will be extracted and stored. If URL is not set, will be extracted from the request.\n- `referrer` (optional string): Referrer for this event.\n- `screen_width` (optional integer): Width of the screen.\n- `props` (optional dict): Custom properties for the event. See: [Using custom props](https://plausible.io/docs/custom-event-goals#using-custom-props).\n\nReturns: True if request was accepted successfully.\n\nExample:\n\n```python\ndef vote(request, candidate_id):\n    candidate = get_object_or_404(Candidate, pk=candidate_id)\n    send_custom_event(request, \'vote\', props={"candidate": candidate.full_name})\n    ...\n```\n\n## Contributors\n\n<a href="https://github.com/imankulov/django-plausible-proxy/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=imankulov/django-plausible-proxy" />\n</a>\n',
    'author': 'Roman Imankulov',
    'author_email': 'roman.imankulov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imankulov/django-plausible-proxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.8,<4.0.0',
}


setup(**setup_kwargs)
