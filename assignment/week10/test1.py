import cv2
import numpy as np

CROP_ROW = 120
IMG_WIDTH = 640
IMG_HEIGHT = 480

LOWER_YELLOW = np.array([25, 50, 100])
UPPER_YELLOW = np.array([35, 255, 255])

WHITE_THRESHOLD = 200

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)

img_center_x = IMG_WIDTH // 2

print("라인 트레이서 작동 시작... 종료하려면 'q' 키를 누르게.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("오류: 카메라 프레임을 읽을 수 없네.")
        break

    crop_img = frame[CROP_ROW:, :]

    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
    _, white_mask = cv2.threshold(blur, WHITE_THRESHOLD, 255, cv2.THRESH_BINARY)

    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)

    M = cv2.moments(combined_mask)
    
    cX = img_center_x 

    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
    
    error = img_center_x - cX

    steering_command = ""
    if abs(error) <= 30: 
        steering_command = "STRAIGHT"
    elif error > 0: 
        steering_command = "STEER LEFT"
    else: 
        steering_command = "STEER RIGHT"

    cv2.imshow('Line Mask (Yellow+White)', combined_mask)
    
    cv2.circle(crop_img, (cX, 100), 10, (0, 0, 255), -1) 
    cv2.line(crop_img, (img_center_x, 0), (img_center_x, crop_img.shape[0]), (0, 255, 0), 2)
    cv2.putText(crop_img, steering_command, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow('Line Tracer View', crop_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()