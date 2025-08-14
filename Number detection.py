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
hold_duration = 10  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Brightness & contrast adjustment
    brightness = cv2.getTrackbarPos('Brightness', 'Digit Detection') - 50
    contrast = cv2.getTrackbarPos('Contrast', 'Digit Detection') / 50
    adjusted = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

    gray = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours (possible tags)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tag_found = False
    digits_found = False
    detected_digits = ""

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)

        # Simple heuristic: tags are roughly rectangular and not too small
        if 1.0 < aspect_ratio < 3.0 and 50 < w < 300 and 20 < h < 150:
            tag_found = True
            tag_roi = gray[y:y+h, x:x+w]

            # OCR on the possible tag
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
            data = pytesseract.image_to_data(tag_roi, config=custom_config, output_type=pytesseract.Output.DICT)

            for i, txt in enumerate(data['text']):
                if txt.strip().isdigit():
                    try:
                        conf = int(data['conf'][i])
                    except ValueError:
                        conf = -1
                    if conf > 50:
                        detected_digits += txt

            if detected_digits:
                digits_found = True

            # Draw rectangle for visual feedback
            cv2.rectangle(adjusted, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Decide message
    current_time = time.time()
    if tag_found:
        if digits_found:
            last_detected = detected_digits
            last_time = current_time
            display_text = f"Detected digits: {last_detected}"
        else:
            display_text = "Number tag detected but empty"
    else:
        display_text = "No number tag detected"

    # Keep last detected for hold_duration
    if current_time - last_time <= hold_duration and last_detected and digits_found:
        display_text = f"Detected digits: {last_detected}"

    # Show text
    cv2.putText(adjusted, display_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow('Digit Detection', adjusted)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
