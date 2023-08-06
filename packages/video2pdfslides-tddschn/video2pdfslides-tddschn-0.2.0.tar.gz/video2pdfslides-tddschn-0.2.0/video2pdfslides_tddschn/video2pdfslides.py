#!/usr/bin/env python3

from pathlib import Path


def get_frames(video_path: Path, FRAME_RATE: int):
    '''A fucntion to return the frames from a video located at video_path
    this function skips frames as defined in FRAME_RATE'''
    import cv2

    # open a pointer to the video file initialize the width and height of the frame
    vs = cv2.VideoCapture(str(video_path))
    if not vs.isOpened():
        raise Exception(f'unable to open file {str(video_path)}')

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
    video_path: Path,
    output_folder_screenshot_path: Path,
    FRAME_RATE: int,
    WARMUP: int,
    FGBG_HISTORY: int,
    VAR_THRESHOLD: int,
    DETECT_SHADOWS: bool,
    MIN_PERCENT: float,
    MAX_PERCENT: float,
) -> None:
    """
    Initialize fgbg a Background object with Parameters
    history = The number of frames history that effects the background subtractor
    varThreshold = Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model. This parameter does not affect the background update.
    detectShadows = If true, the algorithm will detect shadows and mark them. It decreases the speed a bit, so if you do not need this feature, set the parameter to false.
    """

    import time
    import cv2
    import imutils

    fgbg = cv2.createBackgroundSubtractorMOG2(
        history=FGBG_HISTORY, varThreshold=VAR_THRESHOLD, detectShadows=DETECT_SHADOWS
    )

    captured = False
    start_time = time.time()
    (W, H) = (None, None)

    screenshoots_count = 0
    for frame_count, frame_time, frame in get_frames(video_path, FRAME_RATE):
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

            path = str(output_folder_screenshot_path / filename)
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


def initialize_output_folder(video_path: Path, OUTPUT_SLIDES_DIR: Path) -> Path:
    '''Clean the output folder if already exists'''
    import os
    import shutil

    output_folder_screenshot_path = (
        # f"{OUTPUT_SLIDES_DIR}/{video_path.rsplit('/')[-1].split('.')[0]}"
        OUTPUT_SLIDES_DIR
        / video_path.stem
    )

    if os.path.exists(output_folder_screenshot_path):
        shutil.rmtree(output_folder_screenshot_path)

    # os.makedirs(output_folder_screenshot_path, exist_ok=True)
    output_folder_screenshot_path.mkdir(exist_ok=True)
    print('initialized output folder', str(output_folder_screenshot_path))
    return output_folder_screenshot_path


def convert_screenshots_to_pdf(
    output_folder_screenshot_path: Path, OUTPUT_SLIDES_DIR: Path, video_path: Path
) -> Path:
    import img2pdf

    output_pdf_path = (
        # f"{OUTPUT_SLIDES_DIR}/{video_path.rsplit('/')[-1].split('.')[0]}" + '.pdf'
        (OUTPUT_SLIDES_DIR / video_path.stem).with_suffix('.pdf')
    )
    print('output_folder_screenshot_path', str(output_folder_screenshot_path))
    print('output_pdf_path', str(output_pdf_path))
    print('converting images to pdf..')
    with open(output_pdf_path, "wb") as f:
        f.write(
            # img2pdf.convert(sorted(glob.glob(f"{output_folder_screenshot_path}/*.png")))
            img2pdf.convert(
                sorted(map(str, output_folder_screenshot_path.glob('*.png')))
            )
        )
    print('Pdf Created!')
    print('pdf saved at', str(output_pdf_path))
    return output_pdf_path.resolve()
