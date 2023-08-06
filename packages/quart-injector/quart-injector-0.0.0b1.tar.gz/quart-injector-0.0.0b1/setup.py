# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quart_injector']

package_data = \
{'': ['*']}

install_requires = \
['injector>=0.19.0,<1.0.0', 'quart>=0.17.0,<1.0.0']

setup_kwargs = {
    'name': 'quart-injector',
    'version': '0.0.0b1',
    'description': '',
    'long_description': '# Quart Injector\n\n<p class="lead">\nDependency injecetion for quart apps.\n</p>\n\n## 🛠 Installing\n\n```\npoetry add quart-injector\n```\n\n## 🎓 Usage\n\n```py\nimport typing\nimport quart\nimport injector\nimport quart_injector\n\nGreeting = typing.NewType("Greeting", str)\n\n\ndef configure(binder: injector.Binder) -> None:\n    binder.bind(Greeting, to="Hello")\n\n\napp = quart.Quart(__name__)\n\n\n@app.route("/<name>")\n@app.route("/", defaults={"name": "World"})\nasync def greeting_view(greeting: injector.Inject[Greeting], name: str) -> str:\n    return f"{greeting} {name}!"\n\n\nquart_injector.wire(app, configure)\n```\n\n## 📚 Help\n\nSee the [Documentation][docs] or ask questions on the [Discussion][discussions] board.\n\n## ⚖️ Licence\n\nThis project is licensed under the [MIT licence][mit_licence].\n\nAll documentation and images are licenced under the \n[Creative Commons Attribution-ShareAlike 4.0 International License][cc_by_sa].\n\n## 📝 Meta\n\nThis project uses [Semantic Versioning][semvar].\n\n[docs]: https://quart-injector.artisan.io\n[discussions]: https://github.com/artisanofcode/python-quart-injector/discussions\n[mit_licence]: http://dan.mit-license.org/\n[cc_by_sa]: https://creativecommons.org/licenses/by-sa/4.0/\n[semvar]: http://semver.org/',
    'author': 'Daniel Knell',
    'author_email': 'contact@danielknell.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
