import cv2
import time
import os
import HandTrackingModule as htm
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

###Tool-Neoneffect/original,circle,polygons,etc.,+sign on index fing,img drawing on another another frame.

folderpath = 'header1'
mylist = os.listdir(folderpath)
lis = []
for imPath in mylist:
    image = cv2.imread(f'{folderpath}/{imPath}')
    lis.append(image)
print(mylist)

#######################
brushThickness = 2
eraserThickness = 100
#######################


cap = cv2.VideoCapture(0)

detector = htm.HandDetector(detection_con=0.65, max_hands=1)

imgCanvas = np.zeros((480, 640, 3), np.uint8)

header=lis[0]
def create_gradient_color_map(colors):
    cmap = LinearSegmentedColormap.from_list('custom_gradient', colors, N=100)
    return cmap


def get_color_from_gradient(percentage, gradient_cmap):
    return gradient_cmap(percentage / 100.0)


def get_rgb_values(color):
    return [int(x * 255) for x in color[:3]]


def draw_neon_line(img, start_pt, end_pt, color, thickness, num_blur_iterations=5):
    for _ in range(num_blur_iterations):
        blurred_img = cv2.GaussianBlur(img.copy(), (thickness, thickness), 0)
        img = cv2.addWeighted(img, 1.5, blurred_img, -0.5, 0)

    return cv2.line(img, start_pt, end_pt, color, thickness)


def main():
    colors = [(0, 1, 1), (1, 1, 0), (1, 0, 1)]  # RGB values for the second color

    gradient_cmap = create_gradient_color_map(colors)
    (rotang, rotation_angle, p_time, c_time, percentage, xp, yp,x1,y1) = (0, 0, 0, 0, 0, 0, 0,0,0)
    drawColor = (255, 255, 0)
    while True:
        # c_time = time.time() #for calculating fps
        # 1. Import image
        success, img = cap.read()
        # img[0:102, 0:640] = header
        img = cv2.flip(img, 1)

        # imgCanvas = np.zeros_like(img)
        # 2. Find Hand Landmarks
        img = detector.find_hands(img)
        lmList, _ = detector.find_position(img, draw=False)

        '''for i in range(5):
            blurred_img = cv2.GaussianBlur(img.copy(), (15,15), 0)
            img = cv2.addWeighted(img, 1, blurred_img, 1,1)'''

        if lmList:
            rotation_angle = detector.find_rotation()
        rotang = rotation_angle
        per = ((rotang + 90) / 360) * 100
        percentage = int(per)

        selected_color = get_color_from_gradient(percentage, gradient_cmap)
        rgb_values = get_rgb_values(selected_color)

        if len(lmList) != 0:

            # print(lmList)

            # tip of index and middle fingers
            x3, y3 = lmList[0][1], lmList[0][2]
            x2, y2 = lmList[12][1], lmList[12][2]
            x1, y1 = lmList[8][1], lmList[8][2]
            # 3. Check which fingers are up
            fingers = detector.fingersUp(img)
            # print(fingers)
            # 4. If Selection Mode - Two finger are up
            if fingers.count(1) == 5:
                xp, yp = 0, 0
                # print("Selection Mode")
                # # Checking for the click
                drawColor = rgb_values
                cv2.rectangle(img, (x3 - 5, y3 - 25), (x2 + 5, y2 + 25), drawColor, cv2.FILLED)

            # 5. If Drawing Mode - Index finger is up

            if fingers[1] and fingers[2]:
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                # cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1

            if not (fingers[3] or fingers[1] or fingers[2] or fingers[4]):
                drawColor = (0, 0, 0)
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                print("In clearing mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

        cv2.putText(img, str(int(rotang)), (35, 35), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        img4 = cv2.GaussianBlur(imgCanvas, (15, 15), 30)
        img = cv2.addWeighted(img, .7, img4, 1.5, 1)
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)
        # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
        img[0:102, 0:301] = header
        cv2.imshow("Image", img)
        cv2.imshow("Canvas", imgCanvas)
        cv2.imshow("Inv", imgInv)
        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()