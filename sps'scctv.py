import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import os
import pickle
from cryptography.fernet import Fernet
import threading

def generate_key():
    """Generate a new Fernet key."""
    return Fernet.generate_key()

def save_credentials(sender_email, password, receiver_email, key):
    """Save email credentials in a binary file."""
    cipher = Fernet(key)
    credentials = {
        'sender_email': sender_email,
        'password': password,
        'receiver_email': receiver_email
    }
    encrypted_data = cipher.encrypt(pickle.dumps(credentials))
    with open('credentials.bin', 'wb') as f:
        f.write(encrypted_data)

def load_credentials(key):
    """Load email credentials from a binary file."""
    if os.path.exists('credentials.bin'):
        cipher = Fernet(key)
        with open('credentials.bin', 'rb') as f:
            encrypted_data = f.read()
        credentials = pickle.loads(cipher.decrypt(encrypted_data))
        return credentials
    else:
        return None

def send_email(image_path, sender_email, password, receiver_email):
    """Send an email with the attached image."""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Motion Detected"

    with open(image_path, 'rb') as f:
        img = MIMEImage(f.read())
    msg.attach(img)

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
    last_frame = None

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

                # Save the image when motion is detected
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                image_path = f"motion_{timestamp}.jpg"
                cv2.imwrite(image_path, frame)
                send_email(image_path, sender_email, password, receiver_email)

        last_frame = gray
        cv2.imshow('Motion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    """Main function to manage email settings and start motion detection."""
    print("Welcome to Sp's CCTV\n")
    
    # Generate a new key
    key = generate_key()

    # Load credentials or prompt for input
    credentials = load_credentials(key)
    if not credentials:
        sender_email = input("Enter your email: ")
        password = input("Enter your email password: ")
        receiver_email = input("Enter the receiver's email: ")
        save_credentials(sender_email, password, receiver_email, key)
    else:
        sender_email = credentials['sender_email']
        password = credentials['password']
        receiver_email = credentials['receiver_email']

    # Camera selection
    print("Select camera (0 for default, 1-5 for other cameras):")
    camera_index = input("Enter your choice (default is 0): ")
    camera_index = int(camera_index) if camera_index.isdigit() and 0 <= int(camera_index) <= 5 else 0

    # Start motion detection in a separate thread
    detection_thread = threading.Thread(target=detect_motion, args=(camera_index, sender_email, password, receiver_email))
    detection_thread.start()

    while True:
        print("\nOptions:")
        print("Press any key to exit.")
        print("Press '3' for more options.")
        
        key = input("Choose an option: ")
        
        if key == '3':
            # Change email and password
            sender_email = input("Enter new sender email: ")
            password = input("Enter new sender password: ")
            receiver_email = input("Enter new receiver email: ")
            save_credentials(sender_email, password, receiver_email, key)
            print("Credentials updated.")
            
            # Change camera
            camera_index = input("Enter new camera index (0-5): ")
            camera_index = int(camera_index) if camera_index.isdigit() and 0 <= int(camera_index) <= 5 else 0
            print("Camera updated.")
        else:
            # Exit
            break

    detection_thread.join()  # Wait for the detection thread to finish

if __name__ == "__main__":
    main()
