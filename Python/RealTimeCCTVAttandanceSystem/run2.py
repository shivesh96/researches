import cv2
import os
import pandas as pd
import tkinter as tk
from datetime import datetime
from urllib.parse import quote

# Directory to store employee images
employee_images_dir = 'employee_images'
excel_file = 'employee_tracking_records.xlsx'

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# RTSP URL for the camera stream (with username and password)
rtsp_username = 'admin'
rtsp_password = 'Hacker_Home#96_'
rtsp_host = '192.168.1.254'
rtsp_port = '554'
camera_no = 2  # or any other camera channel if specified differently
rtsp_url = f'rtsp://{quote(rtsp_username)}:{quote(rtsp_password)}@{rtsp_host}:{rtsp_port}/cam/realmonitor?channel={camera_no}&subtype=0'

# Check the connected camera devices and select the appropriate one
def select_camera():
    cap = cv2.VideoCapture(rtsp_url)
    if cap.isOpened():
        print(f"RTSP Stream Found")
        return rtsp_url
    cap.release()
    
    num_cameras = 2  # Adjust this value based on the number of cameras connected
    for i in range(num_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera found at index {i}")
            return i
        cap.release()
    return None

# Function to capture employee images for training
def capture_employee():
    cap = cv2.VideoCapture(select_camera())  # Use the default camera

    def save_employee_data():
        employee_id = entry_id.get()
        employee_name = entry_name.get()

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

    root = tk.Tk()
    root.title("Capture Employee")
    label_id = tk.Label(root, text="Enter Employee ID:")
    label_id.pack()
    entry_id = tk.Entry(root)
    entry_id.pack()
    label_name = tk.Label(root, text="Enter Employee Name:")
    label_name.pack()
    entry_name = tk.Entry(root)
    entry_name.pack()
    button_save = tk.Button(root, text="Save Employee Data", command=save_employee_data)
    button_save.pack()

    root.mainloop()

# Function to perform face detection on frames
def start_tracking():
    cap = cv2.VideoCapture(select_camera())  # Use the default camera

    # Load existing records into a DataFrame
    df = pd.DataFrame(columns=['Employee_ID', 'Timestamp', 'Camera_Channel'])
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)

    # Placeholder for face recognition logic
    def recognize_face(frame):
        # Implement face recognition logic here
        # Return employee ID if recognized, otherwise None
        return None  # Modify this according to your face recognition method

    while True:
        ret, frame = cap.read()

        if ret:
            # Placeholder for face recognition logic
            employee_id = recognize_face(frame)
            if employee_id:
                timestamp = datetime.now()
                camera_channel = 'Channel X'  # Replace with actual camera channel info
                tracking_event = {'Employee_ID': employee_id,
                                  'Timestamp': timestamp,
                                  'Camera_Channel': camera_channel}
                df = df.append(tracking_event, ignore_index=True)
                df.to_excel(excel_file, index=False)

            cv2.imshow('Employee Tracking', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

# Create GUI with buttons for Capture Employee and Start Tracking
root = tk.Tk()
root.title("Employee Tracking System")

button_capture = tk.Button(root, text="Capture Employee", command=capture_employee)
button_capture.pack()

button_track = tk.Button(root, text="Start Tracking", command=start_tracking)
button_track.pack()

root.mainloop()
