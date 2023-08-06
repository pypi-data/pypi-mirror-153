# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['logbesselk']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow>=2.6.5,<2.10']

extras_require = \
{'eval': ['tensorflow-probability>=0.16.0,<0.17.0'],
 'figs': ['matplotlib>=3.5.2,<4.0.0', 'seaborn>=0.11,<0.12']}

setup_kwargs = {
    'name': 'logbesselk',
    'version': '2.2.4',
    'description': 'Provide function to calculate the modified Bessel function of the second kind',
    'long_description': '# logbesselk\nProvide function to calculate the modified Bessel function of the second kind\nand its derivatives.\n\n\n## Author\nTAKEKAWA Takashi <takekawa@tk2lab.org>\n\n\n# Reference\nTakashi Takekawa, Fast parallel calculation of modified Bessel function\nof the second kind and its derivatives, SoftwareX, 17, 100923, 2022.\n\n\n### Require\n- python >= 3.7.1\n- tensorflow >= 2.6.1\n\n\n## Installation\n```shell\npip install logbesselk\n```\n\n\n## Examples\n```python\nimport tensorflow as tf\nfrom logbesselk.integral import log_bessel_k\n\n\nlog_k = log_bessel_k(v=1.0, x=1.0)\nlog_dkdv = log_bessel_k(v=1.0, x=1.0, 1, 0)\nlog_dkdx = log_bessel_k(v=1.0, x=1.0, 0, 1)\n\n\n# build graph at first execution time\nlog_bessel_k_tensor = tf.function(log_bessel_k)\nlog_bessel_dkdv_tensor = tf.function(lambda v, x: log_bessel_k(v, x, 1, 0))\nlog_bessel_dkdx_tensor = tf.function(lambda v, x: log_bessel_k(v, x, 0, 1))\n\nn = 1000\nfor i in range(10):\n    v = 10. ** (2. * tf.random.uniform((n,), dtype=tf.float64) - 1.\n    x = 10. ** (3. * tf.random.uniform((n,), dtype=tf.float64) - 1.)\n\n    log_k = log_bessel_k_tensor(v, x)\n    log_dkdv = log_bessel_dkdv_tensor(v, x)\n    log_dkdx = log_bessel_dkdx_tensor(v, x)\n```\n\n\n## Evaluation\n```shell\npython -m eval.prec\npython -m eval.time\npython -m eval.scale\npython -m eval.fig1\npython -m eval.fig2\npython -m eval.fig3\npython -m eval.fig4\npython -m eval.fig5\npython -m eval.fig6\npython -m eval.fig7\n```\n',
    'author': 'TAKEKAWA Takashi',
    'author_email': 'takekawa@tk2lab.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tk2lab/logbesselk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
