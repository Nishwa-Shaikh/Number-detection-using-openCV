import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)  #Try thresh_binary.

    config = r'--oem 3 --psm 6'  # ignore whitelist for testing (TRY PSM 8 LATER)
    text = pytesseract.image_to_string(thresh, config=config).strip()
    digits_only = re.sub(r'\D', '', text)  # Keep digits only

    if digits_only:

        cv2.putText(frame, f"Detected: {digits_only}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3)
        
    cv2.imshow("Number Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

'''import cv2
import pytesseract
import re

# Set path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Initialize webcam
cap = cv2.VideoCapture(0)

# --- Set desired resolution ---
requested_width = 1280
requested_height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, requested_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, requested_height)

# --- Check actual resolution set ---
actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Requested: {requested_width}x{requested_height}")
print(f"Actual:    {actual_width}x{actual_height}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Apply thresholding (white background, black digits)
    _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

    # Tesseract config (digits only)
    config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(thresh, config=config).strip()

    # Extract digits only
    digits_only = re.sub(r'\D', '', text)

    # If any digits detected, show on screen
    if digits_only:
        cv2.putText(frame, f"Detected: {digits_only}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    # Display frames
    cv2.imshow("Number Detector", frame)
    cv2.imshow("Thresholded", thresh)

    # Quit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release and clean up
cap.release()
cv2.destroyAllWindows()'''
