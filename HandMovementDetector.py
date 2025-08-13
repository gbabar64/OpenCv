import cv2
import pyautogui as py
import HandTrackingModule as htm
import time
cap = cv2.VideoCapture(0)
detector = htm.HandDetector(detection_con=0.4,max_hands=1)

screen_width,screen_heigth=py.size()


width_ratio=screen_width/cap.get(3)
heigth_ratio=screen_heigth/cap.get(4)
print(cap.get(3),cap.get(4),screen_width,screen_heigth)
stime=0
ftime=0
while True:
    stime=time.time()
    _, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.find_hands(img)
    lmList, _ = detector.find_position(img, draw=False)
    if len(lmList)!=0:
        py.moveTo(width_ratio*lmList[8][1],heigth_ratio*lmList[8][2])
    cv2.imshow("Frame", img)
    ftime = time.time()
    print(ftime - stime)
    ftime = stime
    if cv2.waitKey(1)==ord('q'):
       break
cap.release()
cv2.destroyAllWindows()