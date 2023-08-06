# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['video2pdfslides_tddschn']

package_data = \
{'': ['*']}

install_requires = \
['img2pdf==0.4.1',
 'imutils==0.5.4',
 'opencv-python==4.5.2.52',
 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['v2ps = video2pdfslides_tddschn.cli:main',
                     'video2pdfslides = video2pdfslides_tddschn.cli:main']}

setup_kwargs = {
    'name': 'video2pdfslides-tddschn',
    'version': '0.2.0',
    'description': 'Converts a video presentation into a deck of pdf slides by capturing screenshots of unique frames',
    'long_description': '# video2pdfslides-tddschn\n\nBased on https://github.com/kaushikj/video2pdfslides,\n\ncredits to https://github.com/kaushikj.\n\n## Description\nThis project converts a video presentation into a deck of pdf slides by capturing screenshots of unique frames\n<br> youtube demo: https://www.youtube.com/watch?v=Q0BIPYLoSBs\n\n## Additional features\n- Add support for specifying parameters via command line options.\n- Add `--no-verify` to skip manual inspection and deduplication of extracted images and save to pdf directly.\n- Add `-c` / `--clip` to copy the output pdf path to clipboard.\n- Installable via `pipx install video2pdfslides-tddschn`. \n\n\n## Table of Contents\n- [video2pdfslides-tddschn](#video2pdfslides-tddschn)\n  - [Description](#description)\n  - [Additional features](#additional-features)\n  - [Table of Contents](#table-of-contents)\n  - [Installation](#installation)\n    - [pipx](#pipx)\n    - [pip](#pip)\n  - [Usage](#usage)\n  - [Example](#example)\n  - [More](#more)\n  - [Develop](#develop)\n  - [Developer contact info](#developer-contact-info)\n\n## Installation\n\nRequires Python 3.9.\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install video2pdfslides-tddschn --python "$(which python3.9)"\n```\n\n### [pip](https://pypi.org/project/video2pdfslides-tddschn/)\n\n```\n$ python3.9 -m pip install video2pdfslides-tddschn\n```\n\n\n## Usage\n```\nvideo2pdfslides <video_path> <options>\n\n# or, use the shorthand v2ps:\nv2ps <video_path> <options>\n```\n\nit will capture screenshots of unique frames and save it output folder...once screenshots are captured the program is paused and the user is asked to manually verify the screenshots and delete any duplicate images. Once this is done the program continues and creates a pdf out of the screenshots.\n\n```\n$ v2ps --help\n\nusage: video2pdfslides [-h] [-o OUTPUT_SLIDES_DIR] [-r FRAME_RATE] [-w WARMUP] [-f FGBG_HISTORY] [-v VAR_THRESHOLD] [-s] [-m MIN_PERCENT] [-x MAX_PERCENT]\n                       [-n] [-c] [-V]\n                       INPUT_VIDEO_PATH\n\nConverts a video presentation into a deck of pdf slides by capturing screenshots of unique frames\n\npositional arguments:\n  INPUT_VIDEO_PATH      path of video to be converted to pdf slides\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -o OUTPUT_SLIDES_DIR, --output-slides-dir OUTPUT_SLIDES_DIR\n                        path of output folder (default: output)\n  -r FRAME_RATE, --frame-rate FRAME_RATE\n                        no of frames per second that needs to be processed, fewer the count faster the speed (default: 1)\n  -w WARMUP, --warmup WARMUP\n                        initial number of frames to be skipped (default: 1)\n  -f FGBG_HISTORY, --fgbg-history FGBG_HISTORY\n                        no.of frames in background object (default: 15)\n  -v VAR_THRESHOLD, --var-threshold VAR_THRESHOLD\n                        Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the\n                        background model. This parameter does not affect the background update. (default: 16)\n  -s, --detect-shadows  If true, the algorithm will detect shadows and mark them. It decreases the speed a bit, so if you do not need this feature, set the\n                        parameter to false. (default: False)\n  -m MIN_PERCENT, --min-percent MIN_PERCENT\n                        min percentage of diff between foreground and background to detect if motion has stopped (default: 0.1)\n  -x MAX_PERCENT, --max-percent MAX_PERCENT\n                        max percentage of diff between foreground and background to detect if frame is still in motion (default: 3.0)\n  -n, --no-verify       skip manual inspection and deduplication of extracted images and save to pdf directly. (default: False)\n  -c, --clip            copy the path of the output pdf to clipboard. (default: False)\n  -V, --version         show program\'s version number and exit\n```\n\n## Example\nThere are two sample video avilable in "./input", you can test the code using these input by running\n<li>python video2pdfslides.py "./input/Test Video 1.mp4" (4 unique slide)\n<li>python video2pdfslides.py "./input/Test Video 2.mp4" (19 unique slide)\n\n\n## More\nThe default parameters works for a typical video presentation. But if the video presentation has lots of animations, the default parametrs won\'t give a good results, you may notice duplicate/missing slides. Don\'t worry, you can make it work for any video presentation, even the ones with animations, you just need to fine tune and figure out the right set of parametrs, The 3 most important parameters that I would recommend to get play around is "MIN_PERCENT", "MAX_PERCENT", "FGBG_HISTORY". The description of these variables can be found in code comments.\n\n\n## Develop\n\n```\n$ git clone https://github.com/tddschn/video2pdfslides-tddschn.git\n$ cd video2pdfslides-tddschn\n$ poetry install\n```\n\n## Developer contact info\nkaushik jeyaraman: kaushikjjj@gmail.com\n',
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
