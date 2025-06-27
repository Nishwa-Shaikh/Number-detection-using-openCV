import cv2 as cv
import pytesseract as py
cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret == False:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
    text = py.image_to_string(thresh, config = '--psm 6 digits')
    cv.putText(frame, f"Detected: {text.strip()}", (10, 50). cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv.imshow('Number detection')
    if cv.waitKey(1)&0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()