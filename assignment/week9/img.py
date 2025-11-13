import cv2
import numpy as np

LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([30, 255, 255])
WHITE_THRESHOLD = 200

kernel = np.ones((5, 5), np.uint8)

image_files = [
    "imgs/1.jpg",
    "imgs/2.jpg",
    "imgs/3.jpg",
    "imgs/4.jpg"
]

for filename in image_files:
    img = cv2.imread(filename)
    if img is None:
        continue

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    yellow_mask = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)
    
    _, white_mask = cv2.threshold(gray, WHITE_THRESHOLD, 255, cv2.THRESH_BINARY)
    
    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)

    mask_cleaned = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    mask_cleaned = cv2.dilate(mask_cleaned, kernel, iterations=1)

    result = np.full_like(img, (0, 0, 255)) 
    result[mask_cleaned != 0] = img[mask_cleaned != 0]

    cv2.imshow(f"Original: {filename}", img)
    cv2.imshow(f"Detected Lines (Red BG): {filename}", result)

    cv2.waitKey(0)

cv2.destroyAllWindows()