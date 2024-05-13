import cv2
import os
import glob

video_folder = './part 2'

video_files = glob.glob(os.path.join(video_folder, '*.mp4'))

for video_path in video_files:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        continue

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    frame_output_path = f'student/{video_name}/'
    try:
        os.makedirs(frame_output_path, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create directory for frames for video {video_name}")
        continue
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps)

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval == 0:
            frame_name = f'frame_{frame_count//interval:02d}.jpg'
            cv2.imwrite(os.path.join(frame_output_path, frame_name), frame)

        frame_count += 1

    cap.release()

cv2.destroyAllWindows()
