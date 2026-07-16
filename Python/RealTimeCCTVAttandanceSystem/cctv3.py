import cv2
import threading
from urllib.parse import quote

# Replace these placeholders with your actual credentials and RTSP URL format
username = 'admin'
password = 'testPass'
ip_address = '192.168.1.254'
connection = '554'  # or any other connection port if specified differently
total_camera = 3  # or any other camera channel if specified differently

def capture_camera_feed(camera_no, rtsp_url):
    print(f'Connecting to {rtsp_url}...')
    cap = cv2.VideoCapture(rtsp_url)
    cv2.namedWindow(f"CCTV Live Feed {camera_no}", cv2.WINDOW_NORMAL)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to grab frame from camera {camera_no}")
            break

        cv2.imshow(f"CCTV Live Feed {camera_no}", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
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