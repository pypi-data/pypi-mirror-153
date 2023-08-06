import argparse
from pathlib import Path

from . import __app_name__, __version__, __description__
from .video2pdfslides import (
    initialize_output_folder,
    detect_unique_screenshots,
    convert_screenshots_to_pdf,
)


def get_args() -> argparse.Namespace:
    # parser = argparse.ArgumentParser("video_path")
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description=__description__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "video_path",
        help="path of video to be converted to pdf slides",
        type=Path,
        metavar='INPUT_VIDEO_PATH',
    )
    OUTPUT_SLIDES_DIR = Path('.') / 'output'

    FRAME_RATE = 1  # no.of frames per second that needs to be processed, fewer the count faster the speed
    WARMUP = FRAME_RATE  # initial number of frames to be skipped
    FGBG_HISTORY = FRAME_RATE * 15  # no.of frames in background object
    VAR_THRESHOLD = 16  # Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model.
    DETECT_SHADOWS = False  # If true, the algorithm will detect shadows and mark them.
    MIN_PERCENT = 0.1  # min percentage of diff between foreground and background to detect if motion has stopped
    MAX_PERCENT = 3.0  # max percentage of diff between foreground and background to detect if frame is still in motion
    parser.add_argument(
        '-o',
        "--output-slides-dir",
        help="path of output folder",
        type=Path,
        default=OUTPUT_SLIDES_DIR,
    )
    parser.add_argument(
        '-r',
        "--frame-rate",
        help="no of frames per second that needs to be processed, fewer the count faster the speed",
        type=int,
        default=FRAME_RATE,
    )
    parser.add_argument(
        '-w',
        "--warmup",
        help="initial number of frames to be skipped",
        type=int,
        default=WARMUP,
    )
    parser.add_argument(
        '-f',
        "--fgbg-history",
        help="no.of frames in background object",
        type=int,
        default=FGBG_HISTORY,
    )
    parser.add_argument(
        '-v',
        "--var-threshold",
        help="Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model. This parameter does not affect the background update.",
        type=int,
        default=VAR_THRESHOLD,
    )
    parser.add_argument(
        '-s',
        "--detect-shadows",
        help="If true, the algorithm will detect shadows and mark them. It decreases the speed a bit, so if you do not need this feature, set the parameter to false.",
        action="store_true",
        default=DETECT_SHADOWS,
        # type=bool,
        # default=DETECT_SHADOWS,
    )
    parser.add_argument(
        '-m',
        "--min-percent",
        help="min percentage of diff between foreground and background to detect if motion has stopped",
        type=float,
        default=MIN_PERCENT,
    )
    parser.add_argument(
        '-x',
        "--max-percent",
        help="max percentage of diff between foreground and background to detect if frame is still in motion",
        type=float,
        default=MAX_PERCENT,
    )

    parser.add_argument(
        '-n',
        '--no-verify',
        action='store_true',
        help='skip manual inspection and deduplication of extracted images and save to pdf directly.',
    )

    parser.add_argument(
        '-c',
        '--clip',
        action='store_true',
        help='copy the path of the output pdf to clipboard.',
    )

    parser.add_argument(
        '-V', '--version', action='version', version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()
    return args


def main():
    args = get_args()
    video_path = args.video_path
    args.output_slides_dir.mkdir(parents=True, exist_ok=True)

    print('video_path', video_path)
    output_folder_screenshot_path = initialize_output_folder(
        video_path, args.output_slides_dir
    )
    detect_unique_screenshots(
        video_path,
        output_folder_screenshot_path,
        args.frame_rate,
        args.warmup,
        args.fgbg_history,
        args.var_threshold,
        args.detect_shadows,
        args.min_percent,
        args.max_percent,
    )

    def convert_to_pdf():
        convert_screenshots_to_pdf(
            output_folder_screenshot_path, args.output_slides_dir, video_path
        )

    if args.no_verify:
        pdf_path = convert_to_pdf()
    else:
        print('Please Manually verify screenshots and delete duplicates')
        while True:
            choice = input("Press y to continue and n to terminate: ")
            choice = choice.lower().strip()
            if choice in ['y', 'n']:
                break
            else:
                print('please enter a valid choice')

        if choice == 'y':
            pdf_path = convert_to_pdf()
        else:
            return

    if args.clip:
        import pyperclip

        pyperclip.copy(str(pdf_path))
        print(f'Copied PDF path {pdf_path} to clipboard.')


if __name__ == "__main__":
    main()
