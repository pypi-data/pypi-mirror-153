# video2pdfslides-tddschn

Based on https://github.com/kaushikj/video2pdfslides,

credits to https://github.com/kaushikj.

## Description
This project converts a video presentation into a deck of pdf slides by capturing screenshots of unique frames
<br> youtube demo: https://www.youtube.com/watch?v=Q0BIPYLoSBs

## Additional features
- Add support for specifying parameters via command line options.
- Add `--no-verify` to skip manual inspection and deduplication of extracted images and save to pdf directly.
- Add `-c` / `--clip` to copy the output pdf path to clipboard.
- Installable via `pipx install video2pdfslides-tddschn`. 


## Table of Contents
- [video2pdfslides-tddschn](#video2pdfslides-tddschn)
  - [Description](#description)
  - [Additional features](#additional-features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Usage](#usage)
  - [Example](#example)
  - [More](#more)
  - [Develop](#develop)
  - [Developer contact info](#developer-contact-info)

## Installation

Requires Python 3.9.

### pipx

This is the recommended installation method.

```
$ pipx install video2pdfslides-tddschn --python "$(which python3.9)"
```

### [pip](https://pypi.org/project/video2pdfslides-tddschn/)

```
$ python3.9 -m pip install video2pdfslides-tddschn
```


## Usage
```
video2pdfslides <video_path> <options>

# or, use the shorthand v2ps:
v2ps <video_path> <options>
```

it will capture screenshots of unique frames and save it output folder...once screenshots are captured the program is paused and the user is asked to manually verify the screenshots and delete any duplicate images. Once this is done the program continues and creates a pdf out of the screenshots.

```
$ v2ps --help

usage: video2pdfslides [-h] [-o OUTPUT_SLIDES_DIR] [-r FRAME_RATE] [-w WARMUP] [-f FGBG_HISTORY] [-v VAR_THRESHOLD] [-s] [-m MIN_PERCENT] [-x MAX_PERCENT]
                       [-n] [-c] [-V]
                       INPUT_VIDEO_PATH

Converts a video presentation into a deck of pdf slides by capturing screenshots of unique frames

positional arguments:
  INPUT_VIDEO_PATH      path of video to be converted to pdf slides

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_SLIDES_DIR, --output-slides-dir OUTPUT_SLIDES_DIR
                        path of output folder (default: output)
  -r FRAME_RATE, --frame-rate FRAME_RATE
                        no of frames per second that needs to be processed, fewer the count faster the speed (default: 1)
  -w WARMUP, --warmup WARMUP
                        initial number of frames to be skipped (default: 1)
  -f FGBG_HISTORY, --fgbg-history FGBG_HISTORY
                        no.of frames in background object (default: 15)
  -v VAR_THRESHOLD, --var-threshold VAR_THRESHOLD
                        Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the
                        background model. This parameter does not affect the background update. (default: 16)
  -s, --detect-shadows  If true, the algorithm will detect shadows and mark them. It decreases the speed a bit, so if you do not need this feature, set the
                        parameter to false. (default: False)
  -m MIN_PERCENT, --min-percent MIN_PERCENT
                        min percentage of diff between foreground and background to detect if motion has stopped (default: 0.1)
  -x MAX_PERCENT, --max-percent MAX_PERCENT
                        max percentage of diff between foreground and background to detect if frame is still in motion (default: 3.0)
  -n, --no-verify       skip manual inspection and deduplication of extracted images and save to pdf directly. (default: False)
  -c, --clip            copy the path of the output pdf to clipboard. (default: False)
  -V, --version         show program's version number and exit
```

## Example
There are two sample video avilable in "./input", you can test the code using these input by running
<li>python video2pdfslides.py "./input/Test Video 1.mp4" (4 unique slide)
<li>python video2pdfslides.py "./input/Test Video 2.mp4" (19 unique slide)


## More
The default parameters works for a typical video presentation. But if the video presentation has lots of animations, the default parametrs won't give a good results, you may notice duplicate/missing slides. Don't worry, you can make it work for any video presentation, even the ones with animations, you just need to fine tune and figure out the right set of parametrs, The 3 most important parameters that I would recommend to get play around is "MIN_PERCENT", "MAX_PERCENT", "FGBG_HISTORY". The description of these variables can be found in code comments.


## Develop

```
$ git clone https://github.com/tddschn/video2pdfslides-tddschn.git
$ cd video2pdfslides-tddschn
$ poetry install
```

## Developer contact info
kaushik jeyaraman: kaushikjjj@gmail.com
