import cv2
# pip install ffmpeg-python
import ffmpeg
import threading
from urllib.parse import quote

# Replace these placeholders with your actual credentials and RTSP URL format
username = 'admin'
password = 'Hacker_Home#96_'
ip_address = '192.168.1.254'
connection = '554'
total_camera = 3

def capture_camera_feed(camera_no, rtsp_url):
    print(f'Connecting to {rtsp_url}...')
    process = (
        ffmpeg
        .input(rtsp_url)
        .output('pipe:', format='rawvideo', pix_fmt='bgr24')
        .run_async(pipe_stdout=True)
    )
    cv2.namedWindow(f"CCTV Live Feed {camera_no}", cv2.WINDOW_NORMAL)

    while True:
        in_bytes = process.stdout.read(1280 * 720 * 3)  # Adjust resolution as needed
        if not in_bytes:
            break
        frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([720, 1280, 3])
        )
        cv2.imshow(f"CCTV Live Feed {camera_no}", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    process.wait()
    cv2.destroyAllWindows()
    print(f"Camera {camera_no} closed")

# Run all cameras
threads = []
for camera_no in range(total_camera):
    rtsp_url = f'rtsp://{quote(username)}:{quote(password)}@{ip_address}:{connection}/cam/realmonitor?channel={camera_no+1}&subtype=0'
    thread = threading.Thread(target=capture_camera_feed, args=(camera_no, rtsp_url))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()