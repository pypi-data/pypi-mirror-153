import os
import time
import cv2
import imutils
import shutil
import img2pdf
import glob
import argparse
from . import __app_name__, __version__, __description__


def get_frames(video_path, FRAME_RATE, WARMUP):
    '''A fucntion to return the frames from a video located at video_path
    this function skips frames as defined in FRAME_RATE'''

    # open a pointer to the video file initialize the width and height of the frame
    vs = cv2.VideoCapture(video_path)
    if not vs.isOpened():
        raise Exception(f'unable to open file {video_path}')

    total_frames = vs.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_time = 0
    frame_count = 0
    print("total_frames: ", total_frames)
    print("FRAME_RATE", FRAME_RATE)

    # loop over the frames of the video
    while True:
        # grab a frame from the video

        vs.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)  # move frame to a timestamp
        frame_time += 1 / FRAME_RATE

        (_, frame) = vs.read()
        # if the frame is None, then we have reached the end of the video file
        if frame is None:
            break

        frame_count += 1
        yield frame_count, frame_time, frame

    vs.release()


def detect_unique_screenshots(
    video_path,
    output_folder_screenshot_path,
    FRAME_RATE,
    WARMUP,
    FGBG_HISTORY,
    VAR_THRESHOLD,
    DETECT_SHADOWS,
    MIN_PERCENT,
    MAX_PERCENT,
):
    # Initialize fgbg a Background object with Parameters
    # history = The number of frames history that effects the background subtractor
    # varThreshold = Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model. This parameter does not affect the background update.
    # detectShadows = If true, the algorithm will detect shadows and mark them. It decreases the speed a bit, so if you do not need this feature, set the parameter to false.

    fgbg = cv2.createBackgroundSubtractorMOG2(
        history=FGBG_HISTORY, varThreshold=VAR_THRESHOLD, detectShadows=DETECT_SHADOWS
    )

    captured = False
    start_time = time.time()
    (W, H) = (None, None)

    screenshoots_count = 0
    for frame_count, frame_time, frame in get_frames(video_path, FRAME_RATE, WARMUP):
        orig = frame.copy()  # clone the original frame (so we can save it later),
        frame = imutils.resize(frame, width=600)  # resize the frame
        mask = fgbg.apply(frame)  # apply the background subtractor

        # apply a series of erosions and dilations to eliminate noise
        #            eroded_mask = cv2.erode(mask, None, iterations=2)
        #            mask = cv2.dilate(mask, None, iterations=2)

        # if the width and height are empty, grab the spatial dimensions
        if W is None or H is None:
            (H, W) = mask.shape[:2]

        # compute the percentage of the mask that is "foreground"
        p_diff = (cv2.countNonZero(mask) / float(W * H)) * 100

        # if p_diff less than N% then motion has stopped, thus capture the frame

        if p_diff < MIN_PERCENT and not captured and frame_count > WARMUP:
            captured = True
            filename = f"{screenshoots_count:03}_{round(frame_time/60, 2)}.png"

            path = os.path.join(output_folder_screenshot_path, filename)
            print("saving {}".format(path))
            cv2.imwrite(path, orig)
            screenshoots_count += 1

        # otherwise, either the scene is changing or we're still in warmup
        # mode so let's wait until the scene has settled or we're finished
        # building the background model
        elif captured and p_diff >= MAX_PERCENT:
            captured = False
    print(f'{screenshoots_count} screenshots Captured!')
    print(f'Time taken {time.time()-start_time}s')
    return


def initialize_output_folder(video_path, OUTPUT_SLIDES_DIR):
    '''Clean the output folder if already exists'''
    output_folder_screenshot_path = (
        f"{OUTPUT_SLIDES_DIR}/{video_path.rsplit('/')[-1].split('.')[0]}"
    )

    if os.path.exists(output_folder_screenshot_path):
        shutil.rmtree(output_folder_screenshot_path)

    os.makedirs(output_folder_screenshot_path, exist_ok=True)
    print('initialized output folder', output_folder_screenshot_path)
    return output_folder_screenshot_path


def convert_screenshots_to_pdf(
    output_folder_screenshot_path, OUTPUT_SLIDES_DIR, video_path
):
    output_pdf_path = (
        f"{OUTPUT_SLIDES_DIR}/{video_path.rsplit('/')[-1].split('.')[0]}" + '.pdf'
    )
    print('output_folder_screenshot_path', output_folder_screenshot_path)
    print('output_pdf_path', output_pdf_path)
    print('converting images to pdf..')
    with open(output_pdf_path, "wb") as f:
        f.write(
            img2pdf.convert(sorted(glob.glob(f"{output_folder_screenshot_path}/*.png")))
        )
    print('Pdf Created!')
    print('pdf saved at', output_pdf_path)


def get_args():
    # parser = argparse.ArgumentParser("video_path")
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description=__description__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "video_path", help="path of video to be converted to pdf slides", type=str
    )
    OUTPUT_SLIDES_DIR = f"./output"

    FRAME_RATE = 1  # no.of frames per second that needs to be processed, fewer the count faster the speed
    WARMUP = FRAME_RATE  # initial number of frames to be skipped
    FGBG_HISTORY = FRAME_RATE * 15  # no.of frames in background object
    VAR_THRESHOLD = 16  # Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model.
    DETECT_SHADOWS = False  # If true, the algorithm will detect shadows and mark them.
    MIN_PERCENT = 0.1  # min percentage of diff between foreground and background to detect if motion has stopped
    MAX_PERCENT = 3.0  # max percentage of diff between foreground and background to detect if frame is still in motion
    parser.add_argument(
        "--output_slides_dir",
        help="path of output folder",
        type=str,
        default=OUTPUT_SLIDES_DIR,
    )
    parser.add_argument(
        "--frame_rate",
        help="no of frames per second that needs to be processed, fewer the count faster the speed",
        type=int,
        default=FRAME_RATE,
    )
    parser.add_argument(
        "--warmup",
        help="initial number of frames to be skipped",
        type=int,
        default=WARMUP,
    )
    parser.add_argument(
        "--fgbg_history",
        help="no.of frames in background object",
        type=int,
        default=FGBG_HISTORY,
    )
    parser.add_argument(
        "--var_threshold",
        help="Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model. This parameter does not affect the background update.",
        type=int,
        default=VAR_THRESHOLD,
    )
    parser.add_argument(
        "--detect_shadows",
        help="If true, the algorithm will detect shadows and mark them. It decreases the speed a bit, so if you do not need this feature, set the parameter to false.",
        action="store_true",
        # type=bool,
        # default=DETECT_SHADOWS,
    )
    parser.add_argument(
        "--min_percent",
        help="min percentage of diff between foreground and background to detect if motion has stopped",
        type=float,
        default=MIN_PERCENT,
    )
    parser.add_argument(
        "--max_percent",
        help="max percentage of diff between foreground and background to detect if frame is still in motion",
        type=float,
        default=MAX_PERCENT,
    )

    parser.add_argument(
        '-V', '--version', action='version', version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()
    return args


def main():
    args = get_args()
    video_path = args.video_path

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

    print('Please Manually verify screenshots and delete duplicates')
    while True:
        choice = input("Press y to continue and n to terminate")
        choice = choice.lower().strip()
        if choice in ['y', 'n']:
            break
        else:
            print('please enter a valid choice')

    if choice == 'y':
        convert_screenshots_to_pdf(
            output_folder_screenshot_path, args.output_slides_dir, video_path
        )


if __name__ == "__main__":
    main()
