import json
import os
import pkg_resources
import platform
import smtplib
import time

import psutil
import simpleaudio as sa


class Timer:
    def __init__(
        self,
        method="json",
        config_path=None,
        email=None,
        password=None,
        server=None,
        port=None,
    ):
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
                    self.sender_email = secrets.get("scriptime_email")
                    self.sender_password = secrets.get("scriptime_password")
                    self.server = secrets.get("scriptime_server")
                    self.port = secrets.get("scriptime_port")
            except FileNotFoundError:
                print(f"{config_path} not found.")
            except json.JSONDecodeError:
                print("Error decoding JSON data.")
        elif method == "env":
            # loads passwords through env variables
            self.sender_email = os.environ.get("SCRIPTIME_EMAIL")
            self.sender_password = os.environ.get("SCRIPTIME_PASSWORD")
            self.server = os.environ.get("SCRIPTIME_SERVER")
            self.port = int(os.environ.get("SCRIPTIME_PORT"))

            if (
                self.sender_email is not None
                and self.sender_password is not None
                and self.server is not None
                and self.port is not None
            ):
                pass
            else:
                ValueError(
                    "Not all environment variables are set. Please ensure you have: SCRIPTIME_EMAIL, SCRIPTIME_PASSWORD, SCRIPTIME_SERVER, and SCRIPTIME_PORT set."
                )
        elif method == "hardcode":
            # loads passwords through email and password variables
            self.sender_email = email
            self.sender_password = password
            self.server = server
            self.port = port
        else:
            raise ValueError(
                f'{method} is not a valid method. Please use "json", "env", or "hardcode"'
            )

        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def send_email(self, target, print_body=False):
        if self.start_time is None:
            raise RuntimeError("Timer has not been started. To start, call start()")

        elapsed_time = time.time() - self.start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        ram_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()
        ram_available = psutil.virtual_memory().available / (1024**3)

        system_info = platform.system()
        processor = platform.processor()
        python_version = platform.python_version()

        self._get_pkgs()

        email_body = f"Subject: {self.descriptor}\n\n"
        email_body += f"Your script has finished.\n\n"
        email_body += f"Elapsed Time: {elapsed_time_str}\n\n"
        email_body += f"Max RAM Usage: {ram_usage:.2f}%\n"
        email_body += f"Max CPU Usage: {cpu_usage:.2f}%\n"
        email_body += f"Max RAM Available: {ram_available:.2f} GB\n\n"
        email_body += f"System information: {system_info}\n"
        email_body += f"Processor: {processor}\n"
        email_body += f"Python Version: {python_version}\n\n"
        email_body += f"Packages Used:\n{self.pkgs}"

        try:
            with smtplib.SMTP(self.server, self.port) as smtp:
                smtp.starttls()
                smtp.login(self.sender_email, self.sender_password)
                if isinstance(target, str):
                    smtp.sendmail(self.sender_email, target, email_body)
                elif isinstance(target, list):
                    for email in target:
                        smtp.sendmail(self.sender_email, email, email_body)
        except Exception as e:
            raise Exception(f"An error occurred sending an email: {e}")

        if print_body:
            print(email_body)

    def play_sound(self):
        # current_dir = os.path.dirname(__file__)
        # parent_dir = os.path.dirname(current_dir)
        # alert_wav_path = os.path.join(parent_dir, "resources/alert.wav")
        # print(alert_wav_path)
        # path_list = os.getenv("PATH").split(os.pathsep)
        # print(path_list)
        wave_obj = sa.WaveObject.from_wave_file("alert.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()

    def _get_pkgs(self):
        installed_packages = [pkg.key for pkg in pkg_resources.working_set]

        pkg_versions = [
            (pkg_name, pkg_resources.get_distribution(pkg_name).version)
            for pkg_name in installed_packages
            if pkg_resources.get_distribution(pkg_name).version
        ]

        self.pkgs = "\n".join(
            [
                f"Package: {package}, Version: {version}"
                for package, version in pkg_versions
            ]
        )
