# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sain']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sain',
    'version': '0.0.1',
    'description': 'Standard Rust core types implementations for Python.',
    'long_description': '# sain\nA pure Python package that implements standard Rust core types for Python.\n\n\n## Install\nYou\'ll need Python 3.8 or higher.\n\nStill not on PyPI\n```rs\n$ pip install git+https://github.com/nxtlo/sain\n```\n\n## Example\n```py\nimport sain\n\n#[cfg_attr(target_os = unix)]\n@sain.cfg_attr(target_os="unix")\ndef run_when_unix() -> None:\n    import uvloop\n    uvloop.install()\n\n# If this returns True, run_when_unix will run, otherwise returns.\nif sain.cfg(requires_modules=("dotenv", ...), python_version=(3, 9, 6)):\n    # Stright up replace typing.Optional[int]\n    def inner() -> sain.Some[int]:\n        return sain.Some(1)\n\n# If the Some[T] contained value is `None`, This raises RuntimeError.\nvalue: int = inner().expect("Still None")\n\nas_none: sain.Some[str] = sain.Some(None)  # type hint is fine.\nassert as_none.is_none()\n```\n\n### Defaults\nA protocol that types can implement which have a default value.\n\n```py\nimport sain\n\nclass DefaultCache(sain.Default[dict[str, int]]):\n    # One staticmethod must be implemented and must return the same type.\n    @staticmethod\n    def default() -> dict[str, int]:\n        return {\'yo\': 999}\n```\n\n\n### Iter\nTurns normal iterables into `Iter` type.\n\n```py\nimport sain\n\nf = sain.Iter([1,2,3])\n# or f = sain.into_iter([1,2,3])\nassert 1 in f\n\nfor item in f.take_while(lambda i: i > 1):\n    print(item)\n```\n\n### Why\ni like Rust coding style :p\n\n### Notes\nSince Rust is a compiled language, Whatever predict returns False will not compile.\n\nBut there\'s no such thing as this in Python, So `RuntimeError` will be raised and whatever was predicated will not run.\n',
    'author': 'nxtlo',
    'author_email': 'dhmony-99@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nxtlo/sain',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
