import inspect
import json
import os
import platform
import smtplib
import sys
import time
from typing import Optional, Union

import pkg_resources
import psutil
import simpleaudio as sa


class Timer:
    """The Timer class contains all functionality for the scriptime project

    This class contains the logic to send an email (send_email) and play a sound (play_sound) when your script has completed running,
    as well as some helper methods to do so.

    Attributes
    ----------
    - `method`: string, default="json"
            - Dictates how the program should get email credentials. Options include:
                - `json`: (default value) read a JSON file containing email credentials.
                - `env`: parse email credentials from environment variables.
                - `hardcode`: manually pass your credentials in as arguments
        - `config_path`: string (optional)
            - If `method` is set to `"json"`, then a path to the JSON file must be passed in as a string.
        - `email`: string (optional)
            - Sender email address. If `method` is set to `"hardcode"`, then the sender email address must be passed in as a string.
        - `password`: string (optional)
            - Sender email password. If `method` is set to `"hardcode"`, then the sender email passsword must be passed in as a string.
        - `server`: string (optional)
            - SMTP SSL server for sender email. If `method` is set to `"hardcode"`, then the sender email SMTP SSL server must be passed in as a string. Find your email server at: https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html
        - `port`: int (optional)
            - SMTP SSL port for sender email. If `method` is set to `"hardcode"`, then the sender email SMTP SSL email port must be passed in as a string. Find your email port at: https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html
    """

    def __init__(
        self,
        method: str = "json",
        config_path: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        server: Optional[str] = None,
        port: Optional[int] = None,
    ) -> None:
        """Initialize Timer with method, config_path, email, password, server, and port.

        Parameters
        ----------
        - `method`: string, default="json"
            - Dictates how the program should get email credentials. Options include:
                - `json`: (default value) read a JSON file containing email credentials.
                - `env`: parse email credentials from environment variables.
                - `hardcode`: manually pass your credentials in as arguments
        - `config_path`: string (optional)
            - If `method` is set to `"json"`, then a path to the JSON file must be passed in as a string.
        - `email`: string (optional)
            - Sender email address. If `method` is set to `"hardcode"`, then the sender email address must be passed in as a string.
        - `password`: string (optional)
            - Sender email password. If `method` is set to `"hardcode"`, then the sender email passsword must be passed in as a string.
        - `server`: string (optional)
            - SMTP SSL server for sender email. If `method` is set to `"hardcode"`, then the sender email SMTP SSL server must be passed in as a string. Find your email server at: https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html
        - `port`: int (optional)
            - SMTP SSL port for sender email. If `method` is set to `"hardcode"`, then the sender email SMTP SSL email port must be passed in as a string. Find your email port at: https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html
        """
        current_time = time.localtime()
        formatted_time = time.strftime("%m-%d-%Y %H:%M:%S", current_time)

        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        file_name = os.path.basename(caller_module.__file__)

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
        """Starts the timer in order for the script runtime to be calcualted."""
        self.start_time = time.time()

    def send_email(self, target: Union[str, list], print_body: bool = False) -> None:
        """Sends the email to the targeted address(es).

        The email body will be formulated and sent to the specified target address(es). \
            Typical use would be doing this at the end of the script, although there is no one forcing you to do that.

        Arguments
        ---------
        - `target`: string or array
            - The address(es) to which the notification will be sent. This can be a string containing one email or a list containing a string of multiple emails.
        - `print_body`: bool, default=False
            - Set `True` if you would like the body of the notification printed out.
        """
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
        email_body += f"Remaining RAM Available: {ram_available:.2f} GB\n\n"
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
        """Plays a notification sound when called."""
        package_name = "scriptime"
        resource_path = "alert.wav"
        resource_package = None

        if getattr(sys, "frozen", False):
            resource_package = sys._MEIPASS
        else:
            resource_package = package_name

        alert_wav_path = pkg_resources.resource_filename(
            resource_package, resource_path
        )
        wave_obj = sa.WaveObject.from_wave_file(alert_wav_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    def _get_pkgs(self):
        """Gets the installed packages for the current venv.

        This is a helper method for building the body of the email.
        """
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
