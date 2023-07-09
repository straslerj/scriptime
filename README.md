# scriptime
Python library to notify when a script has finished running and providing insights such as run time, CPU and RAM usage, and more.


- [scriptime](#scriptime)
  - [About](#about)
  - [Getting Started](#getting-started)
  - [Using scriptimer](#using-scriptimer)
  - [Output](#output)
  - [Links](#links)

## About

This project will send you an email or text message notifying you when a script has completed running. Configurable thorugh a config file, environment variables, or hardcoding the email credentials, this project has little overhead to get started.

## Getting Started

The first step to using scriptime is setting up the email that will be sending the notifications. scriptime uses the built-in Python SMTP to send emails which requires an email address, said email's password, and an SMTP SSL server and port. Therfore,

1. Choose how you will pass your email credential into scriptime:
   1. **JSON config file**
   
        To set up, create a .json file with the following contents:
        ```
        {
            "scriptime_email": "example@email.com",
            "scriptime_password": "superSecure1",
            "scriptime_server": "smtp.email.com"
            "scriptime_port": 123>
        }
        ```
    2. **Environment variables**

        *Recommended -- if you plan to use scriptime more than once this will be the simplest method over time.*

        Set the following environment variales:

        `SCRIPTIME_EMAIL=example@email.com`

        `SCRIPTIME_PASSWORD=superSecure1`

        `SCRIPTIME_SERVER=smtp.email.com`

        `SCRIPTIME_PORT=123`

    3. **Hard coding**

        If you choose to go the hard code route, when creating the `Timer` object, you will need to pass in extra arguments. Your constructor call should look something like:

        ```python
        timer = Timer(method="hardcode", email="example@email.com", password="superSecure1", server="smtp.email.com", port=123)
        ```

        > Note that if you are using Gmail, you may have to create an [app password](https://support.google.com/accounts/answer/185833?hl=en). Your normal password will likely not work. Other email services may have similar catches.


## Using scriptimer

The use of scriptimer is very straightforward:

1. In a terminal, `pip install scriptime`
2. In a Python (.py) or Jupyter Notebook (.ipynb) file, add
    ```python
    from scriptime import Timer
    ``` 
    to your imports.
4. Create an instance of a timer, which could be done in three ways dependant on what you did in [Getting Started](#getting-started):
   1. **JSON config file**
        ```python
        timer = Timer(method="json", config_file="path/to/config.json")
        ```

   2. **Environment variables**
        ```python
        timer = Timer(method="env")
        ```
   3. **Hard coding**

        (This may look famiiliar):

        ```python
        timer = Timer(method="hardcode", email="example@email.com", password="superSecure1", server="smtp.email.com", port=123)
        ```
5. Start the timer
   ```python
   timer.start()
   ```

6. Then, at the end of the script (or wherever you would like a notification), add one of or both of the following:
   1. **Email notification**

        To get an email notification, simply call the send_email function:
        ```python
        timer.send_email("receiver@email.com")
        ```

        You can also send a text using your carrier's email-to-SMS address. You can find your carrier at: [list of carrier SMS emails](https://avtech.com/articles/138/list-of-email-to-sms-addresses/)
        ```python
        timer.send_email("0123456789@text.att.net")
        ```

        Multiple email addresses, phone numbers, or any combination thereof can be passed in as a list:
        ```python
        timer.send_email(["receiver@email.com", "0123456789@text.att.net"])
        ```

        Lastly, if you would like to see the output of the body in order to have the statistics persistent or just because you're curious, simply use the `print_body` flag:
        ```python
        timer.send_email("receiver@email.com", print_body=True)
        ```
   2. **Play sound**

        If you would like an audible notification that your script has finished, simply:
        ```python
        timer.play_sound()
        ```
        > If the time measurement aspect of this program is important to you, be sure to run the play sound after sending the email (if you are sending the email at the end of the script) as it takes ~5 seconds to play the sound.

## Output

The subject of the email will be:

```
[MM-DD-YYYY HH:MM:SS] <name of file> Finished
```

The email/text body will look like the following:

```
Your script has finished.

Elapsed Time: 00:00:01

Max RAM Usage: 74.00%
Max CPU Usage: 40.90%
Remaining RAM Available: 2.08 GB

System information: Darwin
Processor: arm
Python Version: 3.11.4

Packages Used:
Package: numpy, Version: 1.24.2
Package: scikit-learn, Version: 1.2.2
...
```

## Links

 - Source code: https://github.com/straslerj/scriptime
 - PyPI: https://pypi.org/project/scriptime/
