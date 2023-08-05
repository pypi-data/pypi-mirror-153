# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optiseek']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.4,<2.0.0']

setup_kwargs = {
    'name': 'optiseek',
    'version': '0.1.0',
    'description': 'A collection of single objective optimization algorithms for multi-dimensional functions.',
    'long_description': '# optiseek\n\nAn open source collection of single-objective optimization algorithms for multi-dimensional functions.\n\nThe purpose of this library is to give users access to a variety of optimization algorithms with extreme ease of use and interoperability.\nThe parameters of each of the algorithms can be tuned by the users and there is a high level of input uniformity between algorithms of similar type.\n\n## Installation\n\n```bash\n$ pip install optiseek\n```\n\n## Usage\n\n`optiseek` provides access to numerous optimization algorithms that require minimal effort from the user. An example using the well-known particle swarm optimization algorithm can be as simple as this:\n\n```python\nfrom optiseek.metaheuristics import particle_swarm_optimizer\nfrom optiseek.testfunctions import booth\n\n# create an instance of the algorithm, set its parameters, and solve\nmy_algorithm = particle_swarm_optimizer(booth)  # create instance to optimize the booth function\nmy_algorithm.b_lower = [-10, -10] # define lower bounds\nmy_algorithm.b_upper = [10, 10] # define upper bounds\n\n# execute the algorithm\nmy_algorithm.solve()\n\n# show the results!\nprint(my_algorithm.best_value)\nprint(my_algorithm.best_position)\nprint(my_algorithm.completed_iter)\n```\n\nThis is a fairly basic example implementation without much thought put into parameter selection. Of course, the user is free to tune the parameters of the algorithm any way they would like.\n\n## Documentation\n\nFor full documentation, visit the [github pages site](https://acdundore.github.io/optiseek/).\n\n## License\n\n`optiseek` was created by Alex Dundore. It is licensed under the terms of the MIT license.\n\n## Credits and Dependencies\n\n`optiseek` is powered by [`numpy`](https://numpy.org/).',
    'author': 'Alex Dundore',
    'author_email': 'acdundore.5@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/optiseek',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
