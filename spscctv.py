import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import os
import pickle
import threading
import sys

def save_credentials(sender_email, password, receiver_email):
    """Save email credentials in a binary file."""
    credentials = {
        'sender_email': sender_email,
        'password': password,
        'receiver_email': receiver_email
    }
    with open('credentials.bin', 'wb') as f:
        pickle.dump(credentials, f)

def load_credentials():
    """Load email credentials from a binary file."""
    if os.path.exists('credentials.bin'):
        with open('credentials.bin', 'rb') as f:
            return pickle.load(f)
    return None

def send_email(file_path, sender_email, password, receiver_email):
    """Send an email with the attached image."""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Motion Detected"

    with open(file_path, 'rb') as f:
        attachment = MIMEImage(f.read())
    msg.attach(attachment)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def detect_motion(camera_index, sender_email, password, receiver_email):
    """Detect motion using the specified webcam."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Camera at index {camera_index} could not be opened.")
        return

    last_frame = None

    if not os.path.exists('captured_images'):
        os.makedirs('captured_images')

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if last_frame is not None:
            delta_frame = cv2.absdiff(last_frame, gray)
            _, thresh = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) < 1000:
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                image_path = f"captured_images/motion_{timestamp}.jpg"
                cv2.imwrite(image_path, frame)
                send_email(image_path, sender_email, password, receiver_email)

        last_frame = gray
        cv2.imshow('Motion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def count_connected_cameras():
    """Count the number of connected cameras."""
    count = 0
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        count += 1
        cap.release()
        index += 1
    return count

def print_about():
    """Print information about the application."""
    print("""
    Welcome to Sp's CCTV Application!
    
    This application allows you to monitor motion detected by your webcam.
    When motion is detected, an image will be captured and sent to your email.

    Instructions:
    1. Make sure your webcam is connected and functioning.
    2. Enter your email credentials when prompted.
    3. Select the camera you want to use.
    4. To exit the application, press 'q' in the motion detection window.
    """)

def main():
    """Main function to manage email settings and start motion detection."""
    #print("Welcome to Sp's CCTV\n")
    print_about()
    credentials = load_credentials()
    if not credentials:
        sender_email = input("Enter your email: ")
        password = input("Enter your email password: ")
        receiver_email = input("Enter the receiver's email: ")
        save_credentials(sender_email, password, receiver_email)
    else:
        sender_email = credentials['sender_email']
        password = credentials['password']
        receiver_email = credentials['receiver_email']

    camera_count = count_connected_cameras()
    print(f"Number of connected cameras: {camera_count}")

    if camera_count > 0:
        camera_index = int(input("Select camera (0 to {0}): ".format(camera_count - 1) + " (default is 0): ") or 0)
        camera_index = max(0, min(camera_index, camera_count - 1))  # Ensure valid index
    else:
        print("No cameras detected. Exiting.")
        sys.exit(1)

    detection_thread = threading.Thread(target=detect_motion, args=(camera_index, sender_email, password, receiver_email))
    detection_thread.start()

    # Show options after starting the detection thread
    while True:
        print("\nOptions: ")
        print("Press 'q' to exit.")
        print("Press 'a' for about this application.")
        
        key = input("Choose an option: ")
        
        if key.lower() == 'a':
            print_about()
        elif key.lower() == 'q':
            break

    detection_thread.join()  # Wait for the detection thread to finish

if __name__ == "__main__":
    main()
