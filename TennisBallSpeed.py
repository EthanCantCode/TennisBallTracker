import cv2
import numpy as np

#live update of a counter for the video
num = 0
#Font for text on video
font = cv2.FONT_HERSHEY_SIMPLEX

# video path
video = cv2.VideoCapture("Video Goes Here")

#FPS of the video
fps = video.get(cv2.CAP_PROP_FPS)
print(f"Frames per second: {fps}")

prev_x, prev_y = None, None

speed_mph = 0



#Running video in window
while True:
    
    cv2.waitKey(int(1000/fps))  # Wait for the appropriate time based on FPS
    
    ret, frame = video.read()

    #Color range of the ball
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    L_Yellow = np.array([29, 86, 6])
    U_Yellow = np.array([64, 255, 255])

    mask = cv2.inRange(hsv, L_Yellow, U_Yellow)

    #Getting the ball contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    for c in contours:
        area = cv2.contourArea(c)

        if area > 100:  # ignore tiny noise
            (x, y), radius = cv2.minEnclosingCircle(c)

            x = int(x)
            y = int(y)

            if prev_x is not None:

                distance = np.sqrt((x - prev_x)**2 + (y - prev_y)**2)

                if distance > 100: #further the distance is lower the number 
                    #Speed calculation
                    distance_feet = distance * 0.001  # Assuming 1 pixel = 0.1 feet 
                    speed_ft_per_sec = distance_feet * fps
                    speed_mph = speed_ft_per_sec * 0.6818

                #print("Speed:", speed_mph)
                    speed = distance * fps  # pixels per second
                    print(f"Speed: {speed:.2f} pixels/second")

            prev_x, prev_y = x, y

            if radius > 5:
                center = (int(x), int(y))

                cv2.circle(frame, center, int(radius), (0,255,0), 2)

    #Frame counter
    cv2.putText(frame, 
            f"Speed: {speed_mph:.2f} feet per second", 
            (50, 50), 
            font, 1, 
            (0, 255, 255), 
            2, 
            cv2.LINE_4)
    
    
    if not ret:
        break
    cv2.imshow("Tennis Ball", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()