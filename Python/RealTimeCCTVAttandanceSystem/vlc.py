import vlc
from urllib.parse import quote

# Replace these placeholders with your actual credentials and RTSP URL format
username = 'admin'
password = 'Hacker_Home#96_'
ip_address = '192.168.1.254'
connection = '554'  # or any other connection port if specified differently
total_camera = 3  # or any other camera channel if specified differently

rtsp_url = f'rtsp://{quote(username)}:{quote(password)}@{ip_address}:{connection}/cam/realmonitor?channel={camera_no}&subtype=0'
print(f'Connecting to {rtsp_url}...')

p = vlc.MediaPlayer(rtsp_url)

p.play()