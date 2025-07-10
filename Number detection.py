import cv2
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow('Digit Detection')
cv2.createTrackbar('Brightness', 'Digit Detection', 50, 100, nothing)
cv2.createTrackbar('Contrast', 'Digit Detection', 50, 100, nothing)

last_detected = ""
last_time = 0
hold_duration = 10  # seconds to hold last detection before clearing

while True:
    ret, frame = cap.read()
    if not ret:
        break

    brightness = cv2.getTrackbarPos('Brightness', 'Digit Detection') - 50
    contrast = cv2.getTrackbarPos('Contrast', 'Digit Detection') / 50
    adjusted = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)
    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    data = pytesseract.image_to_data(thresh, config=custom_config, output_type=pytesseract.Output.DICT)

    digits = ''
    conf_threshold = 50

    for i, txt in enumerate(data['text']):
        if txt.strip().isdigit():
            try:
                conf = int(data['conf'][i])
            except ValueError:
                conf = -1
            if conf > conf_threshold:
                digits += txt

    current_time = time.time()
    if digits:
        last_detected = digits
        last_time = current_time
    else:
        # Clear after hold_duration seconds without detection
        if current_time - last_time > hold_duration:
            last_detected = ""

    display_text = f'Detected digits: {last_detected}' if last_detected else "No digits detected"

    cv2.putText(adjusted, display_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow('Digit Detection', adjusted)
    cv2.imshow('Thresh', thresh)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
