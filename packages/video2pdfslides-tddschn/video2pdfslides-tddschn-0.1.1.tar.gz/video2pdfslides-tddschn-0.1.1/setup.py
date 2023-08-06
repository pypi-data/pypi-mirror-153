# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['video2pdfslides_tddschn']

package_data = \
{'': ['*']}

install_requires = \
['img2pdf==0.4.1', 'imutils==0.5.4', 'opencv-python==4.5.2.52']

entry_points = \
{'console_scripts': ['v2ps = video2pdfslides_tddschn.video2pdfslides:main',
                     'video2pdfslides = '
                     'video2pdfslides_tddschn.video2pdfslides:main']}

setup_kwargs = {
    'name': 'video2pdfslides-tddschn',
    'version': '0.1.1',
    'description': 'Converts a video presentation into a deck of pdf slides by capturing screenshots of unique frames',
    'long_description': '# video2pdfslides-tddschn\n\nPyPI Upload of https://github.com/kaushikj/video2pdfslides,\n\nwith more command line options.\n\nAll credits to https://github.com/kaushikj.\n\n# Description\nThis project converts a video presentation into a deck of pdf slides by capturing screenshots of unique frames\n<br> youtube demo: https://www.youtube.com/watch?v=Q0BIPYLoSBs\n\n\n\n# Usage\nvideo2pdfslides <video_path> <options>\n\nit will capture screenshots of unique frames and save it output folder...once screenshots are captured the program is paused and the user is asked to manually verify the screenshots and delete any duplicate images. Once this is done the program continues and creates a pdf out of the screenshots.\n\n```\n\n# Example\nThere are two sample video avilable in "./input", you can test the code using these input by running\n<li>python video2pdfslides.py "./input/Test Video 1.mp4" (4 unique slide)\n<li>python video2pdfslides.py "./input/Test Video 2.mp4" (19 unique slide)\n\n\n# More\nThe default parameters works for a typical video presentation. But if the video presentation has lots of animations, the default parametrs won\'t give a good results, you may notice duplicate/missing slides. Don\'t worry, you can make it work for any video presentation, even the ones with animations, you just need to fine tune and figure out the right set of parametrs, The 3 most important parameters that I would recommend to get play around is "MIN_PERCENT", "MAX_PERCENT", "FGBG_HISTORY". The description of these variables can be found in code comments.\n\n\n## Develop\n\n```\n$ git clone https://github.com/tddschn/video2pdfslides-tddschn.git\n$ cd video2pdfslides-tddschn\n$ poetry install\n```\n\n# Developer contact info\nkaushik jeyaraman: kaushikjjj@gmail.com\n',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/video2pdfslides-tddschn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
