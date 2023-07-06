import json
import os
import smtplib
import time

import psutil
import simpleaudio as sa


class Timer:
    def __init__(self, method="json", config_path=None, email=None, password=None):
        current_time = time.localtime()
        formatted_time = time.strftime("%m-%d-%Y %H:%M:%S", current_time)

        file_name = os.path.basename(__file__)

        self.descriptor = f"[{formatted_time}] {file_name} Finished"
        self.sender_email = None
        self.sender_password = None

        if method == "json":
            # load passwords through json
            try:
                with open(config_path) as f:
                    secrets = json.load(f)
                    self.sender_email = secrets.get("sender_email")
                    self.sender_password = secrets.get("sender_password")
                    self.server = secrets.get("server")
                    self.port = secrets.get("port")
            except FileNotFoundError:
                print(f"{config_path} not found.")
            except json.JSONDecodeError:
                print("Error decoding JSON data.")
        elif method == "env":
            # loads passwords through env variables
            self.sender_email = os.environ.get("SENDER_EMAIL")
            self.sender_password = os.environ.get("SENDER_PASSWORD")
        elif method == "hardcode":
            # loads passwords through email and password variables
            self.sender_email = email
            self.sender_password = password
        else:
            raise ValueError(
                f'{method} is not a valid method. Please use "json", "env", or "hardcode"'
            )

        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def send_email(self, target):
        if self.start_time is None:
            raise RuntimeError("Timer has not been started.")

        elapsed_time = time.time() - self.start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        ram_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()

        email_body = f"Subject: {self.descriptor}\n\n"
        email_body += f"Your script has finished.\n\nStatistics:\n"
        email_body += f"Elapsed Time: {elapsed_time_str}\n"
        email_body += f"Max RAM Usage: {ram_usage:.2f}%\n"
        email_body += f"Max CPU Usage: {cpu_usage:.2f}%"

        with smtplib.SMTP(self.server, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.sender_email, self.sender_password)
            if isinstance(target, str):
                smtp.sendmail(self.sender_email, target, email_body)
            elif isinstance(target, list):
                for email in target:
                    smtp.sendmail(self.sender_email, email, email_body)

    def play_sound(self):
        wave_obj = sa.WaveObject.from_wave_file("alert.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()
