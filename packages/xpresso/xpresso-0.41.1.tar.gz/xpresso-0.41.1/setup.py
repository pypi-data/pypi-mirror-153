# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xpresso',
 'xpresso._utils',
 'xpresso.binders',
 'xpresso.binders._binders',
 'xpresso.dependencies',
 'xpresso.middleware',
 'xpresso.openapi',
 'xpresso.routing']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.4.0,<5',
 'di>=0.68.5,<0.69.0',
 'pydantic>=1.9.0,<2.0.0',
 'starlette>=0.17.1,<1']

extras_require = \
{':python_version < "3.9"': ['typing-extensions>=3']}

setup_kwargs = {
    'name': 'xpresso',
    'version': '0.41.1',
    'description': 'A developer centric, performant Python web framework',
    'long_description': '<p align="center">\n  <a href="https://www.xpresso-api.dev"><img src="https://github.com/adriangb/xpresso/raw/main/docs/assets/images/xpresso-title.png" alt="Xpresso"></a>\n</p>\n\n<p align="center">\n<a href="https://github.com/adriangb/xpresso/actions?query=workflow%3ACI%2FCD+event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/adriangb/xpresso/actions/workflows/workflow.yaml/badge.svg?event=push&branch=main" alt="Test">\n</a>\n<a href="https://codecov.io/gh/adriangb/xpresso" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/adriangb/xpresso?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/xpresso" target="_blank">\n    <img src="https://img.shields.io/pypi/v/xpresso?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/xpresso" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/xpresso.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\nXpresso is an ASGI web framework built on top of [Starlette], [Pydantic] and [di], with heavy inspiration from [FastAPI].\n\nSome of the standout features are:\n\n- ASGI support for high performance (within the context of Python web frameworks)\n- OpenAPI documentation generation\n- Automatic parsing and validation of request bodies and parameters, with hooks for custom extractors\n- Full support for [OpenAPI parameter serialization](https://swagger.io/docs/specification/serialization/)\n- Highly typed and tested codebase with great IDE support\n- A powerful dependency injection system, backed by [di]\n\n## Requirements\n\nPython 3.7+\n\n## Installation\n\n```shell\npip install xpresso\n```\n\nYou\'ll also want to install an ASGI server, such as [Uvicorn].\n\n```shell\npip install uvicorn\n```\n\n## Example\n\nCreate a file named `example.py`:\n\n```python\nfrom pydantic import BaseModel\nfrom xpresso import App, Path, FromPath, FromQuery\n\nclass Item(BaseModel):\n    item_id: int\n    name: str\n\nasync def read_item(item_id: FromPath[int], name: FromQuery[str]) -> Item:\n    return Item(item_id=item_id, name=name)\n\napp = App(\n    routes=[\n        Path(\n            "/items/{item_id}",\n            get=read_item,\n        )\n    ]\n)\n```\n\nRun the application:\n\n```shell\nuvicorn example:app\n```\n\nNavigate to [http://127.0.0.1:8000/items/123?name=foobarbaz](http://127.0.0.1:8000/items/123?name=foobarbaz) in your browser.\nYou will get the following JSON response:\n\n```json\n{"item_id":123,"name":"foobarbaz"}\n```\n\nNow navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to poke around the interactive [Swagger UI] documentation:\n\n![Swagger UI](docs/readme_example_swagger.png)\n\nFor more examples, tutorials and reference materials, see our [documentation].\n\n## Inspiration and relationship to other frameworks\n\nXpresso is mainly inspired by FastAPI.\nFastAPI pioneered several ideas that are core to Xpresso\'s approach:\n\n- Leverage Pydantic for JSON parsing, validation and schema generation.\n- Leverage Starlette for routing and other low level web framework functionality.\n- Provide a simple but powerful dependency injection system.\n- Use that dependency injection system to provide extraction of request bodies, forms, query parameters, etc.\n\nXpresso takes these ideas and refines them by:\n\n- Decoupling the dependency injection system from the request/response cycle, leading to an overall much more flexible and powerful dependency injection system, packaged up as the standalone [di] library.\n- Decoupling the framework from Pydantic by using `Annotated` ([PEP 593]) instead of default values (`param: FromQuery[str]` instead of `param: str = Query(...)`).\n- [Middleware on Routers] so that you can use generic ASGI middleware in a routing-aware manner (for example, installing profiling middleware on only some paths without using regex matching).\n- Support for [lifespans on any Router or mounted App] (this silently fails in FastAPI and Starlette)\n- [dependency injection into the application lifespan] and support for [multiple dependency scopes].\n- Formalizing the framework for extracting parameters and bodies from requests into the [Binder API] so that 3rd party extensions can do anything the framework does.\n- Support for [customizing parameter and form serialization].\n- Better performance by implementing [dependency resolution in Rust], [executing dependencies concurrently] and [controlling threading of sync dependencies on a per-dependency basis].\n\n## Current state\n\nThis project is under active development.\nIt should not be considered "stable" or ready to be used in production.\nIt is however ready for experimentation and learning!\n\n### What is implemented and mostly stable?\n\n1. Extraction and OpenAPI documentation of parameters (query, headers, etc.) and request bodies (including multipart requests).\n1. Parameter serialization.\n1. Routing, including applications, routers and routes.\n1. Dependency injection and testing utilities (dependency overrides).\n\nMost of this APIs will be _generally_ stable going forward, although some minor aspects like argument names will probably change at some point.\n\n### What is not implemented or unstable?\n\n1. Low-level API for binders (stuff in `xpresso.binders`): this is public, but should be considered experimental and is likely to change. The high level APIs (`FromPath[str]` and `Annotated[str, PathParam(...)]`) are likely to be stable.\n1. Security dependencies and OpenAPI integration. This part used to exist, but needed some work. It is planned for the future, but we need to think about the scope of these features and the API.\n\n[Starlette]: https://github.com/encode/starlette\n[Pydantic]: https://github.com/samuelcolvin/pydantic/\n[FastAPI]: https://github.com/adriangb/xpresso\n[di]: https://github.com/adriangb/di\n[Uvicorn]: http://www.uvicorn.org/\n[documentation]: https://www.xpresso-api.dev/\n[Swagger UI]: https://swagger.io/tools/swagger-ui/\n[dependency injection into the application lifespan]: https://xpresso-api.dev/latest/tutorial/lifespan\n[multiple dependency scopes]: https://xpresso-api.dev/latest/tutorial/dependencies/scopes/\n[dependency resolution in Rust]: https://github.com/adriangb/graphlib2\n[executing dependencies concurrently]: https://xpresso-api.dev/latest/advanced/dependencies/performance/#concurrent-execution\n[controlling threading of sync dependencies on a per-dependency basis]: https://xpresso-api.dev/latest/advanced/dependencies/performance/#sync-vs-async\n[PEP 593]: https://www.python.org/dev/peps/pep-0593/\n[Binder API]: https://xpresso-api.dev/latest/advanced/binders/\n[customizing parameter and form serialization]: https://xpresso-api.dev/latest/tutorial/query_params/#customizing-deserialization\n[lifespans on any Router or mounted App]: https://xpresso-api.dev/latest/tutorial/lifespan/\n[Middleware on Routers]: https://xpresso-api.dev/0.14.1/tutorial/middleware/#middleware-on-routers\n\nSee this release on GitHub: [v0.41.1](https://github.com/adriangb/xpresso/releases/tag/0.41.1)\n',
    'author': 'Adrian Garcia Badaracco',
    'author_email': 'adrian@adriangb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adriangb/xpresso',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
