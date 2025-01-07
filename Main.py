import threading
import time
import json
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar
from PIL import Image, ImageTk
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

service = Service("C:/Users/lenovo/Desktop/view_bot/chromedriver/chromedriver-win64/chromedriver.exe")

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Define global variables
MAX_CONCURRENT_VIDEOS = config["MAX_CONCURRENT_VIDEOS"]
CHROMEDRIVER_PATH = config["CHROMEDRIVER_PATH"]
task_queue = Queue()  # Queue to manage video tasks

# Function to launch Chrome in incognito mode
def launch_browser(video_url):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-unsafe-swiftshader")  # Add this line
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(video_url)
    print(f"Playing video: {video_url}")
    return driver

# Worker function for handling each video playback task
def process_video(video_url, duration):
    try:
        browser = launch_browser(video_url)
        time.sleep(duration * 60)  # Simulate video playback for the specified duration
        browser.quit()
        print(f"Finished playing video: {video_url}. Resetting...")
    except Exception as e:
        print(f"Error processing video {video_url}: {e}")

# Queue worker thread
def video_worker():
    while True:
        video_url, duration = task_queue.get()
        try:
            process_video(video_url, duration)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            task_queue.task_done()

# Start worker threads
for _ in range(MAX_CONCURRENT_VIDEOS):
    thread = threading.Thread(target=video_worker, daemon=True)
    thread.start()

# UI Setup
root = Tk()
root.title("YouTube Viewer - 610 Marketing")
root.geometry("600x600")

# Load and display the logo
def load_logo():
    try:
        logo_image = Image.open("assets/610_marketing_logo.png")
        logo_image = logo_image.resize((150, 150), Image.ANTIALIAS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = Label(root, image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        logo_label.pack(pady=10)
    except Exception as e:
        Label(root, text="Logo not found or failed to load.", fg="red").pack()

# Start button functionality
def start_viewer():
    video_links_list = video_links.get().split(",")
    duration = view_duration.get()
    max_views_per_day = max_views.get()

    print("Starting program...")
    for video_url in video_links_list:
        for _ in range(max_views_per_day):
            task_queue.put((video_url.strip(), duration))

# Input fields for YouTube viewer
Label(root, text="Enter Video Link(s) (comma-separated):", font=("Arial", 12)).pack(pady=5)
video_links = StringVar()
video_links_entry = Entry(root, textvariable=video_links, width=50)
video_links_entry.pack(pady=5)

Label(root, text="View Duration (minutes):", font=("Arial", 12)).pack(pady=5)
view_duration = IntVar(value=10)
view_duration_entry = Entry(root, textvariable=view_duration, width=10)
view_duration_entry.pack(pady=5)

Label(root, text="Maximum Views Per Day (per video):", font=("Arial", 12)).pack(pady=5)
max_views = IntVar(value=120)
max_views_entry = Entry(root, textvariable=max_views, width=10)
max_views_entry.pack(pady=5)

# Start button
start_button = Button(root, text="Start Viewer", command=start_viewer, bg="green", fg="white")
start_button.pack(pady=20)

# Load the logo
load_logo()

# Run the UI loop
root.mainloop()
