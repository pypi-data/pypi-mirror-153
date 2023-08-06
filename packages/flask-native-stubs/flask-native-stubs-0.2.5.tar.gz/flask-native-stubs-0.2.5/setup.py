# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_native_stubs', 'flask_native_stubs.stubgen']

package_data = \
{'': ['*']}

install_requires = \
['flask', 'requests', 'urllib3']

setup_kwargs = {
    'name': 'flask-native-stubs',
    'version': '0.2.5',
    'description': 'Call flask decorated functions like native ones.',
    'long_description': '# Flask Native Stubs\n\n- [中文版](README.zh.md)\n\nCall flask decorated functions like native ones.\n\nOverall workflow:\n\n1. Create server side functions, replace decorators from `@app.route(...)` to `@auto_route(...)`;\n2. Create a temp script to generate server stub file;\n3. Copy generated stub (folder) to client side;\n4. Client imports stub files and use them like native functions.\n\nExample for guide through:\n\n```\ndemo\n|= server\n   |- main.py\n|= client\n   |- main.py\n```\n\n1.  `server/main.py` source code:\n\n    ```python\n    from flask_native_stubs import app, auto_route\n\n    @auto_route()\n    def hello(a: int, b: str, c: float) -> list:\n        # type annotations are optional, but recommended.\n        return [a, b, c]\n\n    if __name__ == \'__main__\':\n        app.run(\'localhost\', 5000)\n    ```\n\n2.  Create a temp script like this:\n\n    In \'server/temp_stubgen.py\':\n\n    ```python\n    import os\n    from flask_native_stubs import enable_stubgen\n    from flask_native_stubs import generate_stub_files\n\n    enable_stubgen(project_root_path=os.getcwd())\n    #   will search `@auto_route` decorators only under \'~/server\'.\n\n    # explicit import modules which contains routed functions.\n    from main import hello\n    ...\n\n    os.mkdir(d := \'server_stubs\')\n    generate_stub_files(dir_o=d)\n    ```\n\n    1.  Run this script.\n    2.  It will generate \'server/server_stubs\' folder (contains a stub file named \'main.py\').\n\n        The stub file looks like:\n\n        ```python\n        """\n        Auto-generated stub file by [flask-native-stubs][1].\n\n        [1]: https://github.com/likianta/flask-native-stubs\n        """\n        from flask_native_stubs import add_route\n        from typing import Any\n\n        def hello(a: int, b: str, c: float) -> list: ...\n\n        [add_route(x) for x in (hello,)]\n        ```\n\n3.  Copy the generated stub to client side:\n\n    Now the directories are:\n\n    ```\n    demo\n    |= server\n       |- main.py\n       |- temp_stubgen.py\n       |= server_stubs  # 1. copy from\n           |- main.py\n    |= client\n       |- main.py\n       |= server_stubs  # 2. copy to\n           |- main.py\n    ```\n\n4.  Write your client side implementations with server stubs:\n\n    \'client/main.py\':\n\n    ```python\n    from flask_native_stubs import setup\n    from . import server_stubs as stubs\n\n    setup(host=\'localhost\', port=5000)\n    #   note: you should ask server admin to get the host and port.\n\n    def main():\n        result = stubs.hello(a=123, b=\'456\', c=7.89)\n        #   the ide works well with type hints :)\n        print(result)  # -> [123, \'456\', 7.89]\n\n    ...\n\n    if __name__ == \'__main__\':\n        main()\n    ```\n\n## How it works\n\nThis project is inspired by swagger codegen.\n\nI want to get both type hints support and the convenience of native functions calling style. So let the mechanism become truth by some delegate hooks underlay.\n\nHere are a few comparisons between swagger and flask-native-stubs:\n\n- Workflow:\n    - Swagger:\n        1. Draw a blueprint by configuration files;\n        2. Generate template code;\n        3. Override templates to implement server and client logics.\n    - Flask-native-stubs:\n        1. We have implemented a flask app;\n        2. Now generate stub files;\n        3. Let the client side interact with stubs.\n- *TODO:More...*\n\n*TODO:ExplainFlaskNativeStubsImplementations*\n\n## Cautions\n\n- Do not use `*args` and `**kwargs` in decorated functions:\n\n    ```python\n    # don\'t\n    @auto_route()\n    def xxx(a, b, c, *args, d=1, e=None, **kwargs):\n        ...\n    ```\n',
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/likianta/flask-native-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
