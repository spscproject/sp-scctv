# Sp's CCTV

Welcome to the Sp's CCTV ! This application allows you to use your computer's webcam to monitor your surroundings and send email alerts with images whenever motion is detected. It's perfect for home security, monitoring your lab, or keeping an eye on your pets.

## Features

- **Motion Detection**: Continuously monitors for motion using your webcam.
- **Email Alerts**: Sends an email with an image attachment whenever motion is detected.
- **Multiple Camera Support**: Select between multiple cameras connected to your system.
- **Easy Configuration**: Simple setup process with minimal user input.

## Requirements

- Python 3 or above
- OpenCV
- `smtplib` (included with Python)
- `cryptography` library for encryption
- `pickle` (included with Python)

You can install the required libraries using pip.

## Installation

### Windows

1. **Directly Install**:
   - Download Python from [python.org](https://www.python.org/downloads/) and run the installer. Make sure to check the option to add Python to your PATH.

2. **Install Required Libraries**:
   - Open your Command Prompt (you can search for "cmd" in the Start menu) and run the following commands:
   ```bash
   pip install opencv-python cryptography
   ```

3. **Clone the Repository**:
   - In the Command Prompt, run:
   ```bash
   git clone https://github.com/yourusername/PersonalCCTV.git
   cd PersonalCCTV
   ```

4. **Run the Application**:
   - Run the application using this command:
   ```bash
   python cctv_camera.py
   ```

### macOS

1. **Install Python**:
   - Download Python from [python.org](https://www.python.org/downloads/) and run the installer.

2. **Install Required Libraries**:
   - Open your Terminal (found in Applications > Utilities), and run the following commands:
   ```bash
   pip install opencv-python cryptography
   ```

3. **Clone the Repository**:
   - In the Terminal, run:
   ```bash
   git clone https://github.com/yourusername/PersonalCCTV.git
   cd PersonalCCTV
   ```

4. **Run the Application**:
   - Use this command to run the application:
   ```bash
   python cctv_camera.py
   ```

### Direct Installation (Windows & macOS)

For users who prefer a quicker method without navigating through the command line:

1. **Download the ZIP File**:
   - Go to the repository on GitHub: [PersonalCCTV](https://github.com/yourusername/PersonalCCTV).
   - Click on the green "Code" button and select "Download ZIP."

2. **Extract the ZIP File**:
   - Locate the downloaded ZIP file in your Downloads folder and extract it.

3. **Open Command Prompt (Windows) or Terminal (macOS)**:
   - **Windows**: Search for "cmd" in the Start menu.
   - **macOS**: Open Terminal from Applications > Utilities.

4. **Navigate to the Extracted Folder**:
   - Use the following command (replace `<path_to_your_folder>` with the actual path):
   ```bash
   cd <path_to_your_folder>
   ```

5. **Install Required Libraries**:
   - Run this command to install the necessary libraries:
   ```bash
   pip install opencv-python cryptography
   ```

6. **Run the Application**:
   - Execute the following command:
   ```bash
   python cctv_camera.py
   ```

## Usage

1. **Email Configuration**: Upon running the application for the first time, you will be prompted to enter your email, email password, and the receiver's email address. The application securely stores these credentials using encryption.
2. **Select Camera**: Choose which camera to use (default camera is 0, with options up to 5).
3. **Start Monitoring**: The application will start monitoring for motion. If motion is detected, it will capture an image and send it to the specified email address.
4. **Options**: You can change the email credentials or camera index while the application is running by pressing '3' and following the prompts.

## Security Considerations

- The application encrypts sensitive information (email and password) before storing it to ensure privacy.
- Make sure to use a secure email account and consider enabling two-factor authentication (2FA) for added security.

## Limitations

- The application is designed for personal use and may require adjustments for more extensive deployments.
- Performance may vary based on your system's hardware capabilities.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Feel free to modify the links, repository name, and any other specifics to match your project setup. This README provides clear, step-by-step instructions for users to install and run the application easily.
