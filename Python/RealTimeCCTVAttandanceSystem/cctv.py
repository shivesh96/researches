import cv2
from urllib.parse import quote

# Replace these placeholders with your actual credentials and RTSP URL format
username = 'admin'
password = 'Hacker_Home#96_'
# ip_address = '192.168.1.254'
ip_address = 'cybolitehome.cpplusddns.com'
connection = '554' # or any other connection port if specified differently
total_camera = 3  # or any other camera channel if specified differently

# run all cameras
for camera_no in range(total_camera):
    # Create RTSP URL
    rtsp_url = f'rtsp://{quote(username)}:{quote(password)}@{ip_address}:{connection}/cam/realmonitor?channel={camera_no+1}&subtype=0'
    print(f'Connecting to {rtsp_url}...')

    # Create OpenCV VideoCapture object with RTSP stream cap_{camera_no}
    exec(f'cap_{camera_no} = cv2.VideoCapture(rtsp_url)')
    
    # create imshow window
    exec(f'cv2.namedWindow(f"CCTV Live Feed {camera_no}", cv2.WINDOW_NORMAL)')
    
    # run all cameras
    while True:
        # Capture frame-by-frame
        exec(f'ret_{camera_no}, frame_{camera_no} = cap_{camera_no}.read()')

        # Display the closable frame
        exec(f'cv2.imshow(f"CCTV Live Feed {camera_no}", frame_{camera_no})')

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture and close the window
for camera_no in range(total_camera):
    print(f"Destroying Camera {camera_no}")
    exec(f'cap_{camera_no}.release()')
    exec(f'cv2.destroyAllWindows()')

# rtsp_url = f'rtsp://{quote(username)}:{quote(password)}@{ip_address}:{connection}/cam/realmonitor?channel={camera_no}&subtype=0'
# print(f'Connecting to {rtsp_url}...')
# # Create OpenCV VideoCapture object with RTSP stream
# cap = cv2.VideoCapture(rtsp_url)
# while True:
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Display the frame
#     cv2.imshow('CCTV Live Feed', frame)

#     # Exit if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the capture and close the window
# cap.release()
# cv2.destroyAllWindows()
