# Ticket Booking Automation Script

This project is an automation script for booking tickets on the `kham.com.tw` website. It uses the Playwright library for browser automation and `ddddocr` for CAPTCHA recognition.

## Table of Contents

- [Ticket Booking Automation Script](#ticket-booking-automation-script)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)

## Features

- Automates the process of ticket booking.
- Uses OCR to automatically solve CAPTCHA challenges.
- Multithreading support for faster processing of certain tasks.
- Detailed logging to track the process and errors.

## Requirements

- Python 3.7+
- Playwright
- ddddocr
- WebDriver Manager for Python
- Google Chrome or Chromium browser

## Installation

1. **Clone the repository:**

   ```bash
   $ git clone https://github.com/yourusername/ticket-booking-automation.git
   $ cd ticket-booking-automation
   ```

2. **Install the required Python packages:**

You can install the required packages using pip:
```bash
$ pip install -r requirements.txt

If playwright is not installed, you may need to install it manually:
$ pip3 install playwright
$ playwright install
```

Update the username and password in the main() function.
Adjust any other parameters, such as the target URL or the thread count if needed.

3. Copy .env.example as .env, and input url, username, password
```
$ copy .env.example .env
```

4. Run the script:
```
$ python3 kham_spider_ticket_pw.py
```