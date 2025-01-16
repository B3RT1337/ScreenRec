import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
import pyautogui
import cv2
import numpy as np
import threading
import time
from datetime import datetime


class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HD Screen Recorder")
        self.root.geometry("400x355")
        self.root.iconbitmap('utils/rec_ico.ico')
        self.root.resizable(False, False)

        # Initialize settings
        self.recording = False
        self.filename = self.generate_filename()
        self.screen_size = pyautogui.size()
        self.fps = 30
        self.recording_start_time = None

        # Display loading animation
        self.intro_frame = tk.Frame(self.root)
        self.intro_frame.pack(fill="both", expand=True)

        self.intro_label = tk.Label(self.intro_frame, text="HD Screen Recorder", font=("Arial", 14))
        self.intro_label.place(relx=0.5, rely=0.7, anchor="center")

        self.made_by_label = tk.Label(self.root, text="Made by B3RT1337", font=("Arial", 8), fg="gray")
        self.made_by_label.pack(side="bottom", pady=0.01)
    
        self.loading_image = PhotoImage(file="utils/rec.png")
        self.image_label = tk.Label(self.intro_frame, image=self.loading_image)
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # Simulate loading for 2 seconds
        self.root.after(2000, self.show_main_ui)

    def show_main_ui(self):
        self.intro_frame.pack_forget()
        self.create_main_ui()

    def create_main_ui(self):
        self.label = tk.Label(self.root, text="HD Screen Recorder", font=("Arial", 16))
        self.label.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording, bg="green", fg="white", width=20)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, bg="red", fg="white", width=20)
        self.stop_button.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save As...", command=self.save_as, bg="blue", fg="white", width=20)
        self.save_button.pack(pady=5)

        self.settings_button = tk.Button(self.root, text="Settings", command=self.open_settings, bg="gray", fg="white", width=20)
        self.settings_button.pack(pady=5)

        self.about_button = tk.Button(self.root, text="About This App", command=self.about_app, bg="purple", fg="white", width=20)
        self.about_button.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Status: Ready", font=("Arial", 10))
        self.status_label.pack(pady=10)

    def start_recording(self):
        if self.recording:
            messagebox.showwarning("Warning", "Already recording!")
            return
        self.recording = True
        self.recording_start_time = time.time()
        self.status_label.config(text="Recording...(00:00:00)")
        threading.Thread(target=self.update_timer).start()
        threading.Thread(target=self.record_screen).start()

    def stop_recording(self):
        if not self.recording:
            messagebox.showwarning("Warning", "Not recording!")
            return
        self.recording = False
        self.status_label.config(text="Status: Ready")
        messagebox.showinfo("Info", "Recording stopped and saved.")

    def save_as(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".avi",
                                                     filetypes=[("AVI files", "*.avi"), ("All files", "*.*")])
        if not self.filename:
            self.filename = self.generate_filename()

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x250")
        resolution_var = tk.StringVar(value="1080p")
        fps_var = tk.StringVar(value=str(self.fps))

        tk.Label(settings_window, text="Select Resolution:").pack(pady=5)
        resolutions = [("720p (1280x720)", "720p"), ("1080p (1920x1080)", "1080p")]
        for text, value in resolutions:
            tk.Radiobutton(settings_window, text=text, variable=resolution_var, value=value).pack(anchor="w")

        tk.Label(settings_window, text="Select Frame Rate:").pack(pady=5)
        fps_options = ["30", "60"]
        for fps in fps_options:
            tk.Radiobutton(settings_window, text=f"{fps} FPS", variable=fps_var, value=fps).pack(anchor="w")

        def apply_settings():
            resolution = resolution_var.get()
            self.screen_size = (1280, 720) if resolution == "720p" else (1920, 1080)
            self.fps = int(fps_var.get())
            settings_window.destroy()
            messagebox.showinfo("Settings Applied", f"Resolution: {resolution}, FPS: {self.fps}")

        tk.Button(settings_window, text="Apply", command=apply_settings, bg="green", fg="white").pack(pady=10)

    def about_app(self):
        about_text = (
            "HD Screen Recorder\n\n"
            "Version: 1.0\n"
            "This is a simple screen recording app that allows you to record your screen "
            "in HD quality. Customize resolution and frame rate as needed."
            "\n\nMade by B3RT1337"
            "\nGithub: https://github.com/B3RT1337"
        )
        messagebox.showinfo("About This App", about_text)

    def update_timer(self):
        while self.recording:
            elapsed = int(time.time() - self.recording_start_time)
            hours, minutes, seconds = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
            self.status_label.config(text=f"Recording...({hours:02}:{minutes:02}:{seconds:02})")
            time.sleep(1)

    def record_screen(self):
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.filename, fourcc, self.fps, self.screen_size)
        while self.recording:
            img = pyautogui.screenshot(region=(0, 0, self.screen_size[0], self.screen_size[1]))
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            out.write(frame)
            time.sleep(1 / self.fps)
        out.release()

    def generate_filename(self):
        return f"Recording_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.avi"


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()
