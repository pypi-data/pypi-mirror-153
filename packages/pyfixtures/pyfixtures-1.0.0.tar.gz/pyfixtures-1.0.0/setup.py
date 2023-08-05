# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfixtures']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfixtures',
    'version': '1.0.0',
    'description': 'Pytest style fixtures outside of Pytest.',
    'long_description': '# Fixtures\n\n[Pytest](https://docs.pytest.org/en/7.1.x/) style [fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) outside of Pytest.\n\n```python\nimport asyncio\nfrom pathlib import Path\nfrom py_fixtures import fixture, FixtureScope\n\n@fixture\ndef tmpdir() -> Path:\n    path = Path("temp")\n    path.mkdir()\n    try:\n        yield path\n    finally:\n        path.unlink()\n\n\n\ndef mk_temp_files(tmpdir: Path):\n    tmp_file = tmpdir/"tempfile.txt"\n    tmp_file.touch()\n\n\nasync def main():\n    async with FixtureScope() as scope:\n        operation = await scope.bind(mk_temp_files)\n        await operation()\n\n\nasyncio.run(main())\n\n```\n',
    'author': 'Ian Boyes',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/virtool/fixtures',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
