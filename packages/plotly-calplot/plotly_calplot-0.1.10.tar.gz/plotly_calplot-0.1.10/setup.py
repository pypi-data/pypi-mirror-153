# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotly_calplot']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=4.0.1,<5.0.0',
 'isort>=5.10.1,<6.0.0',
 'mypy>=0.942,<0.943',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'plotly>=5.4.0,<6.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'pytest>=7.1.1,<8.0.0',
 'vulture>=2.3,<3.0']

setup_kwargs = {
    'name': 'plotly-calplot',
    'version': '0.1.10',
    'description': 'Calendar Plot made with Plotly',
    'long_description': '# Calendar Heatmap with Plotly\nMaking it easier to visualize and costumize time relevant or time series data with plotly interaction.\n\nNew to the library? Read [this Medium article](https://medium.com/@brunorosilva/5fc322125db7).\n\nThis plot is a very similar to the contribuitions available on Github and Gitlab profile pages and to [Calplot](https://github.com/tomkwok/calplot) - which is a pyplot implementation of the calendar heatmap, thus it is not interactive right off the bat.\n\nThe first mention I could find of this plot being made with plotly was in [this forum post](https://community.plotly.com/t/colored-calendar-heatmap-in-dash/10907/16) and it got my attention as something it should be easily available to anyone.\n\n# Installation\n``` bash\npip install plotly-calplot\n```\n\n# Examples\n\nIn [this Medium article](https://medium.com/@brunorosilva/5fc322125db7) I covered lot\'s of usage methods for this library.\n``` python\nfrom plotly_calplot import calplot\n\nfig = calplot(df, x="date", y="value")\nfig.show()\n# you can also adjust layout and your usual plotly stuff\n```\n\n<img src="https://github.com/brunorosilva/plotly-calplot/blob/main/assets/images/example.png?raw=true">\n',
    'author': 'Bruno Rodrigues Silva',
    'author_email': 'b.rosilva1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brunorosilva/plotly-calplot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
