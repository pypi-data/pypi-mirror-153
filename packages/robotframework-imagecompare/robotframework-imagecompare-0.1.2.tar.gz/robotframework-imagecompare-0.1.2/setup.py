# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ImageCompare']

package_data = \
{'': ['*']}

install_requires = \
['imutils>=0.5.4,<0.6.0',
 'numpy>=1.22.3,<2.0.0',
 'opencv-python-headless>=4.5.5,<5.0.0',
 'robotframework>=4',
 'scikit-image>=0.19.2,<0.20.0']

setup_kwargs = {
    'name': 'robotframework-imagecompare',
    'version': '0.1.2',
    'description': 'A Robot Framework Library for image comparisons',
    'long_description': '\n# ImageCompare Library for Robot Framework®\n\nA library for simple screenshot comparison.\nSupports image files like .png and .jpg.\n\nImage Parts can be ignored via simple coordinate masks or area masks.\n\nSee [Keyword Documentation](https://manykarim.github.io/robotframework-imagecompare/imagecompare.html) for more information.\n\n## Install robotframework-imagecompare\n\n### Installation via `pip`\n\n* `pip install --upgrade robotframework-imagecompare`\n\n## Examples\n\nCheck the `/atest/Compare.robot` test suite for some examples.\n\n### Testing with [Robot Framework](https://robotframework.org)\n```RobotFramework\n*** Settings ***\nLibrary    ImageCompare\n\n*** Test Cases ***\nCompare two Images and highlight differences\n    Compare Images    Reference.jpg    Candidate.jpg\n```\n\n### Use masks/placeholders to exclude parts from visual comparison\n\n```RobotFramework\n*** Settings ***\nLibrary    ImageCompare\n\n*** Test Cases ***\nCompare two Images and ignore parts by using masks\n    Compare Images    Reference.jpg    Candidate.jpg    placeholder_file=masks.json\n\nCompare two PDF Docments and ignore parts by using masks\n    Compare Images    Reference.jpg    Candidate.jpg    placeholder_file=masks.json\n```\n#### Different Mask Types to Ignore Parts When Comparing\n##### Areas, Coordinates\n```python\n[\n    {\n    "page": "1",\n    "name": "Top Border",\n    "type": "area",\n    "location": "top",\n    "percent":  5\n    },\n    {\n    "page": "1",\n    "name": "Left Border",\n    "type": "area",\n    "location": "left",\n    "percent":  5\n    },\n    {\n    "page": 1,\n    "name": "Top Rectangle",\n    "type": "coordinates",\n    "x": 0,\n    "y": 0,\n    "height": 10,\n    "width": 210,\n    "unit": "mm"\n    }\n]\n```\n## More info will be added soon\n',
    'author': 'Many Kasiriha',
    'author_email': 'many.kasiriha@dbschenker.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manykarim/robotframework-imagecompare',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
