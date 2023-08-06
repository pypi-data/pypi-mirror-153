# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['starlette_graphene3']
install_requires = \
['graphene>=3.0b6', 'graphql-core>=3.1,<3.3', 'starlette>=0.14.1']

setup_kwargs = {
    'name': 'starlette-graphene3',
    'version': '0.6.0',
    'description': 'Use Graphene v3 on Starlette',
    'long_description': '# starlette-graphene3\n\nA simple ASGI app for using [Graphene](https://github.com/graphql-python/graphene) v3 with [Starlette](https://github.com/encode/starlette) / [FastAPI](https://github.com/tiangolo/fastapi).\n\n![Test](https://github.com/ciscorn/starlette-graphene3/actions/workflows/test.yml/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/ciscorn/starlette-graphene3/branch/master/graph/badge.svg)](https://codecov.io/gh/ciscorn/starlette-graphene3)\n[![pypi package](https://img.shields.io/pypi/v/starlette-graphene3?color=%2334D058&label=pypi%20package)](https://pypi.org/project/starlette-graphene3)\n\nIt supports:\n\n- Queries and Mutations (over HTTP or WebSocket)\n- Subscriptions (over WebSocket)\n- File uploading (https://github.com/jaydenseric/graphql-multipart-request-spec)\n- GraphiQL / GraphQL Playground\n\nFile uploading requires `python-multipart` to be installed.\n## Alternatives\n\n- [tartiflette](https://github.com/tartiflette/tartiflette) &mdash; Python GraphQL Engine by dailymotion\n- [tartiflette-asgi](https://github.com/tartiflette/tartiflette-asgi)\n\n\n## Installation\n\n```bash\npip3 install -U starlette-graphene3\n```\n\n\n## Example\n\n```python\nimport asyncio\n\nimport graphene\nfrom graphene_file_upload.scalars import Upload\n\nfrom starlette.applications import Starlette\nfrom starlette_graphene3 import GraphQLApp, make_graphiql_handler\n\n\nclass User(graphene.ObjectType):\n    id = graphene.ID()\n    name = graphene.String()\n\n\nclass Query(graphene.ObjectType):\n    me = graphene.Field(User)\n\n    def resolve_me(root, info):\n        return {"id": "john", "name": "John"}\n\n\nclass FileUploadMutation(graphene.Mutation):\n    class Arguments:\n        file = Upload(required=True)\n\n    ok = graphene.Boolean()\n\n    def mutate(self, info, file, **kwargs):\n        return FileUploadMutation(ok=True)\n\n\nclass Mutation(graphene.ObjectType):\n    upload_file = FileUploadMutation.Field()\n\n\nclass Subscription(graphene.ObjectType):\n    count = graphene.Int(upto=graphene.Int())\n\n    async def subscribe_count(root, info, upto=3):\n        for i in range(upto):\n            yield i\n            await asyncio.sleep(1)\n\n\napp = Starlette()\nschema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)\n\napp.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))  # Graphiql IDE\n\n# app.mount("/", GraphQLApp(schema, on_get=make_playground_handler()))  # Playground IDE\n# app.mount("/", GraphQLApp(schema)) # no IDE\n```\n\n## GraphQLApp\n\n`GraphQLApp(schema, [options...])`\n\n```python\nclass GraphQLApp:\n    def __init__(\n        self,\n        schema: graphene.Schema,  # Requied\n        *,\n        # Optional keyword parameters\n        on_get: Optional[\n            Callable[[Request], Union[Response, Awaitable[Response]]]\n        ] = None,  # optional HTTP handler for GET requests\n        context_value: ContextValue = None,\n        root_value: RootValue = None,\n        middleware: Optional[Middleware] = None,\n        error_formatter: Callable[[GraphQLError], Dict[str, Any]] = format_error,\n        logger_name: Optional[str] = None,\n        playground: bool = False,  # deprecating\n        execution_context_class: Optional[Type[ExecutionContext]] = None,\n    ):\n```\n',
    'author': 'Taku Fukada',
    'author_email': 'naninunenor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ciscorn/starlette-graphene3',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
