import cv2
import mediapipe as mp
import time
import math
from matplotlib.colors import LinearSegmentedColormap
class HandDetector:
    def __init__(self, mode=False, max_hands=2, model_comp=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        self.model_comp = model_comp

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            self.mode, self.max_hands, self.model_comp, self.detection_con, self.track_con)
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms,self.mp_hands.HAND_CONNECTIONS)
        return img
#############
    def create_gradient_color_map(color1, color2):
        cmap = LinearSegmentedColormap.from_list('custom_gradient', [color1, color2], N=100)
        return cmap

    def get_color_from_gradient(percentage, gradient_cmap):
        return gradient_cmap(percentage / 100.0)

    def get_rgb_values(color):
        return [int(x * 255) for x in color[:3]]

    def main():
        color1 = (.2, .3, .5)  # RGB values for the first color
        color2 = (.4, .1, .65)  # RGB values for the second color

        gradient_cmap = create_gradient_color_map(color1, color2)

        while True:
            try:
                percentage = int(input("Enter a number between 1 and 100: "))
                if 0 <= percentage <= 100:
                    break
                else:
                    print("Please enter a number between 1 and 100.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        selected_color = get_color_from_gradient(percentage, gradient_cmap)
        rgb_values = get_rgb_values(selected_color)
        print((rgb_values))

#####################

    def unit_vector(self , vector):
        mag = ((vector[0]**2) + (vector[1]**2))**0.5
        if(mag==0):
            mag=1
        return [v/mag for v in vector ]
    def find_position(self, img, hand_no=0, draw=True):
        x_list = []
        y_list = []
        bbox = []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            if x_list and y_list:
                xmin, xmax = min(x_list), max(x_list)
                ymin, ymax = min(y_list), max(y_list)
                bbox = xmin, ymin, xmax, ymax

                if draw:
                    cv2.rectangle(img, (xmin - 20, ymin - 20),
                                  (xmax + 20, ymax + 20), (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self,img):
        fingers = []
        # Thumb
        '''if self.lmList[self.tip_ids[0]][1] > self.lmList[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)'''

        # Fingers
        for id in range(5):
            if self.lmList[self.tip_ids[id]][2] < self.lmList[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # totalFingers = fingers.count(1)

        return fingers

    def find_rotation(self):
        if len(self.lmList) >= 4:
            # Get the landmarks for the thumb, index, middle, ring, and pinky fingers

            indexmcp = self.lmList[5]
            middlemcp = self.lmList[9]
            ringmcp = self.lmList[13]
            pinkymcp = self.lmList[17]

            indexpip = self.lmList[6]
            middlepip = self.lmList[10]
            ringpip = self.lmList[14]
            pinkypip = self.lmList[19]

            vec1 = [indexpip[1] - indexmcp[1], indexpip[2] - indexmcp[2]]
            vec2 = [middlepip[1] - middlemcp[1], middlepip[2] - middlemcp[2]]
            vec3 = [ringpip[1] - ringmcp[1], ringpip[2] - ringmcp[2]]
            vec4 = [pinkypip[1] - pinkymcp[1], pinkypip[2] - pinkymcp[2]]
            vecs = [vec1,vec2,vec3,vec4]
            uvecs = [self.unit_vector(v) for v in vecs]
            s = [0,0]
            for u in uvecs:
                s= [ s[0]+ u[0], s[1] +u[1] ]
            s= [s[0]/4,s[1]/4]

            # Calculate the average angle
            angle = math.degrees(math.atan2(s[0],- s[1]))
            angle += 0
            return angle
        else:
            return None

    def fist(self):
        if self.fingersUp().count(1) == 5:
            return "FIST ON"
        elif self.fingersUp().count(1) == 0:
            return "FIST OFF"
        else:
            return None


def main():
    p_time = 0
    c_time = 0

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = cv2.flip(img,1)
        if not success:
            print("Error: Failed to capture image.")
            break

        img = detector.find_hands(img)
        lmList, bbox = detector.find_position(img)
        rotang=0
        rotation_angle=0
        if lmList:
            rotation_angle = detector.find_rotation()
            print(type(rotation_angle),rotation_angle)
            fist=detector.fist()
            if rotation_angle is not None:
                print(f"Rotation angle: {rotation_angle:.2f}")
            if fist is not None:
                print(f" Rotation Angle: {fist}")
        rotang=rotation_angle
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        #print(type(fps),type(rotation_angle),type(rotang),rotation_angle,fps,rotang)
        p_time = c_time

        cv2.putText(img, str(int(rotang)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
