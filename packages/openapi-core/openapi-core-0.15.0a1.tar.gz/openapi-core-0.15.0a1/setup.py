# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapi_core',
 'openapi_core.casting',
 'openapi_core.casting.schemas',
 'openapi_core.contrib',
 'openapi_core.contrib.django',
 'openapi_core.contrib.falcon',
 'openapi_core.contrib.flask',
 'openapi_core.contrib.requests',
 'openapi_core.deserializing',
 'openapi_core.deserializing.media_types',
 'openapi_core.deserializing.parameters',
 'openapi_core.extensions',
 'openapi_core.extensions.models',
 'openapi_core.schema',
 'openapi_core.security',
 'openapi_core.spec',
 'openapi_core.templating',
 'openapi_core.templating.media_types',
 'openapi_core.templating.paths',
 'openapi_core.templating.responses',
 'openapi_core.testing',
 'openapi_core.unmarshalling',
 'openapi_core.unmarshalling.schemas',
 'openapi_core.validation',
 'openapi_core.validation.request',
 'openapi_core.validation.response']

package_data = \
{'': ['*']}

install_requires = \
['isodate',
 'more-itertools',
 'openapi-schema-validator>=0.2.0,<0.3.0',
 'openapi-spec-validator>=0.4.0,<0.5.0',
 'parse',
 'pathable>=0.4.0,<0.5.0',
 'werkzeug']

extras_require = \
{'django': ['django>=3.0'],
 'falcon': ['falcon>=3.0'],
 'flask': ['flask'],
 'requests': ['requests']}

setup_kwargs = {
    'name': 'openapi-core',
    'version': '0.15.0a1',
    'description': 'client-side and server-side support for the OpenAPI Specification v3',
    'long_description': '************\nopenapi-core\n************\n\n.. image:: https://img.shields.io/pypi/v/openapi-core.svg\n     :target: https://pypi.python.org/pypi/openapi-core\n.. image:: https://travis-ci.org/p1c2u/openapi-core.svg?branch=master\n     :target: https://travis-ci.org/p1c2u/openapi-core\n.. image:: https://img.shields.io/codecov/c/github/p1c2u/openapi-core/master.svg?style=flat\n     :target: https://codecov.io/github/p1c2u/openapi-core?branch=master\n.. image:: https://img.shields.io/pypi/pyversions/openapi-core.svg\n     :target: https://pypi.python.org/pypi/openapi-core\n.. image:: https://img.shields.io/pypi/format/openapi-core.svg\n     :target: https://pypi.python.org/pypi/openapi-core\n.. image:: https://img.shields.io/pypi/status/openapi-core.svg\n     :target: https://pypi.python.org/pypi/openapi-core\n\nAbout\n#####\n\nOpenapi-core is a Python library that adds client-side and server-side support\nfor the `OpenAPI Specification v3 <https://github.com/OAI/OpenAPI-Specification>`__.\n\nKey features\n************\n\n* **Validation** of requests and responses\n* Schema **casting** and **unmarshalling**\n* Media type and parameters **deserialization**\n* **Security** providers (API keys, Cookie, Basic and Bearer HTTP authentications)\n* Custom **deserializers** and **formats**\n* **Integration** with libraries and frameworks\n\n\nDocumentation\n#############\n\nCheck documentation to see more details about the features. All documentation is in the "docs" directory and online at `openapi-core.readthedocs.io <https://openapi-core.readthedocs.io>`__\n\n\nInstallation\n############\n\nRecommended way (via pip):\n\n::\n\n    $ pip install openapi-core\n\nAlternatively you can download the code and install from the repository:\n\n.. code-block:: bash\n\n   $ pip install -e git+https://github.com/p1c2u/openapi-core.git#egg=openapi_core\n\n\nUsage\n#####\n\nFirstly create your specification object:\n\n.. code-block:: python\n\n   from json import load\n   from openapi_core import OpenAPISpec as Spec\n\n   with open(\'openapi.json\', \'r\') as spec_file:\n      spec_dict = load(spec_file)\n\n   spec = Spec.create(spec_dict)\n\nRequest\n*******\n\nNow you can use it to validate against requests\n\n.. code-block:: python\n\n   from openapi_core.validation.request.validators import RequestValidator\n\n   validator = RequestValidator(spec)\n   result = validator.validate(request)\n\n   # raise errors if request invalid\n   result.raise_for_errors()\n\n   # get list of errors\n   errors = result.errors\n\nand unmarshal request data from validation result\n\n.. code-block:: python\n\n   # get parameters object with path, query, cookies and headers parameters\n   validated_params = result.parameters\n   # or specific parameters\n   validated_path_params = result.parameters.path\n\n   # get body\n   validated_body = result.body\n\n   # get security data\n   validated_security = result.security\n\nRequest object should be instance of OpenAPIRequest class (See `Integrations <https://openapi-core.readthedocs.io/en/latest/integrations.html>`__).\n\nResponse\n********\n\nYou can also validate against responses\n\n.. code-block:: python\n\n   from openapi_core.validation.response.validators import ResponseValidator\n\n   validator = ResponseValidator(spec)\n   result = validator.validate(request, response)\n\n   # raise errors if response invalid\n   result.raise_for_errors()\n\n   # get list of errors\n   errors = result.errors\n\nand unmarshal response data from validation result\n\n.. code-block:: python\n\n   # get headers\n   validated_headers = result.headers\n\n   # get data\n   validated_data = result.data\n\nResponse object should be instance of OpenAPIResponse class (See `Integrations <https://openapi-core.readthedocs.io/en/latest/integrations.html>`__).\n\nRelated projects\n################\n* `bottle-openapi-3 <https://github.com/cope-systems/bottle-openapi-3>`__\n   OpenAPI 3.0 Support for the Bottle Web Framework\n* `openapi-spec-validator <https://github.com/p1c2u/openapi-spec-validator>`__\n   Python library that validates OpenAPI Specs against the OpenAPI 2.0 (aka Swagger) and OpenAPI 3.0 specification\n* `openapi-schema-validator <https://github.com/p1c2u/openapi-schema-validator>`__\n   Python library that validates schema against the OpenAPI Schema Specification v3.0.\n* `pyramid_openapi3 <https://github.com/niteoweb/pyramid_openapi3>`__\n   Pyramid addon for OpenAPI3 validation of requests and responses.\n* `tornado-openapi3 <https://github.com/correl/tornado-openapi3>`__\n   Tornado OpenAPI 3 request and response validation library.\n',
    'author': 'Artur Maciag',
    'author_email': 'maciag.artur@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/p1c2u/openapi-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
