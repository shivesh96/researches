import cv2
import os
import pandas as pd
import tkinter as tk
import numpy as np
import face_recognition
from datetime import datetime
from urllib.parse import quote

# Directory to store employee images
employee_images_dir = 'employee_images'
face_encodings_file = 'face_encodings.npy'
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

# Function to capture more employee images for improved recognition
def capture_employee():
    cap = cv2.VideoCapture(select_camera())  # Use the default camera

    def save_employee_data():
        employee_id = entry_id.get()
        employee_name = entry_name.get()

        employee_dir = os.path.join(employee_images_dir, f'employee_{employee_id}')
        os.makedirs(employee_dir, exist_ok=True)

        count = 0
        employee_images = []
        while count < 100:  # Capture more images for improved recognition
            print(f"Capturing image {count}")
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                employee_images.append(roi_gray)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1

            cv2.imshow('Capture Employee Images', frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or count >= 100:
                break

        # Calculate face encodings for all captured images
        face_encodings = [face_recognition.face_encodings(img)[0] for img in employee_images]

        # Save the face encodings into a single file
        np.save(os.path.join(employee_dir, face_encodings_file), np.array(face_encodings))

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

# Function to recognize face using saved employee data
def recognize_face(frame):
    # Load saved employee face encodings
    employees = {}
    for root, dirs, files in os.walk(employee_images_dir):
        for file in files:
            if file.endswith(face_encodings_file):
                employee_encodings = np.load(os.path.join(root, file))
                employees[os.path.basename(root)] = employee_encodings

    # Perform face recognition on the input frame
    unknown_encoding = face_recognition.face_encodings(frame)[0]

    for employee_id, employee_encodings in employees.items():
        # Compare face encodings
        match = face_recognition.compare_faces(employee_encodings, unknown_encoding)
        if True in match:
            return employee_id  # Return employee ID if recognized

    return None  # Return None if no match found


# Function to perform face detection on frames
def start_tracking():
    cap = cv2.VideoCapture(select_camera())  # Use the default camera

    # Load existing records into a DataFrame
    df = pd.DataFrame(columns=['Employee_ID', 'Timestamp', 'Camera_Channel'])
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)

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
