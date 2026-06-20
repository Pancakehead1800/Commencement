import cv2
import numpy as np

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture('input_video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Crop the face region
        face_roi = frame[y:y+h, x:x+w]
        
        # Optional: Apply color segmentation to the face ROI to clean up background
        hsv_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask_face = cv2.inRange(hsv_face, lower_blue, upper_blue)
        fg_mask_face = cv2.bitwise_not(mask_face)
        cleaned_face = cv2.bitwise_and(face_roi, face_roi, mask=fg_mask_face)
        
        # Display the cleaned face
        cv2.imshow('Cleaned Face', cleaned_face)

    cv2.imshow('Original Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()   
