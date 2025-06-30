import cv2 as cv
import pytesseract as py

# Tesseract path because it is not in my path.
py.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
capture = cv.VideoCapture(0, cv.CAP_DSHOW)
while True:
    ret, frame = capture.read()
    if not ret:
        break
    # Convert to grayscale bcs it simplifies the image
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to reduce noise
    blurred = cv.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding for better local contrast
    thresh = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                  cv.THRESH_BINARY_INV, 11, 3)
    # Optional: Dilation to connect broken parts of digits
    '''kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    thresh = cv.dilate(thresh, kernel, iterations=1)'''
    # OCR configuration: single word, digits only
    config = '--psm 8 -c tessedit_char_whitelist=0123456789'
    text = py.image_to_string(thresh, config=config).strip()
    # Display detected text
    cv.putText(frame, f"Detected: {text}", (10, 50),
               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # Show output windows
    cv.imshow('Number Detection', frame)
    # Exit on pressing 'q'
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

# Cleanup
capture.release()
cv.destroyAllWindows()
