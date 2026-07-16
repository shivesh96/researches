import cv2
import os
import pandas as pd
from datetime import datetime
from urllib.parse import quote

# Directory to store employee images
employee_images_dir = 'employee_images'

# Function to capture employee images for training
def capture_employee_images(employee_id):
    cap = cv2.VideoCapture(0)  # Use the default camera (you can modify this if needed)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    employee_dir = os.path.join(employee_images_dir, f'employee_{employee_id}')
    os.makedirs(employee_dir, exist_ok=True)

    count = 0
    while count < 10:  # Capture 10 images for training
        print(f"Capturing image {count}")
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            cv2.imwrite(f"{employee_dir}/employee_{employee_id}_{count}.jpg", roi_gray)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1

        cv2.imshow('Capture Employee Images', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 10:
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to perform face detection on frames
def detect_faces(frame):
    # Use a pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return frame

# Check the connected camera devices and select the appropriate one
def select_camera():
    num_cameras = 2  # Adjust this value based on the number of cameras connected
    for i in range(num_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            return i
        cap.release()
    return None

# Placeholder for employee_detected logic
def employee_detected_logic(frame):
    # Implement your logic here to determine if an employee is detected
    # Example: Return True if face detected, otherwise False
    return False  # Modify this according to your actual detection logic

# Load or create an Excel file to store tracking records
excel_file = 'employee_tracking_records.xlsx'
if not os.path.exists(excel_file):
    # Create a new DataFrame if the Excel file doesn't exist
    df = pd.DataFrame(columns=['Employee_ID', 'Timestamp', 'Camera_Channel'])
else:
    # Load existing records into a DataFrame
    df = pd.read_excel(excel_file)

# Placeholder employee ID for testing purposes
tracked_employee_id = 1

# RTSP URL for the camera stream (with username and password)
rtsp_username = 'admin'
rtsp_password = 'Hacker_Home#96_'
rtsp_host = '192.168.1.254:254'
rtsp_port = '554'
camera_no = 2  # or any other camera channel if specified differently
rtsp_url = f'rtsp://{quote(rtsp_username)}:{quote(rtsp_password)}@{rtsp_host}:{rtsp_port}/cam/realmonitor?channel={camera_no}&subtype=0'


# Open a connection to the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the connection is successful
if not cap.isOpened():
    print("Error: Could not open the RTSP stream.")
    # Open the default camera (usually the laptop's built-in camera)

    # Select the desired camera
    camera_index = select_camera()
    if camera_index is None:
        print("Error: No camera found.")
        exit()

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        exit()

while True:
    ret, frame = cap.read()

    if ret:
        frame_with_faces = detect_faces(frame)
        cv2.imshow('Employee Tracking', frame_with_faces)

        if employee_detected_logic(frame_with_faces):
            # Log the tracking event if an employee is detected
            timestamp = datetime.now()
            camera_channel = 'Channel X'  # Replace with actual camera channel info
            tracking_event = {'Employee_ID': tracked_employee_id,
                              'Timestamp': timestamp,
                              'Camera_Channel': camera_channel}
            df = df.append(tracking_event, ignore_index=True)
            df.to_excel(excel_file, index=False)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
