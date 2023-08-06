# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_injector']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.70.0', 'injector>=0.19.0']

setup_kwargs = {
    'name': 'fastapi-injector',
    'version': '0.2.1',
    'description': 'python-injector integration for FastAPI',
    'long_description': '# FastAPI Injector\n\n![Workflow status](https://github.com/matyasrichter/fastapi-injector/actions/workflows/build.yml/badge.svg?branch=main)\n[![Coverage status](https://coveralls.io/repos/github/matyasrichter/fastapi-injector/badge.svg)](https://coveralls.io/github/matyasrichter/fastapi-injector?branch=main)\n\nIntegrates [injector](https://github.com/alecthomas/injector) with [FastAPI](https://github.com/tiangolo/fastapi).\n\nGithub: https://github.com/matyasrichter/fastapi-injector  \nPyPI: https://pypi.org/project/fastapi-injector/\n\n## Installation\n\n```shell\npip install fastapi-injector\n```\n\n## Usage\n\nWhen creating your FastAPI app, attach the injector to it:\n\n```python\n# app.py\nfrom fastapi import FastAPI\nfrom injector import Injector\nfrom fastapi_injector import attach_injector\n\n\ndef create_app(injector: Injector) -> FastAPI:\n    app = FastAPI()\n    app.include_router(...)\n    ...\n    attach_injector(app, injector)\n    return app\n```\n\nThen, use `Injected` in your routes. Under the hood, `Injected` is `Depends`, so you can use it anywhere `Depends` can be used. In the following example, `InterfaceType` is\nsomething you\'ve bound an implementation to in your injector instance.\n\n```python\nfrom fastapi import APIRouter\nfrom fastapi_injector import Injected\n\nrouter = APIRouter()\n\n\n@router.get("/")\nasync def get_root(integer: int = Injected(InterfaceType)):\n    return integer\n```\n\nA more complete example could look like this (your FastAPI code only depends on `InterfaceType`,\nits implementation only depends on a domain layer port etc.):\n\n```python\n# ------------------------\n# interface.py\nimport abc\nfrom abc import abstractmethod\n\n\nclass SomeInterface(abc.ABC):\n    @abstractmethod\n    async def create_some_entity(self) -> None:\n        """Creates and saves an entity."""\n\n\n# ------------------------\n# service.py\nimport abc\nfrom .interface import SomeInterface\n\n\nclass SomeSavePort(abc.ABC):\n    @abc.abstractmethod\n    async def save_something(self, something: Entity) -> None:\n        """Saves an entity."""\n\n\nclass SomeService(SomeInterface):\n    def __init__(self, save_port: Inject[SomeSavePort]):\n        self.save_port = save_port\n\n    async def create_some_entity(self) -> None:\n        entity = Entity(attr1=1, attr2=2)\n        await self.save_port.save_something(entity)\n\n\n# ------------------------\n# repository.py\nfrom .service import SomeSavePort\n\n\nclass SomeRepository(SomeSavePort):\n    async def save_something(self, something: Entity) -> None:\n# code that saves the entity to the DB\n```\n\n## Testing with fastapi-injector\n\nTo use your app in tests with overridden dependencies, modify the injector before each test:\n\n```python\n# ------------------------\n# app entrypoint\nimport pytest\nfrom injector import Injector\n\napp = create_app(inj)\n\nif __name__ == "__main__":\n    uvicorn.run("app", ...)\n\n\n# ------------------------\n# composition root\ndef create_injector() -> Injector:\n    inj = Injector()\n    # note that this still gets executed,\n    # so if you need to get rid of a DB connection, for example,\n    # you would need to use a callable provider.\n    inj.binder.bind(int, 1)\n    return inj\n\n\n# ------------------------\n# tests\nfrom fastapi import FastAPI\nfrom fastapi.testclient import TestClient\nfrom path.to.app.factory import create_app\n\n\n@pytest.fixture\ndef app() -> FastAPI:\n    inj = Injector()\n    inj.binder.bind(int, 2)\n    return create_app(inj)\n\n\ndef some_test(app: FastAPI):\n    # use test client with the new app\n    client = TestClient(app)\n```\n',
    'author': 'Matyas Richter',
    'author_email': 'matyas@mrichter.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matyasrichter/fastapi-injector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
