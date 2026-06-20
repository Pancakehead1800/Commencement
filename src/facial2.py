import cv2
import numpy as np

# Load image
image = cv2.imread('./db_faces/e.png')

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define range of background color (e.g., white background)
# Adjust these values based on your specific background color
lower_white = np.array([0, 0, 200])
upper_white = np.array([150, 15, 255])

# Create a mask
mask = cv2.inRange(hsv, lower_white, upper_white)

# Invert mask to keep the subject
mask_inv = cv2.bitwise_not(mask)

# Apply mask to original image
foreground = cv2.bitwise_and(image, image, mask=mask_inv)

# Add transparency (BGRA format)
foreground_bgra = cv2.cvtColor(foreground, cv2.COLOR_BGR2BGRA)
foreground_bgra[:, :, 3] = mask_inv

# Save result
cv2.imwrite('output_no_bg.png', foreground_bgra)   