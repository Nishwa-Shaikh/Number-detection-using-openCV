import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    h, w, _ = frame.shape
    #image width and height.
    x1, y1 = w // 2 - 150, h // 2 - 150
    x2, y2 = x1 + 300, y1 + 300
    roi = frame[y1:y2, x1:x2]
    # Show the image in a rectangle
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    # Convert image to grayscale for better visualization
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # OCR for digits only
    config = r'--oem 3 --psm 10 -c tessedit_char_whitelist=0123456789'
    # Run OCR on image
    text = pytesseract.image_to_string(gray, config=config).strip()
    # Show detected text on screen
    if text.isdigit():
        cv2.putText(frame, f"Detected: {text}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.imshow("Number Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()